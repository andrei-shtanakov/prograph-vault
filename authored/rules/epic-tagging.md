---
title: Epic tagging — one stream per artifact, on the first line or in the trailer block
type: rule
status: living
owner: Andrei
updated: 2026-08-25
---

# Epic tagging

`commit-pr-issue-granularity.md` says **which object** a piece of work becomes;
`cross-repo-waits.md` says how a dependency is recorded. This rule says **which stream** the
object belongs to — the axis introduced by
[[2026-08-25-adr-eco-010-epics-and-defect-classes]] and specified in
`authored/contracts/epics/v1/`.

The problem it exists for: in a polyrepo one stream of work lives in four to six repos at
once. Without a stream tag, an issue read an hour later is unattributable, and a weekly digest
grouped by repo renders one arc as several unrelated paragraphs.

---

## 1. One epic on everything you create

| You are writing… | Tag it |
|---|---|
| a `TODO.md` item | `@epic:<program>.<epic>` on the item's **first line** |
| a commit | `Epic: <program>.<epic>` in the final trailer block |
| a pull request | the same trailer, in the body |
| an issue | the same trailer, in the body |

Exactly one. Not a list, not two spellings of the same value — a duplicate is `EP-MULTIPLE`,
because an artifact counted in two streams double-counts in every aggregate.

The tag goes on the **same line** as `- [ ]` for plan items: the parser reads items line by
line and never sees continuation lines. This is the same trap `@owner`/`@blocked_by` already
have.

A commit that belongs to a pull request inherits that PR's epic — write the trailer once, in
the PR body. A direct commit with no PR (the umbrella repo, where policy has none) carries its
own trailer.

## 2. When the work is a fix, add the class

`@defect:<class>` / `Defect: <class>` — **only** on fixes, and never instead of the epic. A
bug found while working inside an epic carries both: the epic says where it happened, the
class says what broke. Tagging it with only the class would delete it from the "where do we
break most" count exactly when we are building most.

Classes are a closed set in the registry. Need a new one — add it to the registry in the same
pull request as the work that needs it.

## 3. The registry is the umbrella's `epics.toml`

`ai-orchestrators-workspace/epics.toml` holds the programs, the epics, the defect classes and
the coverage policy. It is read live, not vendored — it changes weekly.

- **The epic does not exist yet?** Add it to the registry first, by PR into the umbrella. An
  unregistered epic is `EP-UNKNOWN` (an error), and that is deliberate: it is the only thing
  standing between a typo and a silently split aggregate.
- **A program is `ecosystem` or `external`.** Work on a third-party product goes under its own
  program, so "our own platform" stays one filter away.
- **Background work is an epic**, not the absence of one: `eco.ops`, `airun.ops`, status
  `standing`.
- **Renaming an epic is not a rename.** The old id stays forever with `moved_to`; new work
  carrying it is `EP-MOVED`.

## 4. What you get, and what you do not

Aggregates by stream, by program, and by defect class — in dispatcher's epics view and as the
primary axis of Robin's digest.

What you do **not** get, so nobody hunts for it: **in the GitHub web UI an epic is findable
only by full-text search (`in:body`) — there is no clickable label filter.** v1 uses trailers,
not labels, because Robin reads git mirrors rather than the GitHub API, and a trailer in a
commit is countable with no GitHub access at all. Mirroring trailers into labels is a possible
later extension, not a gap to work around by inventing a second convention.

## 5. Exemptions live in one place

Merge commits, bot authors, vendored trees, and everything before `adopted_at` are exempt —
and only because `epics.toml` says so. An exemption you keep in your head is not an exemption;
it is a hole in the denominator, which is how "100 % coverage" becomes a number that depends
on who counts.

---

**Adoption:** `EP-MISSING` is a warning until the date in `[coverage_policy]`; the structural
errors (`EP-GRAMMAR`, `EP-UNKNOWN`, `EP-MULTIPLE`, `EP-MOVED`, `EP-DEFECT-*`, `EP-CONFLICT`)
block from the moment a validator exists. The transition period is for clearing old debt, not
for adding new ambiguity.
