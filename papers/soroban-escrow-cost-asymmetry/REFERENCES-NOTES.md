# REFERENCES-NOTES.md

Claims this paper **could not support**, and what each would take to resolve.

This file exists so that the gaps in `main.tex` are enumerable by a human
rather than implied by silence. Every entry is a claim a reviewer would
reasonably expect a paper in this area to make, that the audit materials do not
support, and that the manuscript therefore marks with a literal
`TODO(<slug>)` marker instead of asserting.

Rule applied throughout: a number enters the manuscript only if it appears in
the audit evidence or is arithmetic over evidence quantities with the
arithmetic shown inline. Where a number was wanted and did not exist, a marker
was left instead.

There are **24 markers** in `main.tex`. Each appears exactly once except
`related-work`, which is repeated in Sections 1 and 9 deliberately, so that
neither section can be read without noticing the gap.

---

## 1. The missing related-work section (structural)

**Gap.** The paper has no literature review and cites no external publication.

**Why.** No literature search was performed and no publication was available to
the audit. Inventing a plausible-looking citation would be worse than admitting
the gap, because a fabricated reference is undetectable by a reader who does
not already know the literature.

**Markers.** `TODO(related-work)` in Section 1 and again in Section 9.

**Resolution.** A real search across smart-contract escrow design, Soroban
resource and fee structure, and mock-based test-oracle validity. Roughly a
day of work. The three questions a related-work section must answer that this
manuscript currently cannot: (a) is the one-sided dispute resolution a known
anti-pattern with a published name; (b) has anyone characterised the
`mock_all_auths` blind spot in the literature, or is F4 novel; (c) how do other
platforms' escrow contracts price the lifecycle, so the F1 asymmetry has a
comparison point.

**Note.** Finding F4 is the one most likely to be anticipated by prior work.
That is a citation risk, not a correctness problem, and the search should
establish whether F4 is a contribution or a rediscovery before submission.

---

## 2. No currency conversion is possible

**Gap.** The paper states all fees in stroops and never in a fiat amount. The
repository's ``~$0.00001 per transaction'' is quoted only as a falsified claim.

**Why.** Converting stroops to a fiat amount requires an XLM/USD rate and a
date. Neither is in the audit materials. A conversion without a dated, sourced
rate is an invented number.

**Marker.** `TODO(stroop-fiat)`, Section 9.

**Resolution.** Record a rate and its source, with the date, in the artifact.

**Note.** F1 is deliberately constructed so it does **not** need this. The
falsification of a flat per-transaction figure is structural: a single constant
cannot be approximately correct for a lifecycle whose recorded fees span
40.1x. That argument holds without any currency conversion, and the paper
relies on it rather than inventing a rate to strengthen a point that does not
need it.

---

## 3. The 20.6x ratio has no mechanism

**Gap.** The paper states *which* operation is expensive and not *why*.

**Why.** The audit materials record an aggregate network fee per transaction
and do not decompose it into the resource classes that drive it. Naming a
cause (footprint, CPU budget, signature verification, rent) without a
per-resource breakdown would be a plausible-sounding guess.

**Marker.** `TODO(fee-resource-breakdown)`, Section 5.

**Resolution.** Per-resource fee breakdown for `fund_escrow` and
`release_funds`, from transaction simulation or resource metering. Probably a
few hours with the SDK.

**Note.** The paper's own wording hedges this correctly, but a reviewer will
push on it. A reader may reasonably suspect the obvious cause --- that funding
creates a trustline held by the contract while releasing operates on an
existing one. The paper does not assert this, and the TODO is what keeps the
distinction honest.

---

## 4. n = 1 everywhere

**Gap.** No distributions, no repeated trials, no confidence intervals. 20.6 is
the ratio of two single observations.

**Marker.** `TODO(fee-replication)`, Section 7 (F1).

**Resolution.** At least 30 repetitions per (amount, asset, address) for each
of the seven steps, reporting median and p95. Several hours plus testnet
fees. Until then no statement about typical or stable fee is admissible.

**Consequence if unresolved.** The paper says this plainly in Section 6 and
Section 9.1. It does not weaken any finding, because the findings are
structural properties of the recorded data. But it does mean F1's ratio must
be read as "in this recorded lifecycle", which is how the paper phrases it
everywhere it appears.

---

## 5. The measurement is on the wrong contract version

**Gap.** The fee data was recorded against `CB7I2GUR...`, while the README
ships `CAFG7VWEN...` as the current contract at version 9.

**Why this is important.** F1's headline ratio is a property of an *earlier*
address of the same family. It has not been re-measured against the artifact
the project currently points at.

**Markers.** `TODO(contract-version-alignment)` in Section 4, plus the
version-scope caveat inside F1 itself.

**Resolution.** Re-run the seven-step measurement against `CAFG7VWEN...` and
report both. Cheap to do; high value, because it converts F1 from
version-scoped to family-wide, or reveals that the asymmetry moved.

---

## 6. Testnet only

**Gap.** No mainnet behaviour, no real fee market, no real liquidity.

