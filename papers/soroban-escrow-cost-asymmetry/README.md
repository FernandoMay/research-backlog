# Auditing the Lifecycle, Not the Transaction

An ACM-format manuscript reporting an executed audit of a Soroban (Stellar)
token-escrow contract family. The audit found a systematic cost and control
asymmetry across the escrow lifecycle, and a test suite whose green status
overstates the authorization evidence it provides.

**Status:** manuscript source only. **Not compiled.** See
[Build status](#build-status).

---

## What the paper claims

Three findings, each traceable to an executed command or a committed artifact.

**F1 --- Lifecycle cost asymmetry.** `fund_escrow` cost 366,938 stroops and
`release_funds` cost 17,791 stroops in the same recorded lifecycle: a ratio of
20.6. Across the seven recorded steps, fees span 40.1x. The project's
documentation asserts a near-constant per-transaction cost; a single constant
cannot be approximately correct for a lifecycle whose own recorded fees span a
factor of 40.

**F2 --- One-sided dispute resolution.** `raise_dispute` is callable by buyer or
seller, so entry is symmetric. Resolution is not: in state `Disputed` both
`release_funds` and `refund_buyer` reject, and the only remaining transition
returns 100% of the amount to the buyer with no fee. There is no code path in
which a disputed escrow pays its seller.

**F3 --- Truncating fee arithmetic.** The fee is `floor(amount * bps / 10000)`
with no minimum-fee term, so it truncates to zero at small amounts. The
executed test asserts this directly: an amount of 1 base unit at 80 bps pays a
fee of 0 and the seller the full amount. The cap bounds the *rate* and the
contract has no floor on the *fee*.

**F4 --- Mocked authorization masks authorization coverage.** Every test calls
`env.mock_all_auths()`, under which `require_auth` succeeds for any caller. The
test named `test_unauthorized_refund` passes on a later caller-identity check,
not on an auth failure. No test in the family exercises a `require_auth`
rejection, and none asserts that `release_funds` rejects the seller.

The paper's contribution is the methodological claim that F1--F4 are one
finding: for Soroban escrow, the economically decisive and security-critical
behaviour sits in the transitions *between* operations, which per-operation
threat models and per-operation tests both miss.

## What the paper does NOT claim

Stated here because it is the part most likely to be misread from the abstract.

| Not claimed | Why |
|---|---|
| Settlement latency or speed | No timing instrumentation exists anywhere in the codebase. The README's "<3.5s median" has no measuring code behind it. |
| Cost savings, or "cheap" | No comparison against any published price for any payment rail exists. The README's economics figures are unsourced hardcoded constants. |
| A dollar figure for any fee | Converting stroops requires an XLM price and a date; neither is in the evidence. Fees are stated in stroops only. |
| Mainnet behaviour | All three escrow proofs are testnet. No mainnet deployment exists. |
| Throughput, durability, production readiness | None is instrumented. |
| An exploited attack | No penetration test, no adversary model, no formal verification. Section 8 is analysis. |
| A distribution of any measured value | n=1 per step. The ratio 20.6 is a ratio of two single observations. |
| Why the asymmetry exists | The recorded fee is an aggregate. No per-resource breakdown is in the evidence. |
| That the ratio holds on the current contract | The fee data was recorded against `CB7I2GUR...`; the README ships `CAFG7VWEN...` (v9) as current. |

## Numbers used in the paper

Every quantity in `main.tex` appears in the table below or is arithmetic over
it, with the arithmetic shown inline. There is no other source for numbers in
the manuscript.

| Quantity | Value | Source |
|---|---:|---|
| `fund_escrow` fee | 366,938 stroops | `E2E-PROOF.md:70-95`, ledger 4,869,217 |
| `release_funds` fee | 17,791 stroops | `E2E-PROOF.md:70-95`, ledger 4,869,223 |
| `create_escrow` fee | 164,691 stroops | `E2E-PROOF.md:70-95`, ledger 4,869,212 |
| S1/S2/S3/S4 fees | 183,215 / 14,202 / 14,202 / 9,140 | `E2E-PROOF.md:70-95` |
| fund / release ratio | 20.6x | derived, shown in Eq. 3 |
| fee span across lifecycle | 40.1x | derived, shown in Eq. 5 |
| lifecycle fee total | 770,179 stroops | derived, shown in Eq. 4 |
| `fund_escrow` share of that total | 47.6% | derived, shown in Eq. 5 |
| fund - release | 349,147 stroops | derived, shown inline |
| `MAX_FEE_BPS` | 1000 (10% cap) | `lib.rs:11` |
| `DEFAULT_FEE_BPS` | 80 (0.8%) | `tests.rs:12` |
| release of 1,000 units | fee 8, seller 992 | `tests.rs:193-196`, `:849-852` |
| release of 3,000 units | fee 24 | `tests.rs:794` |
| release of 1 unit | fee 0, seller 1 | `tests.rs:1082-1113` |
| zero-fee threshold at 80 bps | 124 base units | **derived** from formula + rate; only the 1-unit case is executed |
| cap boundary | 1000 bps accepted, 1001 -> `InvalidFee` | `tests.rs:921-963` |
| `EscrowError` variants | 10 | `lib.rs:15-33` |
| `test_snapshots` files | 26 | `contracts/contracts/escrow/test_snapshots/tests/` |
| `public/escrow.wasm` | 24,827 bytes | build artifact, **not committed** |

### Executed tests

| Repository | Command | Result |
|---|---|---|
| `breadline-protocol` | `cargo test` | 26 passed, 0 failed, 0.91s, soroban-sdk 26.1.1 |
| `proofdrop` | `npm test` | 38 passed, 0 failed (shared 8/8, api 30/30) |
| `pactopay` | `cargo test` | 8 passed, 0 failed, 0.63s, soroban-sdk 27.0.6 |
| `pactopay` | `npx vitest run` | **failed**: 9 of 11 files, 5 of 20 tests |
| `pactopay` | `npx playwright test` | **failed**: 8 failed, 4 skipped, 14 passed |
| `niko-sun-stellar` | not executed | toolchain time ceiling |

72 passing tests in total. `proofdrop` is 100% mocked, n=1, in-memory store. No
repository has a green CI run of record.

### Testnet escrow proofs

| Document | Contract | Asset | Amount | Date |
|---|---|---|---|---|
| `E2E-PROOF.md` | `CB7I2GUR...` | `BREAD`, self-issued, 7 dp | 20 BREAD (200,000,000) | 2026-09-25 |
| `E2E-USDC-PROOF.md` | `CBY6UC4I...` | Circle USDC | 5 USDC (50,000,000) | --- |
| `E2E-FEE-PROOF.md` | `CAFG7VWEN...` | Circle USDC | 0.05 USDC (500,000) | --- |

The fee data comes from the **first** contract, which is not the address the
README ships as current. See the `TODO(contract-version-alignment)` marker.

---

## Artifact provenance

| Artifact | Provenance | Byte-identity checkable? |
|---|---|---|
| `lib.rs`, `tests.rs` | source, cited by line number | yes |
| `E2E-PROOF.md` | fee table, lines 70-95 | yes |
| `E2E-USDC-PROOF.md` | escrow proof | yes |
| `E2E-FEE-PROOF.md` | escrow + fee proof, conservation check | yes |
| `test_snapshots/` | 26 committed JSON files | yes |
| `public/escrow.wasm` | 24,827 bytes, SHA-256 `a648e75a...a777d2c1` | **no** --- build artifact not committed |
| `README.md` | source of claims the audit falsifies | yes |
| `figures/data/lifecycle_fees.csv` | fee table, transcribed verbatim | yes |
| `figures/lifecycle_fees.pdf` | generated from the CSV | yes, via the script |
| `figures/make_figures.py` | figure + derivation checks | yes |

The full contract addresses, asset ids, and the complete SHA-256 are in
`main.tex` Section 12 (References).

---

## Reproduction

### Contract and application suites

```bash
cd breadline-protocol && cargo test      # 26 passed, 0 failed; sdk 26.1.1
cd proofdrop        && npm  test         # 38 passed, 0 failed
cd pactopay         && cargo test        # 8 passed, 0 failed;  sdk 27.0.6

# Reported as failures, not omitted
cd pactopay && npx vitest run            # failed: 9/11 files, 5/20 tests
cd pactopay && npx playwright test       # failed: 8 failed, 4 skipped, 14 passed
```

### Claims with no instrumentation behind them

```bash
# Four hits, all unrelated UI logic. No performance.now, elapsed, median, or p95.
grep -rniE "Date\.now|performance\.now|elapsed|median|p95" .
```

### Fee table

```bash
sed -n '70,95p' E2E-PROOF.md
```

### Figure and derivation checks

The figure is generated from a committed CSV. The script recomputes every
derived quantity in the paper and compares it against the artifact values
**before** writing output; it exits non-zero on any mismatch.

```bash
cd figures
python3 make_figures.py --verify   # print derivations, write nothing
python3 make_figures.py            # write lifecycle_fees.pdf
```

No dependencies beyond a Python 3 interpreter. The script emits vector PDF
using only the standard library, so it runs offline.

Expected `--verify` output:

```
  fund / release                 : 20.6249 -> 20.6x
  fund - release                 : 349,147 stroops
  lifecycle fee sum (n=1)        : 770,179 stroops
  fund share of that sum         : 47.6432%
  max / min across steps         : 40.1464 (S6 / S4)
  fee(1, 80bps)                  : 0
  largest zero-fee amount, 80bps : 124 base units

All derivation checks passed.
```

---

## Build status

**`main.tex` has not been compiled.** It is provided as source. A `pdflatex`
binary is present on the authoring machine at `/Library/TeX/texbin/pdflatex`,
so building it is a two-command operation:

```bash
pdflatex main.tex && pdflatex main.tex
```

What is unverified: page count, figure placement, table overflow, and
reference resolution. The source has been checked for balanced braces, properly
nested environments, no dangling cross-references, and no undeclared packages
(`amssymb`, `booktabs`, `listings` are declared explicitly in the preamble). No
successful compile has been observed.

---

## Files

| File | Purpose |
|---|---|
| `main.tex` | The manuscript. 12 sections, ACM `sigconf` format. |
| `REFERENCES-NOTES.md` | Every unsupported claim, why it is unsupported, and what would resolve it. 23 entries. |
| `README.md` | This file. |
| `figures/make_figures.py` | Dependency-free figure generator with built-in derivation checks. |
| `figures/data/lifecycle_fees.csv` | The seven-step fee table, transcribed verbatim. |
| `figures/lifecycle_fees.pdf` | Generated figure, referenced by the manuscript. |

## Open markers

`main.tex` contains 23 literal `TODO(<slug>)` markers. `REFERENCES-NOTES.md`
enumerates all of them with resolution cost. The cheapest high-value next step
is items 5, 15, 16, 17, and 19 from that file: under an hour, no testnet spend,
and five markers retired.

## Known weaknesses in this work

Stated plainly, because a reader should be able to find them here rather than
discover them in review.

1. **n=1 throughout.** The headline 20.6x is a ratio of two single
   observations. It is not an estimate with a confidence interval.
2. **Version drift.** The fee data is from `CB7I2GUR...`; the project ships
   `CAFG7VWEN...` (v9). F1's scope is version-limited and stated as such.
3. **No mechanism for F1.** The paper says which operation is expensive, not
   why, because no per-resource fee breakdown is in the evidence.
4. **No related work.** No literature was consulted. F4 in particular may be
   anticipated by prior work; that is a citation risk the manuscript flags
   rather than conceals.
5. **F2 depends on guards read at line-number granularity.** The audit
   established which operations reject in `Disputed` and which transition is
   reachable, but not the enclosing function of the authorization helpers.
6. **Thin artifact trail.** No adversarial testing, no formal verification, no
   green CI, no committed build artifact.
