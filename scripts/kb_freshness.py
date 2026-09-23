#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Claim-level freshness audit for the KB (no LLM, read-only).

A note opts in by listing the code its statements rest on:

    evidence:
      - id: review-threshold            # stable name of the claim
        repo: steward                   # sibling checkout in the workspace
        path: scripts/review/apply-threshold.sh
        anchor: "severity blocker|major"  # optional verbatim quote
        baseline: 4170bc6               # commit the claim was checked against

Status per claim:
  unchanged   path (or the anchor window) is identical at baseline and HEAD
  changed     it differs: re-read the code and re-confirm the claim
  missing     path is gone at HEAD, or the anchor no longer occurs
  unverified  no baseline, unknown commit, no checkout, or ambiguous anchor

Usage: uv run scripts/kb_freshness.py [--json] [--strict] [PATH ...]
PATH defaults to authored/. --strict exits 1 unless every claim is unchanged.
The script never writes: bumping `baseline` is a human edit under review.
"""

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

VAULT = Path(__file__).resolve().parents[1]
ANCHOR_CONTEXT = 3  # lines above and below the anchor that must stay identical


@dataclass(frozen=True)
class Claim:
    """One evidence entry from a note's frontmatter."""

    doc: str
    id: str
    repo: str
    path: str
    anchor: str | None
    baseline: str | None


@dataclass(frozen=True)
class Verdict:
    """Freshness of one claim."""

    doc: str
    id: str
    repo: str
    path: str
    status: str
    detail: str
    head: str | None


def main() -> int:
    """Audit every claim under the given paths and print the verdicts."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path, default=[VAULT / "authored"])
    parser.add_argument("--workspace", type=Path, default=VAULT.parent)
    parser.add_argument("--json", action="store_true", help="one JSON object per line")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    claims = [c for p in args.paths for c in collect_claims(p)]
    verdicts = [check_claim(c, args.workspace) for c in claims]
    for v in verdicts:
        print(json.dumps(asdict(v), ensure_ascii=False) if args.json else render(v))
    if not args.json:
        print(summary(verdicts))
    stale = any(v.status != "unchanged" for v in verdicts)
    return 1 if args.strict and stale else 0


def collect_claims(root: Path) -> list[Claim]:
    """Claims from every markdown file under root (or root itself)."""
    files = [root] if root.is_file() else sorted(root.rglob("*.md"))
    return [c for f in files for c in claims_in(f)]


def claims_in(path: Path) -> list[Claim]:
    """Parse the `evidence:` list of one note; notes without it yield nothing."""
    meta = frontmatter(path.read_text(encoding="utf-8"))
    entries = meta.get("evidence") or []
    doc = display_path(path)
    return [
        Claim(
            doc=doc,
            id=str(e.get("id") or f"{e.get('repo')}:{e.get('path')}"),
            repo=str(e.get("repo", "")),
            path=str(e.get("path", "")),
            anchor=e.get("anchor"),
            baseline=str(e["baseline"]) if e.get("baseline") else None,
        )
        for e in entries
        if isinstance(e, dict)
    ]


def frontmatter(text: str) -> dict:
    """YAML between the leading `---` fences; {} when absent or invalid."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    try:
        meta = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return {}
    return meta if isinstance(meta, dict) else {}


def check_claim(claim: Claim, workspace: Path) -> Verdict:
    """Compare the claim's evidence at its baseline commit and at HEAD."""
    repo = workspace / claim.repo
    if not claim.repo or not (repo / ".git").exists():
        return verdict(claim, "unverified", f"no checkout at {repo}", None)
    head = git(repo, "rev-parse", "--short", "HEAD")
    now = git(repo, "show", f"HEAD:{claim.path}")
    if now is None:
        return verdict(claim, "missing", "path absent at HEAD", head)
    if claim.anchor and now.count(claim.anchor) != 1:
        found = now.count(claim.anchor)
        status = "missing" if found == 0 else "unverified"
        return verdict(claim, status, f"anchor occurs {found} times at HEAD", head)
    if not claim.baseline:
        return verdict(
            claim, "unverified", f"no baseline; current HEAD is {head}", head
        )
    then = git(repo, "show", f"{claim.baseline}:{claim.path}")
    if then is None:
        detail = f"baseline {claim.baseline} unknown or path absent there"
        return verdict(claim, "unverified", detail, head)
    same = (
        window(then, claim.anchor) == window(now, claim.anchor)
        if claim.anchor
        else then == now
    )
    scope = "anchor window" if claim.anchor else "file"
    if same:
        return verdict(claim, "unchanged", f"{scope} same since {claim.baseline}", head)
    return verdict(claim, "changed", f"{scope} differs {claim.baseline}..{head}", head)


def window(text: str, anchor: str | None) -> str | None:
    """Lines around the single occurrence of anchor; None if it is not unique."""
    if anchor is None or text.count(anchor) != 1:
        return None
    lines = text.splitlines()
    first = text[: text.index(anchor)].count("\n")
    last = first + anchor.count("\n")
    lo, hi = max(0, first - ANCHOR_CONTEXT), last + ANCHOR_CONTEXT + 1
    return "\n".join(lines[lo:hi])


def git(repo: Path, *args: str) -> str | None:
    """stdout of a read-only git command, or None if it failed."""
    out = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=False
    )
    return out.stdout.strip("\n") if out.returncode == 0 else None


def verdict(claim: Claim, status: str, detail: str, head: str | None) -> Verdict:
    """Build a verdict carrying the claim's identity."""
    return Verdict(claim.doc, claim.id, claim.repo, claim.path, status, detail, head)


def render(v: Verdict) -> str:
    """One pipe-separated line per claim."""
    return f"{v.status}|{v.doc}|{v.id}|{v.repo}/{v.path}|{v.detail}"


def summary(verdicts: list[Verdict]) -> str:
    """Counts per status, stable order."""
    order = ("unchanged", "changed", "missing", "unverified")
    counts = {s: sum(v.status == s for v in verdicts) for s in order}
    return "summary|" + " ".join(f"{s}={n}" for s, n in counts.items())


def display_path(path: Path) -> str:
    """Path relative to the vault when possible."""
    try:
        return str(path.resolve().relative_to(VAULT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    sys.exit(main())
