# Research Backlog — Prof. Fernando May

> Conference paper pipeline and research workflow management

## Structure

```
research-backlog/
├── BACKLOG.md                    # Single source of truth — all papers & conferences
├── WORKFLOW.md                   # Standard operating procedure for paper development
├── README.md                     # This file
├── opencode.json                 # Project config for opencode
├── .opencode/
│   └── agent/
│       └── research-assistant.md # AI agent for research workflow
├── conferences/                  # Per-conference documentation
│   ├── neurotalk-2026/          # Sep 15-17, Kyoto — SPEAKING INVITE
│   ├── icc-2026/                # Oct 9-11, Harbin (IEEE) — PASSED
│   ├── icmv-2026/               # Oct 15-18, Budapest (SPIE)
│   ├── wsse-2026/               # Oct 16-18, Nara (ACM)
│   ├── etcm-2026/               # Oct 22-24, Guayaquil (IEEE) — Hybrid
│   ├── ai4science-2026/         # Oct 23-25, Shenzhen
│   ├── cciot-2026/              # Oct 24-26, Okinawa (ACM)
│   ├── iccpr-2026/              # Oct 29-Nov 1, Wuxi (Springer)
│   ├── icrcv-2026/              # Nov 6-8, Jiangyin (IEEE)
│   ├── cait-2026/               # Nov 13-15, Guiyang (IEEE)
│   ├── iscmi-2026/              # Nov 18-20, Vienna
│   └── aibt-2026/               # Nov 27-29, Shanghai (ACM)
├── proposals/                    # Paper drafts and outlines
└── workflow/
    └── templates/                # Paper templates (ACM, IEEE, Springer)
```

## Conferences (13 total)

| # | Conference | Dates | Deadline | Publisher | Status |
|---|------------|-------|----------|-----------|--------|
| 1 | Neurotalk 2026 | Sep 15-17 | Reply needed | — | ⏳ Speaking invite |
| 2 | IC&C 2026 | Oct 9-11 | Aug 30 ⚠️ | IEEE | PASSED |
| 3 | ICMV 2026 | Oct 15-18 | Sep 5 | SPIE | 🟡 Active |
| 4 | WSSE 2026 | Oct 16-18 | Sep 5 | ACM | 🟡 Active |
| 5 | IEEE ETCM 2026 | Oct 22-24 | Reg. Aug 30 | IEEE | 🟡 Hybrid |
| 6 | AI4Science 2026 | Oct 23-25 | TBD | TBD | 🟢 Planned |
| 7 | CCIOT 2026 | Oct 24-26 | Sep 1 | ACM | 🟡 Active |
| 8 | ICCPR 2026 | Oct 29-Nov 1 | Sep 5 | Springer | 🟡 Active |
| 9 | ICRCV 2026 | Nov 6-8 | Sep 15 | IEEE | 🟡 Active |
| 10 | CAIT 2026 | Nov 13-15 | Sep 20 | IEEE | 🟢 Planned |
| 11 | ISCMI 2026 | Nov 18-20 | Sep 30 | — | 🟢 Planned |
| 12 | AIBT 2026 | Nov 27-29 | Sep 15 | ACM | 🟡 Active |
| 13 | SmartTech-IC 2026 | Dec 1-3 | Sep 20 | Springer CCIS | 🟢 Virtual OK |

## Quick Start

1. Read `BACKLOG.md` for the full research pipeline
2. Read `WORKFLOW.md` for the paper development process
3. Check `conferences/` for per-conference details
4. Use `workflow/templates/` for paper formatting

## Usage with opencode

This project includes an opencode configuration. The `research-assistant` agent can help manage the backlog and paper writing workflow.
