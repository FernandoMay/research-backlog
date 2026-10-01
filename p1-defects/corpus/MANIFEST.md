# P1 Corpus Manifest

Durable copy of every adjudication, gate log, falsifier log and falsifier source
produced by the P1 sweep. Canonical location:
`research-backlog-repo/p1-defects/corpus/`.

Every package below is **on its remote**. Verified with `git ls-remote`, not with
push output — a push reported as successful was in fact a no-op once during this
sweep, and is recorded in `P1-INSTRUMENT-DEFECTS.md` as defect A4.

| package | repo | branch | tip | gate | note |
|---|---|---|---|---|---|
| **LEO** | `leo-routing` | `fix/leo-audit-sweep` | `42ebcea` | NO GATE EXISTS | gate concept postdates this package |
| **ISAC** | `isac-leo` | `fix/isac-audit-sweep` | `f7816c6` | NO GATE EXISTS | gate concept postdates this package |
| **CRL** | `crl-package` | `fix/crl-audit-sweep` | `696fe0d` | present, different form | narrative close, not PASS/FAIL markers |
| **QUANTUM** | `quantum-k-sat` | `fix/quantum-audit-sweep` | `f519ea4` | present | gate rejected 2 of 6 falsifiers on first run |
| **I01** | `i01-leo-edge-orchestration` | `fix/i01-audit-sweep` | `db2be07` | present | gate rejected its own 3 reported problems |
| **QCE** | `qce-ieee` | `fix/qce-audit-sweep` | `313e9dc` | present | gate found 4 of its own defects |
| **SGN** | `sgn-ieee-package` | `fix/lsb-roundtrip-identity` | `ccb9aa5` | present | CLEAN TREE could not fail the gate |

## Contents

- `adjudications/` — 11 documents. `CLAIM-INVENTORY-*` records implementation
  facts only; `CLAIM-ADJUDICATION-*` records claim correspondence and disposition.
- `gates/` — 4 logs. **LEO and ISAC have none**: the gate discipline was introduced
  during the sweep and did not reach the two packages audited before it existed.
- `falsifier-logs/` — 26 documents, including `LOST-AUDIT-EVIDENCE.md` for LEO, which
  records three RED transcripts that were permanently lost to a `tee` collision and
  are recorded as lost rather than reconstructed.
- `instruments/` — 30 falsifier and gate sources, one directory per package.

