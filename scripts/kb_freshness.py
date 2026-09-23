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
        claim: review-threshold         # block id of the statement in the body
        scope: file                     # optional: file | anchor (see below)

The statement itself lives once, in the note body, marked as an Obsidian block:
a paragraph or list item ending in ` ^review-threshold`. Several entries may point
at the same block. The block text is carried into the verdict so a `changed`
claim says which sentence to re-read.

`scope` says what must stay identical: `anchor` (the default when an anchor is
given) compares the anchor and 3 lines around it, `file` (the default without
one) compares the whole file. With `scope: file` an anchor still has to occur
exactly once — it pins where the claim lives, the file is what gets compared.

Target — which revision of each repo is read (`--target`):
  local       HEAD of the sibling checkout, whatever branch it is on (default,
              offline; the branch is printed so a feature branch is visible)
  published   `git fetch` of origin's default branch first, then that commit; a
              failed fetch or an unknown default branch makes every claim of the
              repo `unverified` instead of reading a stale ref
Each repo is resolved to one full SHA per run; the SHAs are printed as
`revision|<repo>|<target>|<sha>` lines so a report can be reproduced.

Status per claim:
  unchanged   path (or the anchor window) is identical at baseline and target
  changed     it differs: re-read the code and re-confirm the claim
  missing     path is gone at HEAD, or the anchor no longer occurs
  unverified  no baseline, unknown commit, no checkout, or an anchor that is
              not unique at HEAD or not unique at baseline
  invalid     the markup itself is broken: unparsable frontmatter in a note that
              declares `evidence`, a non-list or non-mapping entry, empty repo or
              path, a path that is not a file, a non-string anchor, a duplicate id,
              a missing `claim`, a claim block that is absent or not unique, an
              unknown `scope`, or `scope: anchor` without an anchor

`unchanged` means the quoted text and its surroundings did not move since the
baseline. It does not mean the claim is true.

Usage: uv run scripts/kb_freshness.py [--json] [--strict]
           [--target local|published] [PATH ...]
PATH defaults to authored/. The summary also reports coverage: notes scanned,
notes with evidence, notes whose frontmatter did not parse (those without an
`evidence` key are counted, not failed). --strict exits 1 unless at least one
claim was checked and every claim is unchanged.
The script never writes: bumping `baseline` is a human edit under review.
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath

import yaml

VAULT = Path(__file__).resolve().parents[1]
ANCHOR_CONTEXT = 3  # lines above and below the anchor that must stay identical
STATUSES = ("unchanged", "changed", "missing", "unverified", "invalid")
SCOPES = ("anchor", "file")
TARGETS = ("local", "published")
DECLARES_EVIDENCE = re.compile(r"^evidence\s*:", re.MULTILINE)
BLOCK_MARKER = re.compile(r"\s\^([A-Za-z0-9-]+)\s*$")
BLOCK_START = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


@dataclass(frozen=True)
class Claim:
    """One evidence entry from a note's frontmatter."""

    doc: str
    id: str
    repo: str
    path: str
    anchor: str | None
    baseline: str | None
    block: str | None = None
    statement: str | None = None
    scope: str | None = None

    @property
    def effective_scope(self) -> str:
        """`scope` as given, else `anchor` when there is one, else `file`."""
        return self.scope or ("anchor" if self.anchor else "file")


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
    block: str | None = None
    statement: str | None = None
    target: str | None = None


@dataclass(frozen=True)
class Revision:
    """The one commit of a repo that this run reads, or why there is none."""

    label: str
    sha: str | None
    error: str | None = None


class Revisions:
    """Resolves each sibling repo to one full SHA, once per run."""

    def __init__(self, workspace: Path, target: str) -> None:
        self.workspace = workspace
        self.target = target
        self.resolved: dict[str, Revision] = {}

    def get(self, repo: str) -> Revision:
        """The revision of `repo`, resolving (and fetching) it on first use."""
        if repo not in self.resolved:
            self.resolved[repo] = resolve(self.workspace / repo, self.target)
        return self.resolved[repo]


