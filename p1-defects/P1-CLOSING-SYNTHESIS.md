# P1 Closing Synthesis

**Status: COMPLETE — 7 packages adjudicated, 0 open items.**
Corpus: `p1-defects/corpus/` · Manifest: `corpus/MANIFEST.md` ·
Instrument audit: `corpus/P1-INSTRUMENT-DEFECTS.md`.

---

## 1. Why there is no aggregate score

The seven packages differ in population, granularity, category and in what their own
manuscripts chose to disclose. Collapsing them into "X% of claims valid" would
manufacture a comparability the data does not support, and it would reward a package
for having fewer claims.

**The aggregate worth having is structural.**

| package | artifact reproduces? | defect location | R1 | R2 | R3 |
|---|---|---|---|---|---|
| LEO | yes | the function that computes them (NSGA-II arm) | several | ablation design | provenance |
| ISAC | yes | the instrument (population, CRLB, correspondence) | several | estimator | nomenclature |
| CRL | yes | the instrument, plus an absent experiment | 0 | 1 | 2 |
| Quantum | JSON byte-identical | mostly the document; PNGs not environment-reproducible | 0 | 2 | 8 |
| i01 | yes | document framing and provenance | **0** | 2 | 8 |
| QCE | yes | attribution, two arms, a reference kernel | 2 + 1 trivial | 3 | 6 |
| SGN | yes via `main()` only | two arms without verifiable ground truth; described detector unused | 1 | 3 | 6 |

Three structural facts fall out of that table, and none of them is a score:

1. **i01 and Quantum have an empty R1 column.** Every mechanism their manuscripts
   describe is present in the code. Both packages' defects are in what the sentences
   say relative to what the code does. This is a *different failure mode* from LEO's,
   where the function computing the numbers did not implement the declared mechanism.
2. **QCE's artifact is the most solid of the seven and still has three R2/R3 items
   concentrated in experimental identity.** A sound artifact does not imply a sound
   experimental design.
3. **Only CRL and Quantum show a mechanism that is causal but whose *benefit* is
   unidentifiable.** That is a third category again: neither wrong nor right, but not
   demonstrable with the instrument built.

These are profiles, not rankings. Preserving the difference between them is the point.

---

## 2. The methodological result

> **Auditing does not end at finding discrepancies in the object. The falsification
> instrument must be shown able to produce, detect and propagate both failure and
> non-failure states.**

Everything else in P1 follows from that, including the parts that went wrong.

**The instrument failed on itself, repeatedly, and the failures were propagated rather
than cleaned.** Ten classes of instrument defect are retained in
`P1-INSTRUMENT-DEFECTS.md`. The four that most changed the method:

### A1 — No-effect ≠ dead

QCE-1's positive control intervened on the learning rate — causal in general — and
moved nothing. Investigating that produced the deepest finding in QCE: the trained
predictor emits a constant `0.150039`, so it selects one risk level for all 200 steps.

A variable **can sit on the causal path and still have no effect on a given outcome.**
An intervention test asking only "did the result change?" cannot distinguish *"this is
dead"* from *"this cannot matter given the state the system is in."* The second needs
an emission diagnostic.

### A2 — A favourable hypothesis deserves the same discipline

Before QCE-2 I hypothesised the temperature policy would also always select risk 0.1 —
which would have **exonerated** the package — and wrote the concluding lines before
measuring. The measurement refuted the premise.

An auditor who demands evidence before reporting a defect will often accept a
favourable explanation without measuring it. The asymmetry is the danger, not the
finding.

### A5 — Four hardcoded conclusions printed beside measurements

Including two that would have been **favourable to the package under audit**. A
hardcoded conclusion is not absent — it is present, confident, and adjacent to a real
measurement, so it survives a skim.

```
hypothesis → measurement → comparison → verdict
```

never `hypothesis → expected verdict → print(expected verdict)`.

### A6/A4 — Gates are instruments too

The gate found defects in its own package on first execution: Quantum rejected **2 of 6
falsifiers**, one of them a claim checker that had never agreed with anything. SGN's
gate had a **false-green path** — `CLEAN TREE` printed PROBLEM without appending to
`failures`, so the gate could report PASSED with a red last line. And at SGN I reported
a `git push` as successful when it had pushed nothing (`A4`).

