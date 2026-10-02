# SD-05 — Proof-Carrying AI Agents: Adaptive Cryptographic Verification of Autonomous Decision Traces

**Target:** AIBT 2026 — deadline **Oct 10, 2026**, verified at source (§0)
**Track:** Blockchain for AI → Trusted AI and Decentralized AI Systems (Track 4); Systems, Platforms and Experimental Studies (Track 6)
**Status:** **FROZEN.** Not submission-ready. Seven defects open, D1–D4 structural. Redesign must begin from falsifiers, not from the paper narrative.

---

## 0. Venue resolved; SD-05 frozen pending redesign

**Status: FROZEN. Not submission-ready. Not to be rebuilt against a paper narrative before the falsifiers exist.**

### 0.1 Venue — verified at source, 2026-10-02

| | AIBT 2026 |
|---|---|
| Official source | `aibt.net`, fetched directly |
| Submission deadline | **Oct 10, 2026 — 8 days** |
| Notification | Oct 25 |
| Camera-ready | Oct 30 |
| Event | Nov 27-29, Shanghai |
| Publisher | **ACM International Conference Proceedings Series**, Open Access |
| Indexing | Ei Compendex, Scopus |
| Review | Double blind |
| Full paper | 4-10 pages, extra pages charged above 5 |
| Abstract-only | 200-400 words |
| Co-sponsors | East China Normal University; Southwest Jiaotong University |

**The earlier "closed 17 days ago" reading is withdrawn.** It came from the repository's own stale `Sep 15 in invitation` record, which the official page contradicts. That discrepancy is retained in `CONFERENCE-MAP-2026-2027.md` as a fact, not resolved by fiat.

The **IEEE Xplore** claim from the inbox analysis does not survive: AIBT publishes in ACM ICPS.

### 0.2 ICCBN is not an alternative

ICCBN 2026's official submission deadline is **Oct 5 — 3 days**. The Oct 25 figure in the inbox analysis is the **notification** date. The alleged Oct 20 extension fails the venue's own internal consistency: it would leave 5 days for double-blind review before notification, with camera-ready on Oct 31.

**SD-04 Network Digital Twins cannot be built in 3 days.** ICCBN is recorded as effectively closed for this cycle.

### 0.3 Venue reputation — evidence moved, judgment not settled

`SECONDARY-SOURCE-gemini-conversation.md` §4.1 called AIBT a mass-mailing call from a predatory or vanity venue. That source endorsed AIBT in the same document, which is why it was never inherited.

Primary evidence now available: two named Chinese university co-sponsors, ACM ICPS, Ei Compendex and Scopus. This is materially inconsistent with the predatory description. **This is not a clearance.** Venue reputation is a judgment; one page does not settle it. But the alarm should not be repeated as if unexamined.

### 0.4 What is still unverified

Submission portal, template, and page limits for both venues. Only dates and publisher are PRIMARY_SOURCE.

---

## 1. Core thesis

Cryptographic attestation for autonomous agents should be an **adaptive, risk-driven** process. The cost of `on-chain` anchoring is paid only where the consequence justifies it, and skipped where it does not — without weakening non-repudiation of the execution trace.

This is a reasonable thesis. The mechanisms below do not yet implement it.

## 2. Agent Execution Receipt (AER) — Merkle structure

The AEMT models an agentic cycle as a balanced 5-leaf binary Merkle tree yielding a single `TraceRoot`.

```text
                       TraceRoot = SHA256( H_12 || H_345 )
                            /              \
                H_12 = SHA256              H_345 = SHA256
              ( H_M || H_P )               ( H_I || H_45 )
                 /       \                   /       \
              H_M         H_P             H_I       H_45 = SHA256
                                                         ( H_T || H_O )
                                                          /       \
                                                       H_T         H_O
```

Leaf definitions:

- `H_M = SHA256(Model_ID ‖ System_Prompt_Hash)`
- `H_P = SHA256(Policy_Rulesets ‖ Guardrail_Version)`
- `H_I = SHA256(User_Input ‖ Context_Commitment)`
- `H_T = SHA256(Tool_Signatures ‖ API_Version_Manifest)`
- `H_O = SHA256(Agent_Action_Payload ‖ Output_JSON)`