@dataclass(frozen=True)
class NoteScan:
    """What one note contributes: well-formed claims and markup problems."""

    doc: str
    claims: list[Claim]
    problems: list[Verdict]
    unparsed: bool
    declared: bool = False

    @property
    def has_evidence(self) -> bool:
        """The note declares evidence, well-formed or not (an empty list counts)."""
        return self.declared or bool(self.claims or self.problems)


def main() -> int:
    """Audit every claim under the given paths and print the verdicts."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path, default=[VAULT / "authored"])
    parser.add_argument("--workspace", type=Path, default=VAULT.parent)
    parser.add_argument("--json", action="store_true", help="one JSON object per line")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--target", choices=TARGETS, default="local")
    args = parser.parse_args()
    scans = [scan_note(f) for p in args.paths for f in markdown_files(p)]
    revisions = Revisions(args.workspace, args.target)
    verdicts = [v for s in scans for v in s.problems] + [
        check_claim(c, revisions) for s in scans for c in s.claims
    ]
    counts = summary_counts(scans, verdicts)
    for v in verdicts:
        print(json.dumps(asdict(v), ensure_ascii=False) if args.json else render(v))
    for repo, rev in sorted(revisions.resolved.items()):
        record = {"repo": repo, **asdict(rev)}
        line = f"revision|{repo}|{rev.label}|{rev.sha or rev.error}"
        print(json.dumps({"revision": record}) if args.json else line)
    print(json.dumps({"summary": counts}) if args.json else render_summary(counts))
    if not args.strict:
        return 0
    all_fresh = all(v.status == "unchanged" for v in verdicts)
    return 0 if verdicts and all_fresh else 1


def markdown_files(root: Path) -> list[Path]:
    """Every markdown file under root (or root itself)."""
    return [root] if root.is_file() else sorted(root.rglob("*.md"))


def scan_note(path: Path) -> NoteScan:
    """Parse one note's `evidence:` list, keeping broken markup as `invalid`."""
    doc = display_path(path)
    text = path.read_text(encoding="utf-8")
    raw, meta, error = frontmatter(text)
    if error:
        declared = DECLARES_EVIDENCE.search(raw) is not None
        problems = [problem(doc, "<frontmatter>", error)] if declared else []
        return NoteScan(doc, [], problems, unparsed=True)
    entries = meta.get("evidence")
    if entries is None:
        return NoteScan(doc, [], [], unparsed=False)
    if not isinstance(entries, list):
        detail = f"evidence must be a list, got {type(entries).__name__}"
        return NoteScan(doc, [], [problem(doc, "<evidence>", detail)], False)
    closing_fence_onward = text[4 + len(raw) + 1 :]  # "---\n<body>"
    blocks = body_blocks(closing_fence_onward.partition("\n")[2])
    claims: list[Claim] = []
    problems: list[Verdict] = []
    for index, entry in enumerate(entries):
        parsed = parse_entry(doc, index, entry, blocks)
        if isinstance(parsed, Verdict):
            problems.append(parsed)
        elif parsed.id in {c.id for c in claims}:
            problems.append(problem(doc, parsed.id, "duplicate id in this note"))
        else:
            claims.append(parsed)
    return NoteScan(doc, claims, problems, unparsed=False, declared=True)


