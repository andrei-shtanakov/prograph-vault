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


def check(c: kf.Claim, workspace: Path, target: str = "local") -> kf.Verdict:
    """Check one claim with a fresh revision resolver."""
    return kf.check_claim(c, kf.Revisions(workspace, target))


def claim(base: str | None, anchor: str | None = None, path: str = "gate.sh"):
    """A claim about steward/<path>."""
    return kf.Claim("note.md", "c", "steward", path, anchor, base)


def test_unchanged_when_file_is_identical(workspace: Path) -> None:
    v = check(claim(baseline(workspace)), workspace)
    assert v.status == "unchanged"


def test_changed_when_file_differs(workspace: Path) -> None:
    base = baseline(workspace)
    commit(workspace, CODE + "extra\n")
    assert check(claim(base), workspace).status == "changed"


def test_anchor_window_ignores_edits_elsewhere(workspace: Path) -> None:
    base = baseline(workspace)
    commit(workspace, CODE.replace("line 1\n", "line one\n"))
    v = check(claim(base, anchor="blocker|major"), workspace)
    assert v.status == "unchanged"


def test_anchor_window_catches_edits_near_anchor(workspace: Path) -> None:
    base = baseline(workspace)
    commit(workspace, CODE.replace("line 20\n", "line twenty\n"))
    v = check(claim(base, anchor="blocker|major"), workspace)
    assert v.status == "changed"


def test_missing_when_anchor_is_gone(workspace: Path) -> None:
    base = baseline(workspace)
    commit(workspace, CODE.replace("blocker|major", "blocker"))
    v = check(claim(base, anchor="blocker|major"), workspace)
    assert v.status == "missing"


def test_missing_when_path_is_gone(workspace: Path) -> None:
    v = check(claim(baseline(workspace), path="nope.sh"), workspace)
    assert v.status == "missing"


def test_ambiguous_anchor_is_unverified(workspace: Path) -> None:
    v = check(claim(baseline(workspace), anchor="line 1"), workspace)
    assert v.status == "unverified"


@pytest.mark.parametrize("base", [None, "deadbeef"])
def test_no_or_unknown_baseline_is_unverified(workspace: Path, base) -> None:
    assert check(claim(base), workspace).status == "unverified"


def test_no_checkout_is_unverified(tmp_path: Path) -> None:
    assert check(claim("abc"), tmp_path).status == "unverified"


