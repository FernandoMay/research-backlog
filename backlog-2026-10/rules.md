# Backlog Rules

These rules are binding for every file under `research-backlog/`. They exist because a wrong number in a submission backlog costs a paper, and a confident wrong state costs credibility.

## 1. No dual submission

A manuscript already under review elsewhere cannot be submitted concurrently. Before writing `In submission workflow` for any item, confirm the same manuscript is not live at another venue. If it is, one of the two must be withdrawn first.

## 2. Use only these five statuses

| Status | Use when |
|---|---|
| `Proposed` | Draft only. Never submitted anywhere. |
| `In submission workflow` | Submitted, awaiting a decision. Requires a real submission link per rule 4. |
| `Revision in progress` | A decision was received and a revision is being written. |
| `User-asserted` | The user stated an action happened, but no receipt evidence exists on file. |
| `Accepted` | Accepted, with a recorded decision artifact. |

Never invent intermediate states. Never write `Accepted` from a user statement alone; that requires `User-asserted` until a decision artifact exists.

## 3. No number without a reproducible run

Never publish a number that is not reproducible from a linked current run. Any unverified figure stays in a blocked-claims table, reproduced verbatim from its source, with its evidence status and its required evidence intact.

Blocked claims must not be restated as results, and must not be reworded in a way that reads as achieved.

## 4. A submission link is a real handle

A submission link means a real recorded handle or URL: the portal URL plus the order or manuscript number.

A "we should submit here" URL is not a submission link. A conference's own CFP page is not a submission link. If no order or manuscript number exists, the field is `TBD`.

## 5. TBD means not found, and names the search

`TBD` means not found. The record must name what was searched and, where relevant, what the lookup returned.

Write `TBD — not found as of YYYY-MM-DD` and list the sources tried. Never let a bare `TBD` stand in for a lookup that was never performed.

## Evidence discipline

| Requirement | Rule |
|---|---|
| Dates, URLs, venue names, deadlines | Must come from a page actually retrieved, and carry the source URL plus the retrieval date |
| Never invent | Deadlines, submission IDs, acceptance states, venue expansions, URLs |
| Prefer official sources | Official conference sites, official submission portals, official CFP pages |
| Aggregators | WikiCFP, conference-index, myhuiban, mlscientist, blog posts are third-party. Label them as such and mark them unverified |
| Conflicting sources | Record all values, name each source, and prefer the official one. Do not silently pick |
| Tool failure | If a fetch fails, write the TBD and say the lookup failed. Never substitute recalled knowledge |

An honest `TBD` is always better than a plausible guess.

## Ambiguary handling

When an acronym maps to more than one distinct venue, record **all** verified matches with official URL, exact expansion, next deadline, and a one-line fit note. Mark the acronym as ambiguous. Do not silently pick one.

## Scope

| Boundary | Value |
|---|---|
| Files that may be created or edited | Anything under `/Users/fmf/Documents/research-backlog/` only |
| Surviving file that must not be modified | `STRATEGIC-DRAFTS-AUDIT-2026-09-15.md` |
| Repositories that are off-limits | `Almond`, `DSLBank`, `dsl-bank`, `game_king_suite` |
| Prohibited artifacts | `openspec/`, SDD artifacts, engram topics |