Conceptually sound. Two construction defects: **D4** and **D6** below.

## 3. Adaptive risk engine

$$r_i = \sigma\left(w_1 U_i + w_2 V_i + w_3 I_i + w_4 N_i + w_5 P_i + \gamma (U_i \cdot V_i)\right)$$

| Variable | Meaning |
|---|---|
| $U_i$ | **Uncertainty** — log-prob entropy or response variance |
| $V_i$ | **Value** — normalized value of resources committed |
| $I_i$ | **Impact** — severity, 0 = read-only, 1 = mutation or transfer |
| $N_i$ | **Novelty** — distance from historical semantic memory (OOD) |
| $P_i$ | **Policy sensitivity** — proximity to guardrail boundaries |

### Threshold policy

| Level | Condition | Mechanism | Stated overhead | Stated on-chain cost |
|---|---|---|---|---|
| $L_0$ | $r_i < 0.30$ | Local receipt, local chain | $< 1$ ms | $\$0.00$ |
| $L_1$ | $0.30 \le r_i < 0.65$ | Signed receipt, Ed25519, off-chain | $2\text{–}5$ ms | $\$0.00$ |
| $L_2$ | $0.65 \le r_i < 0.85$ | On-chain anchoring of `TraceRoot` (L2/Stellar) | $200\text{–}800$ ms | gas $\sim 10^{-5}$ USD |
| $L_3$ | $r_i \ge 0.85$ | Multi-party attestation, $k$-of-$n$ auditors | $1000\text{–}2500$ ms | multi-sig gas |

**The overhead and cost figures are unverified estimates with no measurement and no source** — see **D7**.

## 4. Prototype architecture

Three layers: FastAPI runtime (`LLM Agent → Risk Engine → Receipt Builder`), then off-chain storage for $L_0/L_1$ and smart-contract anchoring for $L_2/L_3$.

```text
┌─────────────────────────────────────────────────────────────┐
│                       FastAPI Runtime                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │ LLM Agent   │ ─► │ Risk Engine │ ─► │ Receipt Builder │  │
│  └─────────────┘    └─────────────┘    └────────┬────────┘  │
└─────────────────────────────────────────────────┼───────────┘
                     ┌───────────────────────────┴──────────┐
                     ▼                                      ▼
        Off-Chain Storage ($L_0$, $L_1$)        Smart Contract ($L_2$, $L_3$)
```

Contract (Soroban/Rust) and ingestion/verification script are reproduced in §7.

## 5. Adversary injection plan

| # | Attack | Perturbation | Expected result | Claimed detection |
|---|---|---|---|---|
| 1 | Model substitution | Declared model swapped for a local LLM | $H_M'$ distorts $H_{12}$ | `TraceRoot` check fails (**100%**) |
| 2 | Policy tampering | Guardrails disabled at runtime | $H_P'$ distorts $H_{12}$ | `TraceRoot` check fails (**100%**) |
| 3 | Input tampering | Original prompt modified | $H_I'$ distorts $H_{345}$ | `TraceRoot` check fails (**100%**) |
| 4 | Tool hijacking | Tool binary replaced | $H_T'$ distorts $H_{45}$ | `TraceRoot` check fails (**100%**) |
| 5 | Output tampering | Output JSON payload modified | $H_O'$ distorts $H_{45}$ | `TraceRoot` check fails (**100%**) |
| 6 | Replay | Prior `TraceRoot` replayed | Blocked by `timestamp` and key duplication | **Immediate rejection in the contract** |

**Rows 1–5 assert a result that cannot be false** — see **D3**. **Row 6 is not implemented** — see **D2**.

## 6. Open defects

Each was verified against the code in §7, not inferred from the prose.

### D1 — The risk formula is not the risk function *(R1: mechanism not implemented)*

Stated: $\sigma(\cdot)$, a sigmoid. Implemented: `min(max(raw_score, 0.0), 1.0)`, a **clamp**. These are different functions. A clamp reaches exactly 0.0 and 1.0; a sigmoid approaches them and never attains them.

Measured divergence between the stated formula and the pasted code:

