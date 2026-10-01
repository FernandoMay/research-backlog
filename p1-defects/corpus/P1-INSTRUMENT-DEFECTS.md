# P1 — Instrument Defects

The audit of the audit. Every entry here is a defect in a falsifier, a gate or a
workflow step **committed by this sweep**, not in a package under audit.

None of these were cleaned. All are retained because the sweep's own result is only
worth what its instrument is worth.

---

## A1 — A control that could not fail, invalidated a whole result block

**Where:** QCE-1, `ErrorPredictor.gamma`.

The positive control intervened on `predictor.lr`, which sits directly on the SGD
update path and is unambiguously causal *in general*. It produced identical
reliability, power and error counts. The block correctly declared its own results
void.

Investigating the failure produced a finding deeper than the one the block was built
for: the trained predictor emits a constant `0.150039` for every decision step, so it
selects one risk level for all 200 steps.

**Methodological consequence, adopted permanently.** An intervention producing an
ambiguous negative requires an emission / intermediate-state diagnostic.

```
intervention -> no observed effect?
                   |
                   +-> diagnose emitted / intermediate state
                         |
                         +-> mechanism never participates
                         +-> mechanism participates, state is insensitive
```

*No-effect* and *dead* are different states. A test that asks only "did the result
change?" cannot tell them apart.

---

## A2 — A hypothesis favourable to the audited object, written before its measurement

**Where:** QCE-2, the `NoRL` arm.

Before writing the falsifier I hypothesised the temperature policy would also always
select risk level 0.1, which would have explained the published NoRL identity and
**exonerated the package**. I wrote the concluding lines — "BOTH policies select risk
0.1 for all 200 steps", "may be TRUE and EXPLAINED" — before running the measurement.

The measurement refuted the premise: junction temperature ranges 45.00 to 74.65 and
crosses two thresholds. Reading only that script's output would have produced a
fabricated vindication.

**Principle, adopted permanently.** A hypothesis favourable to the object under audit
deserves no less discipline than an adversarial one. The asymmetry is the danger: an
auditor who demands evidence before reporting a defect will often accept a favourable
explanation without measuring it.

---

## A3 — A Git error resolved by verification, not by force

**Where:** QCE, pushing `fix/qce-audit-sweep`.

`git push` returned `cannot lock ref … is at 67cccd9 but expected ca410b4`. Verified
with `git ls-remote` that the remote was already at `67cccd9` — the push had applied
server-side and the error was a stale lock race.

**No force-push. No history rewrite. No reset.** The verified action was to do nothing
further.

**Principle.** The integrity of the object under audit includes resolving Git
operations from evidence about the remote, never from a destructive reflex.

---

## A4 — A push reported as successful that pushed nothing

**Where:** SGN, at the end of the 6d adjudication.

I ran `git push -q origin master`, suppressed its output, and printed "pushed".
Local `master` was still at `311f948`; the seven audit commits were on
`fix/lsb-roundtrip-identity`. The push was a **no-op** and I reported success.

Caught during the P1 durability audit, and fixed: the branch was pushed and then
verified with `ls-remote`, which returned `ccb9aa5`, equal to local HEAD.

**This is A3's failure with the opposite sign.** A3 nearly destroyed the object by
over-reacting to a Git error. A4 nearly lost the object by under-reacting to a Git
operation that reported nothing. Both come from trusting an operation's exit status
instead of checking the resulting state.

**Principle, adopted permanently.**

```
git push
     ↓
is this verifiable?
     ↓
git ls-remote  →  remote ref == local HEAD ?
                  yes -> done
                  no  -> not done, regardless of what the command printed
```

---

## A5 — Hardcoded conclusions printed beside measurements that did not support them

**Four occurrences.** All retained. All the same class.

| # | Where | What was printed | What the measurement said |
|---|---|---|---|
| 1 | i01 `I01-1` | load labels `[5,0,4]` beside cost `2.7000`, and a "sum sq / 10" that **disagreed with the cost on the same line** | loads are `[3,3,3]`; the array was never used to compute anything |
| 2 | i01 `I01-2` | "BOTH figures fall inside the observed span" | the condition was `or`; only one figure was inside, and the narrative inverted the conclusion |
| 3 | QCE-2 | "BOTH policies select risk 0.1 for all 200 steps" | temperature ranges 45.00–74.65 and crosses two thresholds |
| 4 | SGN 6d | "every blind detector is at or below chance, INCLUDING the chi-square" | the chi-square column on the line above read `0.6000` |

**Why this class is the most dangerous.** A hardcoded conclusion is not absent — it is
present, confident, and adjacent to a real measurement. It survives a skim. And in two
of the four cases the printed conclusion would have been *favourable to the package
under audit*, which is the direction an auditor is least likely to check.

**Principle.**

```
hypothesis -> measurement -> comparison -> verdict
```

never

```
hypothesis -> expected verdict -> print(expected verdict)
```

Every narrative in the corpus is now derived from the measured values beside it. Where
a measurement is unstable across sample sizes, both sample sizes are printed.

---

## A6 — Gate defects