def parse_entry(
    doc: str, index: int, entry: object, blocks: dict[str, list[str]]
) -> Claim | Verdict:
    """One evidence entry as a Claim, or an `invalid` verdict saying why not."""
    if not isinstance(entry, dict):
        return problem(doc, f"#{index}", "entry must be a mapping")
    repo, path = str(entry.get("repo") or ""), str(entry.get("path") or "")
    claim_id = str(entry.get("id") or f"{repo}:{path}")
    anchor = entry.get("anchor")
    if not repo or not path:
        return problem(doc, claim_id, "entry needs both repo and path")
    parts = PurePosixPath(path).parts
    if path.startswith("/") or parts in ((), (".",)) or ".." in parts:
        return problem(doc, claim_id, f"path {path!r} must name a file in the repo")
    if anchor is not None and not isinstance(anchor, str):
        return problem(doc, claim_id, "anchor must be a string")
    scope = entry.get("scope")
    if scope is not None and scope not in SCOPES:
        return problem(doc, claim_id, f"scope must be one of {', '.join(SCOPES)}")
    if scope == "anchor" and not anchor:
        return problem(doc, claim_id, "scope: anchor needs an anchor")
    block = str(entry.get("claim") or "").removeprefix("^")
    if not block:
        return problem(doc, claim_id, "entry needs `claim`: a block id in the body")
    found = blocks.get(block, [])
    if len(found) != 1:
        where = "not found" if not found else f"occurs {len(found)} times"
        return problem(doc, claim_id, f"claim block ^{block} {where} in the body")
    baseline = entry.get("baseline")
    base = str(baseline) if baseline else None
    return Claim(doc, claim_id, repo, path, anchor, base, block, found[0], scope)


def body_blocks(body: str) -> dict[str, list[str]]:
    """Text of every `^id`-marked paragraph or list item, keyed by block id.

    Fenced code is skipped. A block runs up from its marker line to the nearest
    blank line, heading or code line (exclusive) or list-item start (inclusive).
    """
    lines = body.splitlines()
    code = code_lines(lines)
    blocks: dict[str, list[str]] = {}
    for index, line in enumerate(lines):
        marker = None if code[index] else BLOCK_MARKER.search(line)
        if marker:
            text = block_text(lines, code, index, marker.start())
            blocks.setdefault(marker.group(1), []).append(text)
    return blocks


def code_lines(lines: list[str]) -> list[bool]:
    """Which lines belong to fenced code, fences included (CommonMark rules).

    A fence closes only with the same character, at least as long, and no info
    string; an unclosed fence runs to the end of the note.
    """
    flags: list[bool] = []
    opener: str | None = None
    for line in lines:
        fence = FENCE.match(line)
        if opener is None:
            if fence and not (fence[1][0] == "`" and "`" in fence[2]):
                opener = fence[1]
            flags.append(opener is not None)
            continue
        flags.append(True)
        closes = fence and fence[1][0] == opener[0] and len(fence[1]) >= len(opener)
        if closes and fence and not fence[2].strip():
            opener = None
    return flags


def block_text(lines: list[str], code: list[bool], end: int, cut: int) -> str:
    """The block ending at line `end` (marker at column `cut`), on one line."""
    start = end
    while start > 0 and not BLOCK_START.match(lines[start]):
        above = lines[start - 1]
        if code[start - 1] or not above.strip() or above.lstrip().startswith("#"):
            break
        start -= 1
    parts = [*lines[start:end], lines[end][:cut]]
    return " ".join(part.strip() for part in parts).strip()


def frontmatter(text: str) -> tuple[str, dict, str | None]:
    """(raw block, parsed mapping, error) for the leading `---` fences.

    A note without frontmatter is not an error: it simply declares nothing.
    """
    if not text.startswith("---\n"):
        return "", {}, None
    end = text.find("\n---", 4)
    if end == -1:
        return text[4:], {}, "frontmatter fence is not closed"
    raw = text[4:end]
    try:
        meta = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return raw, {}, f"frontmatter is not valid YAML: {one_line(exc)}"
    if meta is None:
        return raw, {}, None
    if not isinstance(meta, dict):
        return raw, {}, f"frontmatter is a {type(meta).__name__}, not a mapping"
    return raw, meta, None