| $U$ | $V$ | $I$ | $N$ | $P$ | code (clamp) | formula ($\sigma$) | $\lvert\Delta \rvert$ | level differs? |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0.2 | 0.85 | 0.90 | 0.10 | 0.20 | 0.6205 | 0.6503 | 0.0298 | no (both $L_2$) |
| 0.1 | 0.10 | 0.10 | 0.10 | 0.10 | 0.1015 | 0.5254 | **0.4239** | **yes** ($L_0$ vs $L_1$) |
| 0.9 | 0.90 | 0.90 | 0.50 | 0.90 | 0.9815 | 0.7274 | 0.2541 | **yes** ($L_3$ vs $L_2$) |
| 1.0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.0000 | 0.7595 | **0.2405** | **yes** ($L_3$ vs $L_2$) |

Two consequences:

1. **The worked example masks the defect.** The single worked case in §7 lands at 0.6205 vs 0.6503 — both $L_2$. A reader checking the example sees agreement and concludes the code matches the math.
2. **$\gamma$ is hardcoded to `0.15`** in the code while the math carries it as a free parameter with no stated value.

Either the prose or the code is wrong. Both cannot stand.

### D2 — Replay protection is claimed and absent *(R1)*

Matrix row 6 promises "Immediate rejection in the Smart Contract". The contract does not do this:

```rust
pub fn anchor_execution(env: Env, agent_id: Address, trace_root: BytesN<32>, risk_score_bp: u32) {
    // no duplicate check, no nonce, no expiry
    env.storage().persistent().set(&key, &timestamp);
}
pub fn verify_execution(env: Env, agent_id: Address, trace_root: BytesN<32>) -> bool {
    env.storage().persistent().has(&key)   // true for ANY previously anchored root
}
```

Replaying an already-anchored `TraceRoot` returns **true**. Re-anchoring simply overwrites the timestamp. There is no nonce, no expiry, no consumed-state. **The claimed security property is not implemented.**

### D3 — The adversary matrix cannot fail *(R2: unidentifiable experiment)*

**Instrument category: `NON-DISCRIMINATING-FALSIFIER`.** This is stronger than "a weak test". A non-discriminating falsifier is one where the tested property cannot take the failing value. It is recorded here as a distinct class, because P1's `R2` understates what goes wrong: an R2 defect may still fail sometimes, whereas this suite cannot fail **at all**.

Rows 1–5 all predict `TraceRoot` check failure at **100%**. That is true by construction: SHA-256 is preimage-resistant, so changing any leaf necessarily changes the root. Formally:

```text
for every perturbation p in {1..5}:
    PASS(p)  ==  "hash changed"
```

`PASS` is a tautology over a property of SHA-256, not evidence about the system under test. `test_tamper_detection.py` asserting 100% detection therefore certifies that hash functions work. **A stage that cannot produce a negative result cannot gate anything** — it can only be reported as PASS, so reporting it as anything else requires overriding the instrument.

The property that actually matters, and that this suite never touches, is the **policy**:

```text
high-impact action
        ↓
   risk engine
        ↓
     r < 0.30
        ↓
       L0
        ↓
no signature · no anchor · zero cost · no on-chain trace
```

Can an attacker construct an action that the risk engine scores below 0.30 — receiving $L_0$, no signature, no anchoring, no permanent trace — while being genuinely high-impact? That falsifies the **security policy**, which is a different property from cryptographic resistance, and it requires no hash collision whatsoever. It is the test that can fail, and therefore the only one whose PASS means anything.

### D4 — No domain separation in the Merkle construction

`leaf(x) = SHA256(x)` and `node(l, r) = SHA256(l ‖ r)` are the **same operation** with no prefix. A leaf's input text can therefore be reinterpreted as an internal node.

Bounded precisely, because the strength of the claim matters: this is **domain ambiguity, not a SHA-256 collision**. Constructing a genuine collision was verified as infeasible in this review. The defect is that a verifier cannot tell which role a hashed value played.

Secondary: hashes are composed as **hex strings** rather than raw 32-byte digests, doubling both the domain ambiguity and the input length.

Standard fix: domain-separate the leaves — `SHA256(0x00 ‖ leaf)`, `SHA256(0x01 ‖ l ‖ r)` — over raw bytes.

### D5 — Address format is internally inconsistent

