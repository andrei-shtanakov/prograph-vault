"""Tests for kb_freshness.py.

Run: uv run --with pytest --with pyyaml pytest scripts/test_kb_freshness.py
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import kb_freshness as kf  # noqa: E402

CODE = "\n".join(f"line {i}" for i in range(1, 21)) + "\nTHRESHOLD = blocker|major\n"


def run(repo: Path, *args: str) -> str:
    """Run git in repo and return stdout."""
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    """A workspace with one sibling repo `steward` holding one committed file."""
    repo = tmp_path / "steward"
    repo.mkdir()
    run(repo, "init", "-q")
    run(repo, "config", "user.email", "t@t")
    run(repo, "config", "user.name", "t")
    (repo / "gate.sh").write_text(CODE)
    run(repo, "add", ".")
    run(repo, "commit", "-qm", "init")
    return tmp_path


def commit(workspace: Path, text: str) -> None:
    """Replace gate.sh and commit."""
    repo = workspace / "steward"
    (repo / "gate.sh").write_text(text)
    run(repo, "commit", "-qam", "edit")


def baseline(workspace: Path) -> str:
    """Short HEAD of the steward repo."""
    return run(workspace / "steward", "rev-parse", "--short", "HEAD")


def claim(base: str | None, anchor: str | None = None, path: str = "gate.sh"):
    """A claim about steward/<path>."""
    return kf.Claim("note.md", "c", "steward", path, anchor, base)


def test_unchanged_when_file_is_identical(workspace: Path) -> None:
    v = kf.check_claim(claim(baseline(workspace)), workspace)
    assert v.status == "unchanged"


def test_changed_when_file_differs(workspace: Path) -> None:
    base = baseline(workspace)
    commit(workspace, CODE + "extra\n")
    assert kf.check_claim(claim(base), workspace).status == "changed"


def test_anchor_window_ignores_edits_elsewhere(workspace: Path) -> None:
    base = baseline(workspace)
    commit(workspace, CODE.replace("line 1\n", "line one\n"))
    v = kf.check_claim(claim(base, anchor="blocker|major"), workspace)
    assert v.status == "unchanged"


def test_anchor_window_catches_edits_near_anchor(workspace: Path) -> None:
    base = baseline(workspace)
    commit(workspace, CODE.replace("line 20\n", "line twenty\n"))
    v = kf.check_claim(claim(base, anchor="blocker|major"), workspace)
    assert v.status == "changed"


def test_missing_when_anchor_is_gone(workspace: Path) -> None:
    base = baseline(workspace)
    commit(workspace, CODE.replace("blocker|major", "blocker"))
    v = kf.check_claim(claim(base, anchor="blocker|major"), workspace)
    assert v.status == "missing"


def test_missing_when_path_is_gone(workspace: Path) -> None:
    v = kf.check_claim(claim(baseline(workspace), path="nope.sh"), workspace)
    assert v.status == "missing"


def test_ambiguous_anchor_is_unverified(workspace: Path) -> None:
    v = kf.check_claim(claim(baseline(workspace), anchor="line 1"), workspace)
    assert v.status == "unverified"


@pytest.mark.parametrize("base", [None, "deadbeef"])
def test_no_or_unknown_baseline_is_unverified(workspace: Path, base) -> None:
    assert kf.check_claim(claim(base), workspace).status == "unverified"


def test_no_checkout_is_unverified(tmp_path: Path) -> None:
    assert kf.check_claim(claim("abc"), tmp_path).status == "unverified"


def test_claims_parsed_from_frontmatter(tmp_path: Path) -> None:
    note = tmp_path / "rule.md"
    note.write_text(
        "---\ntitle: t\nevidence:\n"
        "  - id: gate\n    repo: steward\n    path: gate.sh\n"
        "    anchor: 'blocker|major'\n    baseline: 4170bc6\n"
        "---\n\nbody\n"
    )
    scan = kf.scan_note(note)
    [c] = scan.claims
    assert (c.id, c.repo, c.path, c.anchor, c.baseline) == (
        "gate",
        "steward",
        "gate.sh",
        "blocker|major",
        "4170bc6",
    )
    assert (scan.problems, scan.unparsed) == ([], False)


@pytest.mark.parametrize("text", ["no frontmatter\n", "---\ntitle: t\n---\n"])
def test_notes_without_evidence_yield_nothing(tmp_path: Path, text: str) -> None:
    note = tmp_path / "n.md"
    note.write_text(text)
    scan = kf.scan_note(note)
    assert (scan.claims, scan.problems, scan.unparsed) == ([], [], False)


def test_broken_frontmatter_without_evidence_is_counted_not_failed(
    tmp_path: Path,
) -> None:
    note = tmp_path / "n.md"
    note.write_text("---\n: [bad\n---\n")
    scan = kf.scan_note(note)
    assert (scan.claims, scan.problems, scan.unparsed) == ([], [], True)


GOOD = "  - id: ok\n    repo: steward\n    path: gate.sh\n    baseline: abc\n"


@pytest.mark.parametrize(
    "frontmatter",
    [
        "evidence: [broken\n",  # YAML error in a note that declares evidence
        "evidence:\n  - id: [x\n",  # same, deeper
        "evidence: gate.sh\n",  # not a list
        "evidence:\n  - gate.sh\n",  # entry not a mapping
        "evidence:\n  - id: a\n    path: gate.sh\n",  # no repo
        "evidence:\n  - id: a\n    repo: steward\n",  # no path
        "evidence:\n  - id: a\n    repo: steward\n    path: ''\n",  # empty path
        "evidence:\n  - id: a\n    repo: steward\n    path: g\n    anchor: 7\n",
        "evidence:\n" + GOOD + GOOD,  # duplicate id
    ],
)
def test_malformed_evidence_is_invalid(tmp_path: Path, frontmatter: str) -> None:
    note = tmp_path / "n.md"
    note.write_text(f"---\n{frontmatter}---\n")
    problems = kf.scan_note(note).problems
    assert problems
    assert all(v.status == "invalid" and v.detail for v in problems)


def test_valid_entries_survive_a_bad_sibling(tmp_path: Path) -> None:
    note = tmp_path / "n.md"
    note.write_text("---\nevidence:\n  - broken\n" + GOOD + "---\n")
    scan = kf.scan_note(note)
    assert [c.id for c in scan.claims] == ["ok"]
    assert [v.status for v in scan.problems] == ["invalid"]


def test_path_to_directory_is_invalid(workspace: Path) -> None:
    repo = workspace / "steward"
    (repo / "sub").mkdir()
    (repo / "sub" / "f").write_text("x\n")
    run(repo, "add", ".")
    run(repo, "commit", "-qm", "dir")
    v = kf.check_claim(claim(baseline(workspace), path="sub"), workspace)
    assert v.status == "invalid"


@pytest.mark.parametrize("path", [".", "./", "/etc/passwd", "../devtools/x.sh"])
def test_path_outside_a_repo_file_is_invalid(tmp_path: Path, path: str) -> None:
    note = tmp_path / "n.md"
    entry = f"  - id: a\n    repo: steward\n    path: '{path}'\n"
    note.write_text(f"---\nevidence:\n{entry}---\n")
    [v] = kf.scan_note(note).problems
    assert v.status == "invalid"


def test_anchor_absent_at_baseline_is_unverified(workspace: Path) -> None:
    base = baseline(workspace)
    commit(workspace, CODE + "NEW RULE\n")
    v = kf.check_claim(claim(base, anchor="NEW RULE"), workspace)
    assert v.status == "unverified"
    assert "baseline" in v.detail


def test_anchor_ambiguous_at_baseline_is_unverified(workspace: Path) -> None:
    commit(workspace, CODE + "blocker|major\n")
    base = baseline(workspace)
    commit(workspace, CODE)
    v = kf.check_claim(claim(base, anchor="blocker|major"), workspace)
    assert v.status == "unverified"
    assert "baseline" in v.detail


def write_note(tmp_path: Path, name: str, text: str) -> Path:
    """Write a note under tmp_path/notes and return that directory."""
    notes = tmp_path / "notes"
    notes.mkdir(exist_ok=True)
    (notes / name).write_text(text)
    return notes


def audit(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the script as a CLI."""
    script = Path(kf.__file__)
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_strict_fails_when_nothing_is_checked(tmp_path: Path) -> None:
    notes = write_note(tmp_path, "a.md", "---\ntitle: t\n---\n")
    out = audit("--strict", "--workspace", str(tmp_path), str(notes))
    assert out.returncode == 1
    assert "notes=1 with_evidence=0" in out.stdout