**Why.** No mainnet deployment exists in the audit materials. Testnet resource
pricing is not evidence of mainnet pricing.

**Marker.** `TODO(mainnet-fees)`, Section 7 (F1).

**Consequence if unresolved.** The paper confines every cost statement to
testnet and says so in Section 9.3. The ``Circle USDC'' proofs reference the
mainnet asset id but execute on a test network, which establishes nothing
about the mainnet asset; the paper says this explicitly.

---

## 7. No latency instrumentation exists

**Gap.** The paper reports no settlement latency, speed, or completion time.

**Why.** A search for `Date.now`, `performance.now`, `elapsed`, `median`, and
`p95` returns four hits, all in unrelated UI logic. The README's ``<3.5s
median testnet settlement'' has no measuring code behind it.

**Marker.** `TODO(latency-instrumentation)`, Section 9.

**Resolution.** A monotonic-clock harness emitting a per-stage JSON receipt,
aggregated over at least 30 lifecycles.

**Note.** The ledger column in the fee table is an *ordinal* sequence number.
It is tempting to read the 42-ledger span as a duration. It is not one, cannot
be converted to one from the available data, and the paper says so in the
table caption, the figure annotation, and the body text.

---

## 8. The per-user deployment path was never run

**Gap.** The path the application actually uses has no measured fee.

**Why.** `README.md:97` states it requires a wallet signature. It was never
executed during the audit.

**Marker.** `TODO(per-user-deploy)`, Section 9.

**Consequence if unresolved.** F1 is measured on an operator-side path. If the
per-user path has a different cost structure, F1's scope changes. The paper
flags this in Section 9.5.

---

## 9. No green CI of record

**Gap.** Suites were run locally on one machine at one moment.

**Marker.** `TODO(ci-baseline)`, Section 7.

**Consequence if unresolved.** "The test suite passes" is a statement about one
execution, not a property of the repository. The paper reports passing runs as
observed, and reports failing runs as failed, without reconciling them.

---

## 10. No adversary, no penetration test, no formal verification

**Gap.** Section 8 is analysis, not a threat model.

**Why.** No adversary was defined during the audit. A threat model requires
actor classes, their capabilities, and their incentives; none was provided.

**Marker.** `TODO(threat-model)`, Section 8.

**Consequence if unresolved.** The vectors T1-T4 are code properties, not
modelled attacks. The paper states this in the section's first paragraph and
must not be described as a threat model in a submission until an adversary
model exists.

---

## 11. Missing test coverage, stated but not filled

Three gaps are asserted in the paper without the corresponding tests existing.

| Marker | Location | What is missing |
|---|---|---|
| `TODO(negative-auth-test)` | F4 | Tests where `require_auth` can actually fail: `release_funds` and `refund_buyer` rejecting a non-party, and rejecting a correct party with no valid authorization. Without these, F4 stands as an observation about the suite, not a fixed defect. |
| `TODO(negative-auth-test-scan)` | F4 | A mechanical re-verification that *every* test calls `mock_all_auths`, so the claim is independently checkable rather than resting on a reading. |
| `TODO(dust-threshold-test)` | F3 | A sweep over amounts 0..200 asserting the fee at each. The paper currently *derives* the threshold of 124 base units from the formula; only the single-amount case at 1 base unit is executed. |
| `TODO(pactopay-liveness-tests)` | Section 8 (T2) | Any test for the two `pactopay` liveness defects: the absent deadline field and the `Disputed` milestone with no outgoing transition. |

All four are small changes to an existing suite. Until they exist, the paper is
correct to report them as absent rather than to imply coverage.

---

## 12. Source facts established only by line number

| Marker | Location | What is not established |
|---|---|---|
| `TODO(state-enum-enumeration)` | Table 1 | The full state type. Only `Funded` and `Disputed` are named; the states reached by `release_funds` and `refund_buyer` are unknown. Table 1 cannot be completed without reading the source. |
| `TODO(auth-helper-callgraph)` | Table 1 | Which function encloses `require_auth` (`lib.rs:231`) and the caller-identity check (`lib.rs:239`). Given only line numbers, the guard analysis in F2 and F4 is stated at the level the evidence supports and no further. |
| `TODO(deadline-clock)` | Table 1 | Whether the `auto_refund_if_expired` deadline is contract-stored or caller-supplied. This is material to F2: a caller-supplied deadline would change the shape of the extraction path. |
| `TODO(fee-proof-decomposition)` | Section 4 | The labels of the four terms in the `5.0624` conservation check. Until each term is identified, it cannot be checked against `MAX_FEE_BPS = 1000`, so the only real-asset fee proof does not confirm the cap is respected. |
| `TODO(usdc-decimals)` | Section 4 | Decimal precision of the `USDC` asset. 7 dp is established for `BREAD` only; without the `USDC` value the base-unit amounts cannot be read as whole units. |

---

## 13. Artifact and reference provenance

