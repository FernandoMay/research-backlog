# Research Workflow

> Standard Operating Procedure for conference paper development
> Prof. Fernando May — Research Pipeline

---

## Workflow Stages

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  1. INTAKE  │───▶│  2. PLAN    │───▶│  3. WRITE   │───▶│  4. REVIEW  │───▶│  5. SUBMIT  │
│  (Backlog)  │    │  (Research) │    │  (Draft)    │    │  (Quality)  │    │  (Publish)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼                  ▼
  Add to BACKLOG    Create plan file    Write paper        Check quality      Submit to
  with deadline     in conferences/     in proposals/      + peer review      conference
                    <conf>/             <id>.md                            portal
```

---

## Stage 1: Intake (Backlog)

**Trigger:** New conference invitation email received

**Steps:**
1. Extract conference metadata (name, dates, venue, deadline, topics, publisher)
2. Add conference to `BACKLOG.md` — Conference Pipeline section
3. Cross-reference with existing papers to detect duplicates/overlaps
4. Assign priority: 🔴 Deadline < 2w | 🟡 2-6w | 🟢 6+w
5. Create conference directory: `conferences/<conf-abbreviation>/`
6. Update Priority Queue in BACKLOG.md

**Output:** Updated `BACKLOG.md` + new conference directory

---

## Stage 2: Plan (Research Design)

**Trigger:** Paper assigned to a conference in BACKLOG.md

**Steps:**
1. Create research plan file: `conferences/<conf>/<paper-id>-PLAN.md`
2. Define:
   - Paper title (working)
   - Abstract (250 words)
   - Research questions (3-5)
   - Methodology
   - Expected contributions
   - Timeline (weeks until deadline)
   - Required resources (datasets, compute, collaborators)
   - References (10-15 key papers)
3. Review existing repo code/data that supports this research
4. Identify gaps — what needs to be built/simulated/analyzed
5. Set milestone dates within the timeline

**Output:** `conferences/<conf>/<paper-id>-PLAN.md`

---

## Stage 3: Write (Draft Development)

**Trigger:** Plan approved / research milestones hit

**Sub-stages:**

### 3a. Outline
- Create `proposals/<paper-id>-OUTLINE.md`
- Structure: Introduction → Related Work → Methodology → Experiments → Results → Conclusion
- Each section: 2-4 bullet points of content to cover

### 3b. First Draft
- Create `proposals/<paper-id>-DRAFT-v1.md`
- Full paper following conference template (ACM/IEEE/Springer)
- Target: 8-10 pages (or conference specified length)
- Include figures, tables, equations as needed

### 3c. Revision
- Create `proposals/<paper-id>-DRAFT-v2.md` (if needed)
- Address reviewer feedback
- Strengthen weak sections
- Verify references

**Output:** `proposals/<paper-id>-DRAFT-v{N}.md`

---

## Stage 4: Review (Quality Assurance)

**Trigger:** Draft complete

**Checklist:**

- [ ] **Formatting:** Matches conference template (ACM/IEEE/Springer)
- [ ] **Length:** Within page limits
- [ ] **Abstract:** < 250 words, clear contribution statement
- [ ] **Keywords:** 4-6 relevant keywords
- [ ] **Introduction:** Problem, motivation, contributions clearly stated
- [ ] **Related Work:** Adequate coverage, properly cited
- [ ] **Methodology:** Reproducible, well-explained
- [ ] **Results:** Statistical significance, proper baselines
- [ ] **Figures:** High resolution, properly labeled
- [ ] **References:** Complete, recent, properly formatted
- [ ] **Plagiarism:** No overlap with own prior work (self-plagiarism check)
- [ ] **English:** Grammar, clarity, academic tone

**Quality Gate:** All items checked before proceeding to submission

**Output:** Updated draft + checklist completion

---

## Stage 5: Submit (Conference Submission)

**Trigger:** Quality gate passed + deadline approaching

**Steps:**
1. Convert to conference-required format (PDF, LaTeX source)
2. Upload to conference submission portal
3. Record submission in BACKLOG.md (update Status to ✅)
4. Add submission details to conference directory:
   - `conferences/<conf>/<paper-id>-SUBMISSION.md` (confirmation, ID, dates)
5. Set calendar reminders for:
   - Notification date
   - Camera-ready deadline
   - Conference registration deadline
   - Travel/visa deadlines (if in-person)

**Output:** `conferences/<conf>/<paper-id>-SUBMISSION.md` + updated BACKLOG.md

---

## File Naming Convention

```
conferences/
  <conf-abbreviation>/
    <paper-id>-PLAN.md          # Research plan
    <paper-id>-SUBMISSION.md    # Submission record
proposals/
  <paper-id>-OUTLINE.md         # Paper outline
  <paper-id>-DRAFT-v1.md        # First draft
  <paper-id>-DRAFT-v2.md        # Revision (if needed)
  <paper-id>-FINAL.md           # Final version
workflow/
  templates/
    acm-template.md             # ACM paper template
    ieee-template.md            # IEEE paper template
    springer-template.md        # Springer paper template
```

---

## Paper ID Convention

Format: `<letter>-<NN>` where:
- `<letter>` = Conference abbreviation initial (S=WSSE, I=CCIOT, P=ICCPR, etc.)
- `<NN>` = Sequential number

Examples:
- `S-01` = First WSSE paper
- `I-01` = First CCIOT paper
- `P-01` = First ICCPR paper

---

## Duplicate Paper Strategy

When a paper could fit multiple conferences:

1. **Primary venue:** Best topical fit + earliest deadline + highest impact
2. **Secondary venue:** If rejected from primary, revise and resubmit
3. **Never submit simultaneously** to multiple venues (ethical violation)
4. Document decision in the paper's PLAN.md

---

## Weekly Review Process

Every Monday:
1. Review BACKLOG.md Priority Queue
2. Check for deadline changes (conference websites)
3. Update paper statuses
4. Identify blocked items
5. Plan week's research tasks

---

*Follow this workflow for every paper. Consistency = quality.*
