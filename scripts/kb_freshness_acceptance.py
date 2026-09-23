#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Mutation acceptance for kb_freshness.py: does every real claim catch what it should?

For each claim declared under authored/, the evidence repo is copied into a temp
workspace at its published revision (fetch + origin default branch, the same
revision the weekly run reads). Prepared mutations are committed there and the
claim is checked again; the status must match the expectation for its scope.
Note-level mutations (broken frontmatter, a dropped block marker) run on a temp
copy of the note. Sibling checkouts are never touched.

Mutation              anchor scope   file scope     no anchor
  control (none)      as published   as published   as published
  edit anchor line    changed        changed        -
  delete anchor       missing        missing        -
  duplicate anchor    unverified     unverified     -
  shift lines         unchanged      changed        changed
  edit far line       unchanged      changed        changed
  delete file         missing        missing        missing
  unknown baseline    unverified     unverified     unverified
  broken frontmatter  invalid        invalid        invalid
  drop block marker   invalid        invalid        invalid

The control row is the published status, so a claim that is already stale (the
point of the audit) stays in the run: its mutations are still expected to move
it the same way, except where `changed` absorbs them — noted per row.

A shifted anchor keeps its window only if at least 3 lines sat above it; an
anchor in the first 3 lines is expected to report `changed` on a shift.

The run fails closed: a note whose markup is broken is a failed row, not a
skipped note, and a run that checked no claim at all exits 1. A mutation that
does not apply (a file too short for a far edit) is printed as `skip`.

Usage: uv run scripts/kb_freshness_acceptance.py [PATH ...]   (default authored/)
Exits 1 on any mismatch, any markup problem, or when no claim was checked.
"""

import argparse
import dataclasses
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kb_freshness as kf  # noqa: E402

FAR = 4  # a line this far from the anchor is outside its ±3 window
Mutation = Callable[[str, kf.Claim], str | None]  # new text; None = not applicable
DELETE = None  # in a plan row: the mutation removes the file
SKIPPED = "not applicable"


def main() -> int:
    """Run every mutation against every claim and print a table."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path, default=[kf.VAULT / "authored"])
    parser.add_argument("--workspace", type=Path, default=kf.VAULT.parent)
    args = parser.parse_args()
    notes = [f for p in args.paths for f in kf.markdown_files(p)]
    scans = [s for s in map(kf.scan_note, notes) if s.has_evidence]
    published = kf.Revisions(args.workspace, "published")
    rows: list[tuple[str, str, str, str]] = [
        (v.doc, f"markup {v.id}", "no problem", f"invalid: {v.detail}")
        for s in scans
        for v in s.problems
    ]
    with tempfile.TemporaryDirectory() as tmp:
        sandbox = Path(tmp)
        for scan in scans:
            for claim in scan.claims:
                rows += claim_rows(claim, published, sandbox)
            if scan.claims:
                rows += note_rows(scan, args.workspace / "prograph-vault", sandbox)
    for claim_id, mutation, expected, actual in rows:
        mark = row_mark(expected, actual)
        print(f"{mark}|{claim_id}|{mutation}|expected={expected}|actual={actual}")
    marks = [row_mark(expected, actual) for _, _, expected, actual in rows]
    claims = sum(len(s.claims) for s in scans)
    failed, skipped = marks.count("MISMATCH"), marks.count("skip")
    print(
        f"summary|claims={claims} rows={len(rows)} mismatches={failed} "
        f"skipped={skipped}"
    )
    return 1 if failed or claims == 0 else 0


def row_mark(expected: str, actual: str) -> str:
    """ok, skip (mutation not applicable) or MISMATCH."""
    if actual == SKIPPED:
        return "skip"
    return "ok" if expected == actual else "MISMATCH"


def claim_rows(
    claim: kf.Claim, published: kf.Revisions, sandbox: Path
) -> list[tuple[str, str, str, str]]:
    """Control plus every applicable file mutation for one claim."""
    rev = published.get(claim.repo)
    if rev.sha is None:
        return [
            (claim.id, "control", "resolvable revision", f"unverified: {rev.error}")
        ]
    repo = sandbox / f"{claim.repo}-{claim.id}"
    clone_at(published.workspace / claim.repo, rev.sha, repo)
    local = kf.Revisions(sandbox, "local")
    renamed = dataclasses.replace(claim, repo=repo.name)
    control = kf.check_claim(renamed, local).status
    text = kf.blob(repo, "HEAD", claim.path) or ""
    rows = [(claim.id, "control", published_status(claim, published), control)]
    for name, mutate, expected in plan(claim, control, text):
        new = None if mutate is DELETE else mutate(text, claim)
        if mutate is not DELETE and new is None:  # not applicable to this file
            rows.append((claim.id, name, expected, SKIPPED))
            continue
        head = kf.git(repo, "rev-parse", "HEAD") or ""
        write_commit(repo, claim.path, new, name)
        actual = kf.check_claim(renamed, kf.Revisions(sandbox, "local")).status
        rows.append((claim.id, name, expected, actual))
        kf.git(repo, "reset", "-q", "--hard", head)
    stale = dataclasses.replace(renamed, baseline="0000000")
    unknown = kf.check_claim(stale, kf.Revisions(sandbox, "local")).status
    rows.append((claim.id, "unknown baseline", "unverified", unknown))
    return rows