def check_claim(claim: Claim, revisions: Revisions) -> Verdict:
    """Compare the claim's evidence at its baseline and at the target revision."""
    rev = revisions.get(claim.repo)
    if rev.sha is None:
        return verdict(claim, "unverified", rev.error or "no revision", rev)
    repo, at = revisions.workspace / claim.repo, rev.label
    kind = git(repo, "cat-file", "-t", f"{rev.sha}:{claim.path}")
    if kind is None:
        return verdict(claim, "missing", f"path absent at {at}", rev)
    if kind != "blob":
        return verdict(claim, "invalid", f"path is a {kind} at {at}, not a file", rev)
    now = git(repo, "show", f"{rev.sha}:{claim.path}") or ""
    if claim.anchor and now.count(claim.anchor) != 1:
        found = now.count(claim.anchor)
        status = "missing" if found == 0 else "unverified"
        return verdict(claim, status, f"anchor occurs {found} times at {at}", rev)
    if not claim.baseline:
        detail = f"no baseline; {at} is {rev.sha[:7]}"
        return verdict(claim, "unverified", detail, rev)
    then = None
    if git(repo, "cat-file", "-t", f"{claim.baseline}:{claim.path}") == "blob":
        then = git(repo, "show", f"{claim.baseline}:{claim.path}")
    if then is None:
        detail = f"baseline {claim.baseline} unknown or no such file there"
        return verdict(claim, "unverified", detail, rev)
    if claim.anchor and then.count(claim.anchor) != 1:
        found = then.count(claim.anchor)
        detail = f"anchor occurs {found} times at baseline {claim.baseline}"
        return verdict(claim, "unverified", detail, rev)
    by_window = claim.effective_scope == "anchor"
    if by_window:
        same = window(then, claim.anchor) == window(now, claim.anchor)
    else:
        same = then == now
    scope = "anchor window" if by_window else "file"
    if same:
        return verdict(claim, "unchanged", f"{scope} same since {claim.baseline}", rev)
    span = f"{claim.baseline}..{rev.sha[:7]}"
    return verdict(claim, "changed", f"{scope} differs {span}", rev)


def resolve(repo: Path, target: str) -> Revision:
    """Pin `repo` to one full SHA for this run (fetching first when published)."""
    if not (repo / ".git").exists():
        return Revision(target, None, f"no checkout at {repo}")
    if target == "local":
        branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
        label = f"HEAD ({'detached' if branch in (None, 'HEAD') else branch})"
        return Revision(label, git(repo, "rev-parse", "HEAD"))
    ref = git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if ref is None:
        return Revision("published", None, "unknown default branch: no origin/HEAD")
    if git(repo, "fetch", "--quiet", "origin", ref.removeprefix("origin/")) is None:
        return Revision(ref, None, f"fetch of {ref} failed; not reading a stale ref")
    return Revision(ref, git(repo, "rev-parse", ref))


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


def verdict(claim: Claim, status: str, detail: str, rev: Revision) -> Verdict:
    """Build a verdict carrying the claim's identity and the revision read."""
    return Verdict(
        claim.doc,
        claim.id,
        claim.repo,
        claim.path,
        status,
        detail,
        rev.sha,
        claim.block,
        claim.statement,
        rev.label,
    )


def problem(doc: str, claim_id: str, detail: str) -> Verdict:
    """An `invalid` verdict for markup that could not become a claim."""
    return Verdict(doc, claim_id, "", "", "invalid", detail, None)


def one_line(exc: Exception) -> str:
    """An exception message squeezed onto one line."""
    return " ".join(str(exc).split())


def render(v: Verdict) -> str:
    """One pipe-separated line per claim, plus the statement when it needs a look."""
    line = f"{v.status}|{v.doc}|{v.id}|{v.repo}/{v.path}|{v.detail}"
    if v.status == "unchanged" or not v.block:
        return line
    return f"{line}\n    ^{v.block}: {v.statement}"


def summary_counts(scans: list[NoteScan], verdicts: list[Verdict]) -> dict[str, int]:
    """Counts per status (stable order) followed by coverage counts."""
    counts = {s: sum(v.status == s for v in verdicts) for s in STATUSES}
    counts["notes"] = len(scans)
    counts["with_evidence"] = sum(s.has_evidence for s in scans)
    counts["unparsed_frontmatter"] = sum(s.unparsed for s in scans)
    return counts


def render_summary(counts: dict[str, int]) -> str:
    """The pipe-separated summary line."""
    return "summary|" + " ".join(f"{k}={n}" for k, n in counts.items())


def display_path(path: Path) -> str:
    """Path relative to the vault when possible."""
    try:
        return str(path.resolve().relative_to(VAULT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    sys.exit(main())