def test_strict_fails_on_broken_evidence_yaml(tmp_path: Path) -> None:
    notes = write_note(tmp_path, "a.md", "---\nevidence: [broken\n---\n")
    out = audit("--strict", "--workspace", str(tmp_path), str(notes))
    assert out.returncode == 1
    assert out.stdout.startswith("invalid|")
    assert "invalid=1" in out.stdout


def test_summary_counts_coverage(workspace: Path) -> None:
    base = baseline(workspace)
    entry = f"  - id: g\n    repo: steward\n    path: gate.sh\n    baseline: {base}\n"
    write_note(workspace, "a.md", f"---\nevidence:\n{entry}---\n")
    write_note(workspace, "b.md", "---\n: [bad\n---\n")
    notes = write_note(workspace, "c.md", "plain\n")
    out = audit("--strict", "--workspace", str(workspace), str(notes))
    assert out.returncode == 0, out.stdout
    assert out.stdout.splitlines()[-1] == (
        "summary|unchanged=1 changed=0 missing=0 unverified=0 invalid=0 "
        "notes=3 with_evidence=1 unparsed_frontmatter=1"
    )


def test_json_ends_with_summary_record(workspace: Path) -> None:
    notes = write_note(workspace, "a.md", "plain\n")
    out = audit("--json", "--workspace", str(workspace), str(notes))
    last = json.loads(out.stdout.splitlines()[-1])
    assert last["summary"]["notes"] == 1
    assert last["summary"]["with_evidence"] == 0