def plan(
    claim: kf.Claim, control: str, text: str
) -> list[tuple[str, Mutation | None, str]]:
    """Mutations with the status each must produce for this claim's scope."""
    whole_file = claim.effective_scope == "file"
    # Once a claim is `changed`, a mutation that leaves the compared text alone
    # keeps it `changed`: the expectation follows the control, not `unchanged`.
    quiet = control if control == "changed" else "unchanged"
    rows: list[tuple[str, Mutation | None, str]] = []
    if claim.anchor:
        rows += [
            ("edit anchor line", edit_anchor_line, "changed"),
            ("delete anchor", delete_anchor, "missing"),
            ("duplicate anchor", duplicate_anchor, "unverified"),
        ]
    # Lines inserted on top enter the window of an anchor with < 3 lines above it.
    near_top = bool(claim.anchor) and text[: text.find(claim.anchor)].count("\n") < 3
    rows += [
        ("shift lines", shift_lines, "changed" if whole_file or near_top else quiet),
        ("edit far line", edit_far_line, "changed" if whole_file else quiet),
        ("delete file", DELETE, "missing"),
    ]
    return rows


def published_status(claim: kf.Claim, published: kf.Revisions) -> str:
    """The status the weekly run would report right now."""
    return kf.check_claim(claim, published).status


def edit_anchor_line(text: str, claim: kf.Claim) -> str:
    """Change the anchor's own line, keeping the quote itself intact."""
    anchor = claim.anchor or ""
    return text.replace(anchor, anchor + "  # mutated", 1)


def delete_anchor(text: str, claim: kf.Claim) -> str:
    """Remove the quote."""
    return text.replace(claim.anchor or "", "MUTATED-AWAY", 1)


def duplicate_anchor(text: str, claim: kf.Claim) -> str:
    """Make the quote ambiguous."""
    return f"{text.rstrip(chr(10))}\n{claim.anchor}\n"


def shift_lines(text: str, _claim: kf.Claim) -> str:
    """Insert lines at the top: the anchor moves, its window does not change."""
    return "\n" * 10 + text


def edit_far_line(text: str, claim: kf.Claim) -> str | None:
    """Edit a line at least FAR lines away from the anchor (first or last line)."""
    lines = text.split("\n")
    if not claim.anchor:
        lines[0] += "  # mutated"
        return "\n".join(lines)
    first = text[: text.index(claim.anchor)].count("\n")
    last = first + claim.anchor.count("\n")
    if first >= FAR:
        lines[0] += "  # mutated"
    elif len(lines) - 1 - last >= FAR:
        lines[-1] += "  # mutated"
    else:
        return None  # file too small for a line outside the window
    return "\n".join(lines)


def note_rows(
    scan: kf.NoteScan, vault: Path, sandbox: Path
) -> list[tuple[str, str, str, str]]:
    """Note-level mutations: the markup itself breaks."""
    source = (vault / scan.doc).read_text(encoding="utf-8")
    rows = []
    broken = source.replace("\nevidence:", "\nbroken: [\nevidence:", 1)
    rows.append(
        (scan.doc, "broken frontmatter", "invalid", note_status(broken, sandbox))
    )
    block = scan.claims[0].block or ""
    dropped = source.replace(f" ^{block}\n", "\n", 1)
    rows.append(
        (scan.doc, "drop block marker", "invalid", note_status(dropped, sandbox))
    )
    return rows


def note_status(text: str, sandbox: Path) -> str:
    """`invalid` if the mutated note yields a markup problem, else what it yields."""
    note = sandbox / "mutated-note.md"
    note.write_text(text, encoding="utf-8")
    scan = kf.scan_note(note)
    return "invalid" if scan.problems else "no problem reported"


def clone_at(source: Path, sha: str, target: Path) -> None:
    """A throwaway repo holding every object of `source`, checked out at `sha`."""
    run("git", "init", "-q", str(target))
    run(
        "git",
        "-C",
        str(target),
        "fetch",
        "-q",
        "--no-tags",
        str(source),
        "+refs/*:refs/source/*",
    )
    run("git", "-C", str(target), "checkout", "-q", "-B", "master", sha)
    run("git", "-C", str(target), "config", "user.email", "acceptance@local")
    run("git", "-C", str(target), "config", "user.name", "acceptance")


def write_commit(repo: Path, path: str, text: str | None, message: str) -> None:
    """Replace or delete `path` and commit."""
    target = repo / path
    if text is None:
        run("git", "-C", str(repo), "rm", "-q", path)
    else:
        target.write_text(text, encoding="utf-8")
        run("git", "-C", str(repo), "add", path)
    run("git", "-C", str(repo), "commit", "-q", "-m", message)


def run(*cmd: str) -> None:
    """Run a command, failing loudly."""
    subprocess.run(cmd, check=True, capture_output=True, text=True)


if __name__ == "__main__":
    sys.exit(main())
