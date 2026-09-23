"""Tests for kb_freshness.py.

Run: uv run --with pytest --with pyyaml pytest scripts/test_kb_freshness.py
"""

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
    [c] = kf.claims_in(note)
    assert (c.id, c.repo, c.path, c.anchor, c.baseline) == (
        "gate",
        "steward",
        "gate.sh",
        "blocker|major",
        "4170bc6",
    )


@pytest.mark.parametrize(
    "text", ["no frontmatter\n", "---\ntitle: t\n---\n", "---\n: [bad\n---\n"]
)
def test_notes_without_evidence_yield_nothing(tmp_path: Path, text: str) -> None:
    note = tmp_path / "n.md"
    note.write_text(text)
    assert kf.claims_in(note) == []