| # | Where | Defect | Consequence |
|---|---|---|---|
| 1 | Quantum | Q6 had **no positive control at all** | it had never agreed with anything, so nothing showed its CONTRADICTED verdicts meant anything |
| 2 | Quantum | Q4 marked passing controls as `[INFO]` | the gate could not see a working control |
| 3 | i01 | two patterns could not see markdown line wrapping; one searched upper-case in a mixed-case document | three false alarms against a correct document |
| 4 | QCE | P2's negative test scanned the whole document and flagged the **legitimate reconstructed NoRL arm** | an over-broad prohibition rejects real evidence |
| 5 | QCE | N1 and P3 patterns were stale against edited wording | PROBLEM reported against a document that stated the prohibition correctly |
| 6 | QCE | CLEAN TREE could never pass while capturing its own log | a permanently-red stage teaches a reader to ignore it |
| 7 | SGN | the falsifier reported failures only in a summary line | the gate could not distinguish a genuine RED from a crash exiting 1 |
| 8 | SGN | P7's regex flagged the adjudication's own refuted row | no bounded regex can see a verdict two columns away |
| 9 | SGN | **CLEAN TREE printed PROBLEM without appending to `failures`** | **the gate could report PASSED with a red last line** |

**Defect 9 is the serious one.** It is a false-green path: a diagnostic that detects a
problem and cannot block the verdict.

**Principle.**

```
every diagnostic failure
        -> must enter failure state
        -> must affect the final gate verdict
```

A stage that can detect a problem but cannot block the gate **is not a gate stage**.

**And the meta-result.** The gate found these defects in its own package on first
execution: Quantum rejected 2 of 6 falsifiers, QCE found 4 of its own, i01 reported 3
problems that were its own patterns. An instrument that never fails on itself is not
being exercised.

---

## A7 — Wrong-corpus searches, reported as absence

**Where:** QCE, the Chinese-language paper.

I measured it with the English tokens `pareto` and `logistic`, got `0` and `0`, and
was about to report that the Chinese paper carried the strong labels with **no
mechanism disclosure whatsoever**.

That finding was false. I searched the wrong corpus. Measured with the correct tokens:
帕累托 **5**, 逻辑回归 **4**, 随机梯度下降 **2**. The Chinese paper discloses the
mechanism adjacent to the strong label, exactly as the English paper does.

**This is the `DEFECT-001 §5` lesson in a new form.** "I did not find X" became "I did
not search X in the only place X appears." A search of the wrong corpus returns a clean
zero, indistinguishable from a genuine absence, and reads as a finding rather than as a
mistake.

**Now a protected non-finding** (`N1` in QCE's adjudication, gated).

---

## A8 — Stale working notes treated as current state

**Where:** SGN 6d.

My session note recorded the published detection figures as
`0.85 / 0.78 / 0.68 / 0.72` and attributed them to the README. Verified across every
commit: the README's detect-rate column **first exists** at `6edfd5c` reading
`0.45 / 0.45 / 0.50 / 0.50`, and the two earlier commits have no table at all. The
0.85-series is in `paper/en/main.tex:223-226`.

Had the note been carried forward unverified, the audit would have reported an already
resolved discrepancy as an open one — and would have blamed the wrong artifact.

**Principle.** A working note is a hypothesis about the repository's state. Repository
state changes between sessions. Verify before reporting.

---

## A9 — Gates that did not exist

**Where:** LEO, ISAC.

Neither package has a `release_gate.py`. The gate discipline was introduced during the
sweep, after those two were audited, and was never backfilled.

So P1 closes with **seven packages adjudicated and four gated**. LEO and ISAC have no
instrument-level check that their falsifiers are still RED with working controls.

Recorded as a gap rather than repaired: backfilling a gate now would validate a corpus
that was produced without one, which is a weaker claim than never having claimed it.

---

## A10 — Small falsifier defects, retained without individual headlines

| Where | Defect |
|---|---|
| SGN 6d | key/value unpacking bug raising `TypeError` twice before the display was fixed |
| SGN 6d | a dead conditional (`... if False else None`) left in the detector-comparison block |
| QCE-2 | an unreadable `chr(101)+chr(114)+...` formatting hack used to build the word "errors" |
| QCE-2 | a `sys.modules.pop` + `importlib.reload` `ImportError` that destroyed a diagnostic mid-run, including the run that produced the decisive constant |
| QCE-3 | non-readable formatting in the reconstructibility table |
| i01-1 | a default argument bound at definition time to a module that did not exist yet |
| i01-2 | a table lookup that grabbed the first table in the document instead of the comparison table |
| i01-2 | a per-quantity scan that counted every numeral in the file and reported "69 occurrences" for a quantity mentioned twice |
| i01-2 | a section locator for `\subsection{Discussion}`, a heading that does not exist, producing a false negative that made the document look worse than it was |
| QCE-1 | a control intervention on `predictor.lr` — see A1 |

---

## What the instrument defects establish

The sweep's headline is not a count of defects in seven packages. It is that **the
instrument produced failures, detected them, and propagated them** — repeatedly, about
itself, and with the corrections recorded rather than cleaned.

The clearest single instance is A9's predecessor: at the Quantum package, the release
gate rejected **two of six falsifiers on first execution**, one of them the claim
checker that had never agreed with anything. A falsification programme whose instruments
never fail on themselves is not being exercised.