```json
"agent_id": "did:agent:stellar:0x8f3a..."
```

The DID names **Stellar**; the payload is **EVM** hex; the contract is **Soroban**, whose `Address` is a StrKey beginning `G`. Three components, three conventions. `0x8f3a…` is also a truncated literal that would not compile as written.

### D6 — A placeholder is presented as a computed value

`model_hash` in the §7 JSON is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. That is `SHA256("")`, the empty-string digest. Under the pasted code, `sha256(model_id.encode())` produces it **if and only if `model_id == ""`**.

Either the example was generated with an empty `model_id`, or it is a copied placeholder. It is not a hash of any model.

### D7 — Cost and latency figures are unmeasured

`< 1 ms`, `2–5 ms`, `200–800 ms`, `1000–2500 ms`, `~10⁻⁵ USD`. No measurement, no environment, no reference. `metrics.json` appears in §8 as a **planned** artifact; it does not exist.

These must not appear in any results table. An exploratory figure outside every results table is acceptable; an unmeasured estimate inside one is not.

## 7. Code as submitted for review

```python
class AgentExecutionReceipt:
    def _hash_leaf(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()
    def _hash_node(self, left: str, right: str) -> str:
        return hashlib.sha256((left + right).encode()).hexdigest()   # D4: no domain separation

class AdaptiveRiskEngine:
    def compute_risk(self, u, v, i, n, p):
        raw_score = (self.w[0]*u + self.w[1]*v + self.w[2]*i + self.w[3]*n + self.w[4]*p) + (0.15 * u * v)
        return min(max(raw_score, 0.0), 1.0)                          # D1: clamp, not sigmoid
```

```rust
pub fn anchor_execution(env: Env, agent_id: Address, trace_root: BytesN<32>, risk_score_bp: u32) {
    agent_id.require_auth();
    let key = (agent_id.clone(), trace_root.clone());
    let timestamp = env.ledger().timestamp();
    env.storage().persistent().set(&key, &timestamp);                // D2: no replay defence
    env.events().publish((Symbol::new(&env, "execution_anchored"), agent_id),
                         (trace_root, risk_score_bp, timestamp));
}
pub fn verify_execution(env: Env, agent_id: Address, trace_root: BytesN<32>) -> bool {
    env.storage().persistent().has(&key)                             // D2: replay returns true
}
```

## 8. Proposed repository layout — not yet initialised

```text
sd-05-proof-carrying-agents/
├── contracts/attestation.rs            # Soroban contract        (needs D2, D5 fixed)
├── src/agent.py                        # Receipt builder         (needs D4)
├── src/risk_engine.py                  # Risk evaluator          (needs D1)
├── src/verifier.py                     # Off-chain / on-chain verification
├── tests/test_tamper_detection.py      # Attacks 1-6             (needs D3: must be able to fail)
├── tests/test_risk_thresholds.py       # Risk engine unit tests
├── metrics.json                        # PLANNED — does not exist (D7)
├── Dockerfile
├── REPRODUCE.md
└── CITATION.cff
```

## 9. What must happen before any submission

1. **Resolve the venue.** Obtain the official AIBT CFP. Establish whether the deadline is Sep 15 or Oct 10, whether it is open, and whether the ACM relationship is as assumed. If AIBT is predatory or closed, re-target — ICCBN 2026 is the other candidate in this cycle and is separately unverified.
2. **Decide the risk function.** Implement $\sigma$, or restate the mathematics as a clamp. Then make the worked example exercise the region where the two disagree — a worked example that hides the discrepancy is worse than no example.
3. **Implement replay protection, or delete the claim.** A nonce and expiry, or row 6 of the matrix comes out.
4. **Replace the tautological tests.** At minimum, a policy-adversarial suite: adversarially crafted low-$r$, high-impact actions. If the suite cannot fail, it is not a suite.
5. **Domain-separate the Merkle construction** and hash raw bytes.
6. **Unify the address format** across the DID, the JSON, and the Soroban contract.
7. **Replace D6's placeholder** with a real model hash.
8. **Measure, then publish.** Latency, gas and detection rates belong in `metrics.json` only after a run produces them.
9. Only then: the repository's own submission gate, all seven rules.