| Marker | Gap |
|---|---|
| `TODO(wasm-provenance)` | `contracts/target/.../escrow.wasm` is not committed, so the recorded 24,827-byte SHA-256 cannot be checked by a reader. Byte-identity of the deployed artifact is unverifiable from the repository. Commit the artifact, or publish a reproducible build with a pinned toolchain and lockfile. |
| `TODO(registry-provenance)` | The reference list names software artifacts by repository name, contract address, and version. Retrieval metadata for the SDK crates and the four repositories was not available and is not asserted. Every entry in Section 12 currently reads "retrieval URL not recorded by the audit", which is honest but not yet a resolvable citation. |
| `TODO(authorship)` | No author names, affiliations, or contact addresses were provided. The anonymous-submission form is used; no author metadata is invented. |

---

## 14. Economics claims deliberately not repeated

**Gap.** The paper does not state a cost saving, a comparison to any payment
rail, or the word "cheap" of this system.

**Why.** The repository's economics comparison (SWIFT \$45 flat + 5.9\%
spread, "85% cheaper") is unsourced hardcoded constants in the source. No
comparison against any published price for SWIFT, PayPal, SPEI, or PIX exists in
the audit materials.

**Marker.** `TODO(economics-baseline)`, Section 9.

**Resolution.** A cited, dated price for the comparator rail, plus a stated
currency conversion rate with its own source and date.

**Note.** These figures *are* quoted in the paper, twice, and in both places
only as claims the audit falsifies or declines to support. A reader who greps
for "85%" will find it in Section 9's limitations and in the reference entry
for the README. It appears nowhere as a result.

---

## 15. F2 may be a scoping defect rather than a design defect

**Gap.** The paper calls the one-sided dispute resolution a design defect.

**Why this is unresolved.** The honest counter-argument is that a symmetric
dispute path may have been out of scope for the deliverable. The repository
documents the behaviour as deliberate at `lib.rs:296-303`, which is consistent
with either reading: deliberate *as a scoping decision* and deliberate *as a
design choice* look identical in the source.

**Marker.** `TODO(dispute-exit)`, Section 7 (F2).

**Resolution.** Ask the project maintainers whether a seller-side resolution
path was planned and deferred. This is a question to a person, not a
measurement, and it cannot be settled from the repository. If the answer is
that it was deferred, F2 becomes a scoping defect and the paper should be
revised to say so -- though the underlying property of the transition relation
would be unchanged, and the README/code mismatch at `README.md:286` would
remain a defect either way.

**Consequence if unresolved.** F2 is stated as a property of the code, which is
what the evidence supports. The paper does not claim intent, and this marker
exists so a reader does not infer intent from the finding.

---

## Summary table

| # | Claim | Marker | Effort to resolve |
|---|---|---|---|
| 1 | Related work | `TODO(related-work)` | ~1 day, literature search |
| 2 | Currency conversion | `TODO(stroop-fiat)` | Minutes, once a rate is sourced |
| 3 | Mechanism of the 20.6x | `TODO(fee-resource-breakdown)` | Hours, resource metering |
| 4 | Repeat the fee measurement | `TODO(fee-replication)` | Hours + testnet fees |
| 5 | Re-measure on v9 | `TODO(contract-version-alignment)` | ~1 hour |
| 6 | Mainnet fees | `TODO(mainnet-fees)` | Blocked: no mainnet deployment |
| 7 | Settlement latency | `TODO(latency-instrumentation)` | ~1 day, instrument and aggregate |
| 8 | Per-user deploy path | `TODO(per-user-deploy)` | Hours |
| 9 | Green CI | `TODO(ci-baseline)` | Hours, config + run records |
| 10 | Adversary model | `TODO(threat-model)` | ~1 day, model definition |
| 11 | Authorization failure tests | `TODO(negative-auth-test)` | Hours |
| 12 | Mock coverage re-verification | `TODO(negative-auth-test-scan)` | Minutes, one grep |
| 13 | Dust threshold sweep | `TODO(dust-threshold-test)` | Minutes |
| 14 | Liveness defect tests | `TODO(pactopay-liveness-tests)` | Hours |
| 15 | Full state enumeration | `TODO(state-enum-enumeration)` | Minutes, read the source |
| 16 | Auth call graph | `TODO(auth-helper-callgraph)` | Minutes, read the source |
| 17 | Deadline clock source | `TODO(deadline-clock)` | Minutes, read the source |
| 18 | Fee-proof term labels | `TODO(fee-proof-decomposition)` | Minutes |
| 19 | USDC decimals | `TODO(usdc-decimals)` | Minutes |
| 20 | Wasm byte-identity | `TODO(wasm-provenance)` | Hours, reproducible build |
| 21 | Reference metadata | `TODO(registry-provenance)` | Minutes |
| 22 | Author block | `TODO(authorship)` | Minutes |
| 23 | Payment-rail price baseline | `TODO(economics-baseline)` | Hours, cited prices |
| 24 | F2 scoping vs design intent | `TODO(dispute-exit)` | A question to the maintainers |

**Cheapest high-value next step:** items 5, 15, 16, 17, and 19 together take
under an hour, require no testnet spend, and would let the paper drop five
markers and materially strengthen F2 and F3.
