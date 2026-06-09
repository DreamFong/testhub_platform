---
name: srs-to-ragflow-kb
description: Turn a source-derived SRS handoff into a RAGFlow-ready knowledge base plan, retrieval question set, offline readiness review, online retrieval gate, and downstream handoff. Use this skill whenever the user wants Skill B, SRS-to-knowledge-base preparation, RAGFlow KB validation from srs-kb-friendly.md/PDF/TXT, retrieval sanity checks, chunk quality review, SRS_KB_ID handoff, or deciding whether an SRS KB can proceed to Skill C or orchestration.
---

# SRS to RAGFlow KB

This is the project-level portable version of **Skill B：知识库构建与检索验证**. It consumes Skill A outputs and produces a RAGFlow knowledge-base readiness package plus an online retrieval gate when RAGFlow access is available and approved.

## What this skill does

Use this skill to turn a completed `source-to-srs` / Skill A run into a reusable Skill B package:

```text
Skill A handoff
→ input snapshot
→ KB create/reuse plan
→ parse config plan
→ retrieval question set
→ offline retrieval readiness review
→ optional real RAGFlow online validation after user confirmation
→ retrieval gate result
→ Skill B handoff for Skill C / orchestration
```

## What this skill does not do

Do not use this skill to:

- Generate or rewrite the SRS itself.
- Modify Skill A outputs.
- Generate TestHub scenario JSON.
- Execute TestHub or target APIs.
- Invent dataset IDs, chunk counts, retrieval results, or pass gates.
- Replace Skill C execution-constraint extraction.

Those belong to `source-to-srs`, Skill C work, or `ragflow-testhub-agent-workflow`.

## Required inputs

Ask for missing values before online work. Offline planning can proceed with the Skill A run directory.

```text
skill_a_run_dir        — directory containing Skill A outputs
project_name           — project display name for handoff
business_domain        — module/domain name
srs_markdown           — usually <skill_a_run_dir>/srs-kb-friendly.md
source_evidence_map    — usually <skill_a_run_dir>/source-evidence-map.md
skill_a_gate_result    — usually <skill_a_run_dir>/gate-result.md
pdf_text_check_report  — usually <skill_a_run_dir>/pdf-text-check-report.md
risk_items             — optional risk-items.md
```

For real RAGFlow online validation, also require:

```text
RAGFLOW_API
RAGFLOW_KEY
TEST_SCOPE
MIN_BUSINESS_FLOW
knowledge base purpose
expected downstream use
language/domain
document types
```

Do not print secrets. Mask `RAGFLOW_KEY` in all summaries.

## Input role rules

Default document roles:

```text
srs-kb-friendly.md      — main analysis input and preferred source for TXT conversion
source-evidence-map.md  — required analysis input, default not uploaded to the main SRS KB
srs-kb-friendly.pdf     — readable delivery artifact and parser experiment candidate, default not main KB input
```

Keep the main SRS KB focused on business requirements. Do not mix `source-evidence-map.md` into the same main SRS KB unless the user explicitly wants a combined evidence KB experiment.

## RAGFlow carrier selection

Use actual RAGFlow behavior and chunk inspection, not only UI labels.

Recommended order for SRS business KB:

1. **TXT carrier generated from `srs-kb-friendly.md`** when Markdown is unsupported or chunk quality matters.
2. **Markdown direct upload** only when the target RAGFlow version supports parsing `.md` and chunks verify cleanly.
3. **PDF + DeepDOC** only when PDF is required or explicitly being tested; reject it if chunks show title-only fragments, lost body text, or neighboring requirement titles merged together.

Known result from the user-management validation:

```text
.md upload: parse blocked in the tested RAGFlow environment.
.pdf upload: parse succeeded, but chunk structure was unreliable due to title merging and body loss.
.txt carrier: book parsing produced stable business chunks and passed with caveats.
```

Treat PDF parse success as insufficient. Always inspect chunk structure and run retrieval sanity checks.

## Workflow

### 1. Read the Skill B reference

Read `references/skill-b-knowledge-base-and-retrieval.md` before running a full Skill B flow.

### 2. Produce offline artifacts

Use the templates under `templates/`:

```text
skill-b-input-snapshot.md
kb-plan.md
parse-config-plan.md
retrieval-question-set.md
offline-retrieval-readiness-report.md
retrieval-gate-result.md
skill-b-handoff.md
```

Use prompts under `prompts/` when executing sub-steps:

```text
skill-b-controller.md
retrieval-question-generation.md
offline-readiness-review.md
retrieval-gate.md
```

### 3. Build retrieval question set

Cover at least:

- Functional requirements.
- Field and validation rules.
- Permission or access-control rules when present in SRS.
- Exception and boundary conditions.
- Acceptance criteria.
- Explicit exclusions.
- Risk items, if present.

For a first online sanity check, 6-10 questions are usually enough. Include critical questions first.

### 4. Decide offline gate

Use:

```text
offline_readiness_gate: pass | conditional pass | fail
```

`offline_readiness_gate = pass` only means the document is ready to request real online validation. It does not mean the RAGFlow KB is usable.

### 5. Ask before external operations

Before creating datasets, uploading files, triggering parsing, or running retrieval against RAGFlow, show the plan and ask the user to confirm. External system writes must be authorized for the current scope.

### 6. Run online validation when approved

When approved:

1. Create a new dataset unless the user explicitly requests reuse.
2. Upload only the planned document set.
3. Trigger parsing.
4. Inspect chunk count and sample chunks.
5. Run retrieval sanity checks.
6. Cross-check answers against `srs-kb-friendly.md` and `source-evidence-map.md`.
7. Record real identifiers and results.

Use `SRS_KB_ID` as the canonical handoff field. Mention `dataset_id` only when describing the raw RAGFlow API result.

### 7. Decide online gate

Use:

```text
online_retrieval_gate: pass | conditional pass | fail | blocked
skill_b_status: offline_ready_pending_online | online_verified | online_verified_with_risks | blocked_waiting_confirmation | blocked_ragflow_unavailable | fail
```

Blocked reasons:

```text
RAGFlow unavailable
external action not approved
online step not executed yet
unsupported document type
parse failed
```

Prefer `fail` over `conditional pass` when chunks show structural loss that will make downstream retrieval unstable, such as missing requirement body text or merged neighboring requirement titles.

## Handoff structure

Always end with a concise handoff block:

```text
PROJECT_NAME=
BUSINESS_DOMAIN=
TEST_SCOPE=
MIN_BUSINESS_FLOW=
SRS_KB_ID=
API_DOCS_KB_ID=
RETRIEVAL_PARAMS=
KNOWN_CAVEATS=
offline_readiness_gate=
online_retrieval_gate=
skill_b_status=
allowed_next_stage=request_online_execution | wait_for_ragflow | manual_fix | skill_c | orchestration | none
```

Recommend `skill_c` when the SRS KB is usable for business requirements but still needs execution-constraint extraction. Recommend `orchestration` only when the downstream workflow can already consume the KBs and caveats directly.

## Quality bar

A Skill B result is not complete until both are true:

- The gate result explains whether the KB can be used and why.
- The handoff makes the next agent's inputs explicit, including caveats and missing KBs.

Do not hide caveats. Conditional pass is acceptable when risks are explicit and the next step can safely consume them.