**A stage that can detect a problem but cannot block the verdict is not a gate stage.**
**A Git operation is verified against the remote, not against its exit status.**

---

## 3. The seven results, stated without aggregation

**LEO** — 21 claims, **1 survives as written**. Reproduces perfectly; the numbers are
faithful to code computing an unrelated function. Seven documented false greens, all
retained. Three RED transcripts permanently lost to a `tee` collision and recorded as
lost rather than reconstructed.

**ISAC** — 12 claims, **3 survive**. The paper's own two CRLB equations disagree by a
factor of **621** in standard deviation. An independent matched-filter estimator was
built to test independence rather than assumed. MIMO `>10 bps/Hz` coverage remains
**NOT VERIFIED**, explicitly not contradicted.

**CRL** — mechanism, causal access and activation **SUPPORTED**; equal exposure
established before comparing arms; the resilience **benefit is NOT SUPPORTED** by the
metric. Four of seven claims are the manuscript limiting itself, and all four are
accurate — stronger than its own evidence requires. Recorded so they are not averaged
away.

**Quantum** — 17 claims, **15 contradicted**, 1 unsupported, 1 correct. The artifact is
**byte-identical**; the five PNGs are not, and the difference is rendering environment,
not data. Eight of seventeen are R3: valid numbers, invalid document. The
random-initialisation disclosure is **accurate as written** and kept out of the average.

**i01** — **R1 = 0.** Three conservative sections are *more* cautious than the evidence
requires. The overclaim is **one sentence**, the conclusion. The R2 defect is objective
comparability, not pairing — and pairing is recorded as a **protected non-finding**
because the arms *are* paired.

**QCE** — 9 supported, 1 supported-by-disclosure. Artifact solid, numbers trace, both
languages disclose the mechanism. Defects concentrated in **attribution** (the power
saving is attributable to the safety floor, not to an optimizer preference), **two
ablation arms** and a **reference C kernel** that diverges by a material margin. Two
reconstructions beat the published result on both axes, recorded as observations
outside the comparison set.

**SGN** — the detection rates were not the finding. The finding is that **two of four
arms have no verifiable ground truth**, and that the manuscript describes a detector
the reported figure does not use. A hypothesis that the signal was plainly detectable
was **retracted**, then its retraction was **over-corrected**; the surviving conclusion
is narrower and is the one the evidence supports.

---

## 4. Open, and deliberately so

| item | status | why it stays open |
|---|---|---|
| ISAC MIMO `>10 bps/Hz` | **NOT VERIFIED** | explicitly not contradicted; needs a coverage experiment that does not exist |
| CRL resilience benefit | **NOT SUPPORTED** | the mechanism is causal; the metric cannot resolve the benefit |
| SGN GAN_Enc / Adaptive_JND decoders | **not repaired** | C9 is the one repairable finding; changing it moves four published claims, so it is a manuscript decision |
| LEO and ISAC gates | **do not exist** | backfilling now would validate a corpus produced without one |
| The 0.963554 / 354.0291 mW observation | **outside every results table** | an exploratory intervention is not a published experiment |

---

## 5. What is preserved, and where

Everything is on its remote, verified with `ls-remote` rather than push output.

Durable copy at `p1-defects/corpus/`: **11** adjudications, **4** gate logs,
**26** falsifier logs including `LOST-AUDIT-EVIDENCE.md`, **30** falsifier and gate
sources, `MANIFEST.md`, `P1-INSTRUMENT-DEFECTS.md`.

**No manuscript text was edited in any package. No published number was corrected. No
historical figure was made a repair target. No repair was started.**

---

## 6. The boundary this close establishes

P1 is closed. The next phase — P1 repair where authorised, P2, or the P3 transition —
must not contaminate this corpus. The adjudications, the gates and the instrument
defects are the record of what was established; a repair changes the object, not the
record of its audit.

**Not repairing by inertia.** A green repair is not a true claim. A repair is validated
by restoring a pre-specified property, never by producing a number that matches a
published one.