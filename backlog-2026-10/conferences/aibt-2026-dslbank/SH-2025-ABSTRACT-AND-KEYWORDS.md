# SH-2025 — Abstract and Keywords (draft, 150–250 words)

**Manuscript title:** "The DSL Bank Durability Study: A Blind Adversarial Audit of a Solana Payment-Rails Platform"

**Grounding:** Abstract extracted/rewritten from the actual manuscript at `/Users/fmf/Documents/aibt2026-dslbank/main.tex` (and PDF present). No numbers have been added beyond those that appear in the manuscript; the draft abstracts the audit method and scope without restating unverified numeric claims as new results.

## Abstract (draft, ~186 words)

This paper presents the DSL Bank Durability Study, a blind adversarial audit of a Solana payment-rails platform. The audit was designed to test seven properties of a durable, auditable payment system: reservation safety, submission integrity, settlement authority, recovery correctness, ownership provenance, rail-side evidence, and the structural gates that keep them honest. Conducted blind before deep familiarity with the codebase, the audit methodology explicitly allowed for falsification of its own core property. The study documents the audit process, identifies defects found and subsequently closed with failing tests, reports the seven properties under test, and characterizes crash-and-concurrency behavior across the payment lifecycle. This is a systems and verification contribution for blockchain technology and systems: an audit with reproducible evidence, focused on durability and verifiability of payment rails rather than proposing new consensus mechanisms. The approach emphasizes traceable evidence and testable gates to support independent verification of durability claims in high-throughput payment systems.

## Keywords
- DSL Bank
- Solana payment rails
- blind adversarial audit
- durable payments
- settlement authority
- verification
- reproducible evidence
