# G0-FINDING-001 — BioHealy IPN: derived current limit, no validating measurement

**Object**: `FernandoMay/biohealy-ipn`
**Type**: documentation and correspondence finding
**Raised**: 2026-10-02, G0-3 wave 2 content inspection
**Status**: FROZEN. No repair proposed. No manuscript edited.
**Scope class**: finding, **not** a safety conclusion

---

## 1. The finding

> **The package derives a maximum-current limit from circuit parameters but does not provide an experimental current measurement validating that limit.**

That is the whole claim. It is stated once, it is the whole finding, and nothing below extends it.

## 2. Evidence

`docs/biohealy_paper.tex`, 659 lines, read in full. Repository is 19 files, all enumerated and read, so every absence below is **verified absence across the entire repository**, not an unsuccessful search.

| Element | Status | Location |
|---|---|---|
| Current limit `I_max` | **DERIVED** | `biohealy_paper.tex:249-251` |
| Derivation basis | op-amp saturation at the 12 V rail, 10 kΩ limiting resistor | `biohealy_paper.tex:249-251` |
| Derived value | `I_max = V_sat / R_lim = 12 / 10000 = 1.2 mA` | `biohealy_paper.tex:251` |
| Safety-limit claim | **CLAIMED** | `biohealy_paper.tex:102` — "balanced Howland current pump with hardware safety limits" |
| Current measurement | **ABSENT** | — |
| Frequency measurement | PRESENT (digital oscilloscope, AD9833 output) | `biohealy_paper.tex:532` |
| Magnetic-field measurement | PRESENT (calibrated Hall-effect probe, 1 cm) | `biohealy_paper.tex:538` |

The structural observation: the device exists to deliver current through tissue. Two real verification procedures exist, and both measure a **different quantity** — frequency, and magnetic field. The delivered quantity is not among them.

## 3. Explicitly not claimed

This finding does **not** assert any of the following, and no evidence gathered supports them:

- ✗ That the device is unsafe.
- ✗ That the device exceeds 1.2 mA.
- ✗ That the derived limit is numerically wrong.
- ✗ That any regulatory non-compliance occurred.

## 4. Documentary absences — recorded as absence only

Present across all 19 files and the complete paper:

| Term class | Hits |
|---|---|
| The word "safe" | **0** |
| Electrical safety, galvanic isolation, IEC 60601, UL 60601 | **0** |
| Medical disclaimer, contraindications, "consult a physician" | **0** |
| IRB, ethics committee, informed consent, human subject | **0** |
| Warning, danger, hazard, "do not use" | **0** |

These are recorded as **documentary absences in this repository**. They are **not** a finding of regulatory non-compliance, and not a clinical or safety judgement. This repository is not the whole world; absence here is not absence everywhere.

For contrast, and only as context for what the paper itself asserts: `biohealy_paper.tex:93-94` positions the work against commercial devices that "embed proprietary frequency programs with **limited clinical validation**". The paper draws that distinction and does not state its own validation status.

## 5. Secondary finding — R3 class

`README.md` contains uncompiled LaTeX source in rendered Markdown: `\SIrange{10}{1000}{\micro\ampere}`. The README was pasted from the paper's LaTeX source without compilation.

R3 class: a document that does not correspond to its source form. No code change is required to fix it. It independently establishes that README and paper share a single origin.

## 6. Why the scope was drawn this narrowly

A broader claim was available and was rejected: "a device that stimulates humans documents no safety envelope." It is more alarming and less defensible. It asserts an absence of *intent* and of *process* across materials this inspection cannot see — a wiki, prior revisions, unpublished documentation, or the author's own practice.

The finding as written asserts only what the artifacts show: a derived limit, and no measurement validating it. That is checkable by any reader against a 659-line public file. The broader claim is not.

## 7. Repair status

**No repair proposed.** A repair here would be a new artifact — a current-measurement procedure, an executed measurement, and a gate that verifies the measurement against the derived limit — plus a new falsifier and a new adjudication. That work is out of scope for G0 and is not begun.

Per the standing rule: a repair is validated by restoring a pre-specified property, not by producing different numbers. **No historical published number — including `1.2 mA` — is ever a repair target.**