def test_claims_parsed_from_frontmatter(tmp_path: Path) -> None:
    note = tmp_path / "rule.md"
    note.write_text(
        "---\ntitle: t\nevidence:\n"
        "  - id: gate\n    repo: steward\n    path: gate.sh\n"
        "    anchor: 'blocker|major'\n    baseline: 4170bc6\n    claim: gate\n"
        "---\n\nbody\n\nOnly blocker and major block. ^gate\n"
    )
    scan = kf.scan_note(note)
    [c] = scan.claims
    assert (c.id, c.repo, c.path, c.anchor, c.baseline, c.block, c.statement) == (
        "gate",
        "steward",
        "gate.sh",
        "blocker|major",
        "4170bc6",
        "gate",
        "Only blocker and major block.",
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


GOOD = (
    "  - id: ok\n    repo: steward\n    path: gate.sh\n    baseline: abc\n"
    "    claim: ok\n"
)


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
    note.write_text(f"---\n{frontmatter}---\nRule. ^ok\n")
    problems = kf.scan_note(note).problems
    assert problems
    assert all(v.status == "invalid" and v.detail for v in problems)


def test_valid_entries_survive_a_bad_sibling(tmp_path: Path) -> None:
    note = tmp_path / "n.md"
    note.write_text("---\nevidence:\n  - broken\n" + GOOD + "---\nRule. ^ok\n")
    scan = kf.scan_note(note)
    assert [c.id for c in scan.claims] == ["ok"]
    assert [v.status for v in scan.problems] == ["invalid"]


def test_path_to_directory_is_invalid(workspace: Path) -> None:
    repo = workspace / "steward"
    (repo / "sub").mkdir()
    (repo / "sub" / "f").write_text("x\n")
    run(repo, "add", ".")
    run(repo, "commit", "-qm", "dir")
    v = check(claim(baseline(workspace), path="sub"), workspace)
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
    v = check(claim(base, anchor="NEW RULE"), workspace)
    assert v.status == "unverified"
    assert "baseline" in v.detail


def test_anchor_ambiguous_at_baseline_is_unverified(workspace: Path) -> None:
    commit(workspace, CODE + "blocker|major\n")
    base = baseline(workspace)
    commit(workspace, CODE)
    v = check(claim(base, anchor="blocker|major"), workspace)
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
    entry = (
        f"  - id: g\n    repo: steward\n    path: gate.sh\n    baseline: {base}\n"
        "    claim: g\n"
    )
    write_note(workspace, "a.md", f"---\nevidence:\n{entry}---\nRule. ^g\n")
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


def note_with(tmp_path: Path, body: str, claim_ref: str = "gate") -> Path:
    """A note with one well-formed entry pointing at claim_ref, plus body."""
    note = tmp_path / "n.md"
    entry = (
        f"  - id: e\n    repo: steward\n    path: gate.sh\n    claim: '{claim_ref}'\n"
    )
    note.write_text(f"---\nevidence:\n{entry}---\n{body}")
    return note


def test_claim_block_is_the_whole_list_item(tmp_path: Path) -> None:
    body = (
        "# Rules\n\n- first item\n"
        "- **Blocking** findings are\n  blocker or major only. ^gate\n"
        "- next item\n"
    )
    [c] = kf.scan_note(note_with(tmp_path, body)).claims
    assert c.statement == "- **Blocking** findings are blocker or major only."


def test_claim_block_is_the_whole_paragraph(tmp_path: Path) -> None:
    body = "Intro.\n\nThe gate blocks\non major. ^gate\n\nAfter.\n"
    [c] = kf.scan_note(note_with(tmp_path, body)).claims
    assert c.statement == "The gate blocks on major."


def test_caret_prefix_in_reference_is_accepted(tmp_path: Path) -> None:
    [c] = kf.scan_note(note_with(tmp_path, "Rule. ^gate\n", "^gate")).claims
    assert c.block == "gate"


@pytest.mark.parametrize(
    ("body", "claim_ref", "why"),
    [
        ("Rule without marker.\n", "gate", "not found"),
        ("A. ^gate\n\nB. ^gate\n", "gate", "2 times"),
        ("```\ncode ^gate\n```\n", "gate", "not found"),  # fenced: not a block
        ("Rule. ^gate\n", "", "claim"),
    ],
)
def test_unbound_claim_is_invalid(
    tmp_path: Path, body: str, claim_ref: str, why: str
) -> None:
    scan = kf.scan_note(note_with(tmp_path, body, claim_ref))
    [v] = scan.problems
    assert (v.status, scan.claims) == ("invalid", [])
    assert why in v.detail


def test_empty_evidence_list_counts_as_declared(tmp_path: Path) -> None:
    note = tmp_path / "n.md"
    note.write_text("---\nevidence: []\n---\n")
    assert kf.scan_note(note).has_evidence


def test_verdict_carries_the_statement(workspace: Path) -> None:
    base = baseline(workspace)
    c = kf.Claim("n.md", "c", "steward", "gate.sh", None, base, "g", "Rule text.")
    commit(workspace, CODE + "extra\n")
    v = check(c, workspace)
    assert (v.status, v.block, v.statement) == ("changed", "g", "Rule text.")
    assert kf.render(v).endswith("\n    ^g: Rule text.")


def test_unchanged_render_stays_one_line(workspace: Path) -> None:
    c = kf.Claim("n.md", "c", "steward", "gate.sh", None, baseline(workspace), "g", "R")
    assert "\n" not in kf.render(check(c, workspace))


FENCED_MARKERS = {
    "other fence char inside": "```text\n~~~\nExample. ^gate\n```\n",
    "backticks inside tildes": "~~~\n```\nExample. ^gate\n~~~\n",
    "shorter fence inside": "````\n```\nExample. ^gate\n````\n",
    "closer with info string": "```\n```text\nExample. ^gate\n```\n",
    "unclosed fence": "```\nExample. ^gate\n",
    "fence inside a list item": "- item\n     ```\n     Example. ^gate\n     ```\n",
}


@pytest.mark.parametrize("body", FENCED_MARKERS.values(), ids=FENCED_MARKERS.keys())
def test_marker_inside_code_is_not_a_claim(tmp_path: Path, body: str) -> None:
    [v] = kf.scan_note(note_with(tmp_path, body)).problems
    assert "not found" in v.detail


OUTSIDE_CODE = {
    "after a closed fence": ("```\ncode\n```\n\nRule. ^gate\n", "Rule."),
    "longer closer closes": ("~~~\ncode\n~~~~\n\nRule. ^gate\n", "Rule."),
    "right under a fence": ("```\ncode\n```\nRule. ^gate\n", "Rule."),
    "trailing spaces": ("Rule. ^gate  \n", "Rule."),
    "trailing tab": ("Rule. ^gate\t\n", "Rule."),
}


@pytest.mark.parametrize(
    ("body", "statement"), OUTSIDE_CODE.values(), ids=OUTSIDE_CODE.keys()
)
def test_marker_outside_code_is_a_claim(
    tmp_path: Path, body: str, statement: str
) -> None:
    [c] = kf.scan_note(note_with(tmp_path, body)).claims
    assert c.statement == statement


@pytest.fixture
def published(tmp_path: Path) -> Path:
    """Workspace whose `steward` is a clone of a bare origin fed by `seed`."""
    seed = tmp_path / "seed"
    seed.mkdir()
    run(seed, "init", "-q", "-b", "master")
    run(seed, "config", "user.email", "t@t")
    run(seed, "config", "user.name", "t")
    (seed / "gate.sh").write_text(CODE)
    run(seed, "add", ".")
    run(seed, "commit", "-qm", "init")
    origin = tmp_path / "origin.git"
    run(tmp_path, "clone", "-q", "--bare", str(seed), str(origin))
    run(seed, "remote", "add", "origin", str(origin))
    workspace = tmp_path / "ws"
    workspace.mkdir()
    run(workspace, "clone", "-q", str(origin), "steward")
    run(workspace / "steward", "config", "user.email", "t@t")
    run(workspace / "steward", "config", "user.name", "t")
    return workspace


def push_from_seed(workspace: Path, text: str) -> None:
    """Publish a new gate.sh to origin without touching the local checkout."""
    seed = workspace.parent / "seed"
    (seed / "gate.sh").write_text(text)
    run(seed, "commit", "-qam", "published edit")
    run(seed, "push", "-q", "origin", "master")


def test_published_ignores_the_local_branch(published: Path) -> None:
    base = baseline(published)
    local = published / "steward"
    run(local, "switch", "-q", "-c", "feature")
    commit(published, CODE + "local only\n")
    assert check(claim(base), published, "local").status == "changed"
    assert check(claim(base), published, "published").status == "unchanged"


def test_published_fetches_before_reading(published: Path) -> None:
    base = baseline(published)
    push_from_seed(published, CODE + "published\n")
    assert check(claim(base), published, "local").status == "unchanged"
    assert check(claim(base), published, "published").status == "changed"


def test_failed_fetch_is_unverified_not_stale(published: Path) -> None:
    base = baseline(published)
    local = published / "steward"
    run(local, "remote", "set-url", "origin", str(published / "nowhere.git"))
    v = check(claim(base), published, "published")
    assert v.status == "unverified"
    assert "stale ref" in v.detail


def test_unknown_default_branch_is_unverified(published: Path) -> None:
    base = baseline(published)
    run(published.parent / "origin.git", "symbolic-ref", "HEAD", "refs/heads/ghost")
    v = check(claim(base), published, "published")
    assert v.status == "unverified"
    assert "default branch" in v.detail


def test_default_branch_is_asked_from_origin(published: Path) -> None:
    """A stale local origin/HEAD must not pick the old default branch."""
    base = baseline(published)
    seed = published.parent / "seed"
    run(seed, "switch", "-q", "-c", "main")
    (seed / "gate.sh").write_text(CODE + "on main\n")
    run(seed, "commit", "-qam", "main moves on")
    run(seed, "push", "-q", "origin", "main")
    run(published.parent / "origin.git", "symbolic-ref", "HEAD", "refs/heads/main")
    local_head = run(published / "steward", "symbolic-ref", "refs/remotes/origin/HEAD")
    assert local_head == "refs/remotes/origin/master"  # stale on purpose
    v = check(claim(base), published, "published")
    assert (v.status, v.target) == ("changed", "origin/main")


def test_verdict_names_full_revision_and_target(published: Path) -> None:
    base = baseline(published)
    run(published / "steward", "switch", "-q", "-c", "feature")
    local = check(claim(base), published, "local")
    remote = check(claim(base), published, "published")
    sha = run(published / "steward", "rev-parse", "HEAD")
    assert (local.head, local.target) == (sha, "HEAD (feature)")
    assert (remote.head, remote.target) == (sha, "origin/master")


def test_revision_is_resolved_once_per_run(published: Path) -> None:
    revisions = kf.Revisions(published, "published")
    first = revisions.get("steward")
    push_from_seed(published, CODE + "later\n")
    assert revisions.get("steward") is first


def test_scope_file_sees_edits_outside_the_window(workspace: Path) -> None:
    base = baseline(workspace)
    commit(workspace, CODE.replace("line 1\n", "line one\n"))
    c = kf.Claim("n.md", "c", "steward", "gate.sh", "blocker|major", base, scope="file")
    v = check(c, workspace)
    assert (v.status, v.detail.split()[0]) == ("changed", "file")


def test_scope_file_still_requires_the_anchor(workspace: Path) -> None:
    base = baseline(workspace)
    commit(workspace, CODE.replace("blocker|major", "blocker"))
    c = kf.Claim("n.md", "c", "steward", "gate.sh", "blocker|major", base, scope="file")
    assert check(c, workspace).status == "missing"


@pytest.mark.parametrize(
    ("value", "ok"), [("file", True), ("anchor", True), ("x", False)]
)
def test_scope_values(tmp_path: Path, value: str, ok: bool) -> None:
    note = tmp_path / "n.md"
    entry = (
        "  - id: e\n    repo: steward\n    path: gate.sh\n    anchor: a\n"
        f"    claim: g\n    scope: {value}\n"
    )
    note.write_text(f"---\nevidence:\n{entry}---\nRule. ^g\n")
    scan = kf.scan_note(note)
    assert bool(scan.claims) is ok
    if ok:
        assert scan.claims[0].scope == value


def test_scope_anchor_without_anchor_is_invalid(tmp_path: Path) -> None:
    note = tmp_path / "n.md"
    entry = (
        "  - id: e\n    repo: steward\n    path: g\n    claim: g\n    scope: anchor\n"
    )
    note.write_text(f"---\nevidence:\n{entry}---\nRule. ^g\n")
    [v] = kf.scan_note(note).problems
    assert "anchor" in v.detail


def test_cli_prints_the_revision_of_each_repo(published: Path) -> None:
    base = baseline(published)
    entry = (
        f"  - id: g\n    repo: steward\n    path: gate.sh\n    baseline: {base}\n"
        "    claim: g\n"
    )
    notes = write_note(published, "a.md", f"---\nevidence:\n{entry}---\nRule. ^g\n")
    out = audit("--target", "published", "--workspace", str(published), str(notes))
    sha = run(published / "steward", "rev-parse", "origin/master")
    assert f"revision|steward|origin/master|{sha}" in out.stdout.splitlines()


def test_blockquote_markers_are_dropped_from_the_statement(tmp_path: Path) -> None:
    body = "> **Not checked** by\n> any machine. ^gate\n"
    [c] = kf.scan_note(note_with(tmp_path, body)).claims
    assert c.statement == "**Not checked** by any machine."


@pytest.mark.parametrize("edit", ["\n\n" + CODE, CODE + "\n\n"], ids=["head", "tail"])
def test_scope_file_sees_blank_lines_at_the_edges(workspace: Path, edit: str) -> None:
    """Found by the mutation acceptance: content must not be stripped."""
    base = baseline(workspace)
    commit(workspace, edit)
    assert check(claim(base), workspace).status == "changed"
