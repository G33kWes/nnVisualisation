# Agent README — Reproduce nnVisualisation one step at a time

This document instructs an LLM-driven agent how to use the generated markdown to recreate the project.

Workflow (strict):
1. Open `docs/master.md` and select the first step from `docs/steps/`.
2. Open the step file (e.g. `docs/steps/01_assets.md`) and the per-file docs in `docs/filedocs/`.
3. For each file to produce, run the suggested validation commands. For Python files, run `python -m py_compile`.
4. After generating code for a step, create small test scripts (unit or smoke) that verify behavior.
5. Present test results to a human for approval. Only after explicit human approval, proceed to the next step.

Notes:
- Prefer Python for code generation where possible. If another language is required, declare why and include
  the commands the agent will run to validate the produced artifacts.
- Keep changes small and verifiable. Each step should be independently testable.

Agent constraints (important — do NOT duplicate existing code or snapshot blobs):

- **New project requirement:** You must implement this project as a brand-new codebase. Do not copy or reuse source
  code files from this repository (files under `training/`, `tools/`, or `exports/` are **not** to be duplicated). You may
  read the docs to understand interfaces, data formats, and expected behaviors, but the agent's output must be original
  code written by the agent.
- **Snapshots and weights:** The provided `exports/` manifest and snapshot files are example artifacts and may be used
  only as a reference for the file format, timelines, and expected metrics. Do not copy their binary/base64 payloads
  into the new project. If the new project needs weights for demonstrations, generate them by running training, using
  a synthetic data generator, or by implementing a lightweight exporter that produces the same manifest shape.
- **Parameters are allowed:** You may reuse parameter values (network sizes, timeline milestones, dtype choices, JSON
  schema shapes, and CLI argument names). Reusing these parameters helps keep the new project compatible with the
  visualization, but the implementation must be distinct.
- **Validation and tests:** Implement the same validation checks (e.g., base64 decode length == prod(shape)*2) in the
  new project's test suite to show compliance with the manifest/schema. Attach test outputs to each step for human review.

If you are unsure whether something counts as a copy, ask for human clarification before proceeding.