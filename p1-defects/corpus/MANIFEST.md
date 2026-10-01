# P1 Corpus Manifest

Durable copy of every adjudication, gate log, falsifier log and falsifier source
produced by the P1 sweep. Canonical location:
`research-backlog-repo/p1-defects/corpus/`.

Every package below is **on its remote**. Verified with `git ls-remote`, not with
push output — a push reported as successful was in fact a no-op once during this
sweep, and is recorded in `P1-INSTRUMENT-DEFECTS.md` as defect A4.

| package | repo | branch | tip | contemporaneous gate? |
|---|---|---|---|---|
| **LEO** | `leo-routing` | `fix/leo-audit-sweep` | `42ebcea` | **no gate instrument** |
| **ISAC** | `isac-leo` | `fix/isac-audit-sweep` | `f7816c6` | **no gate instrument** |
| **CRL** | `crl-package` | `fix/crl-audit-sweep` | `696fe0d` | publication gate, different form |
| **QUANTUM** | `quantum-k-sat` | `fix/quantum-audit-sweep` | `f519ea4` | **formal, contemporaneous** |
| **I01** | `i01-leo-edge-orchestration` | `fix/i01-audit-sweep` | `db2be07` | **formal, contemporaneous** |
| **QCE** | `qce-ieee` | `fix/qce-audit-sweep` | `313e9dc` | **formal, contemporaneous** |
| **SGN** | `sgn-ieee-package` | `fix/lsb-roundtrip-identity` | `ccb9aa5` | **formal, contemporaneous** |

## The gate distinction is load-bearing, not cosmetic

**Four packages were adjudicated under the formal gate discipline. Three were not.**

CRL has a *publication* gate with `PASS` lines and its own criteria. It is a real
instrument and it is preserved, but it is not the formal pipeline, and counting it as
one would overstate the discipline applied.

LEO and ISAC have **no gate at all**. The gate concept was introduced during the sweep,
after those two were audited. Running today's gate against their trees would license
the claim *"these trees pass the current gate"*. It would **not** license the claim
*"the original adjudication was produced under this gate discipline"*. Those are
different claims, and only the first is available.

**This is why the gaps are not backfilled.** A retrospective gate validates a corpus
produced without one, which is a weaker claim than never having claimed it.

## Contents

- `adjudications/` — 13 documents. `CLAIM-INVENTORY-*` records implementation
  facts only; `CLAIM-ADJUDICATION-*` records claim correspondence and disposition.
- `gates/` — 5 logs: 4 formal contemporaneous gates (Quantum, i01, QCE, SGN) and
  CRL's publication gate of a different form. **LEO and ISAC have none.**
- `falsifier-logs/` — 31 documents, including `LOST-AUDIT-EVIDENCE.md` for LEO, which
  records three RED transcripts that were permanently lost to a `tee` collision and
  are recorded as lost rather than reconstructed.
- `instruments/` — 30 falsifier and gate sources, one directory per package.

