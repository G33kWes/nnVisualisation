```markdown
# Step 04.01 — exports (manifest & snapshots)

Source: `exports/` directory and `exports/mlp_weights.json` manifest

## High-level goal
Ensure exported snapshot files and the manifest are present, correctly formatted, and consistent with the snapshot payloads.

## Sub-steps (one at a time)

1) Static checks
   - Inspect `exports/` for `mlp_weights.json` and snapshot files under `exports/mlp_weights/`.

2) Manifest parse
   - Run: `python -c "import json; print(json.load(open('exports/mlp_weights.json')).keys())"`
   - Agent should confirm `network` and `timeline` keys exist.

3) Snapshot file generation & base64 validation (agent must produce new snapshots)
    - Important: Do NOT copy existing snapshot payloads from this repository. Instead, generate new snapshot files
       by implementing a training run or a synthetic-weight generator in the new project.
    - Use the `tools/validate_snapshots.py` helper approach (or a reimplementation of the same checks) to verify a
       snapshot file decodes correctly and matches declared shapes.
    - Example (after producing a snapshot file):
       `python tools/validate_snapshots.py --snapshot exports/mlp_weights/000_initial.json`
    - Refer to `docs/specs/manifest_schema.md` and `docs/specs/snapshot_format.md` for the expected JSON shapes
       and base64 encoding rules.

4) Human check
   - Confirm manifest and snapshots are consistent and that the visualization's `index.html` can read the manifest.

## Failure handling
 - Save failing payloads and logs under `docs/steps/failures/04_exports__01/` and request human guidance.

## Human explanation
 - "The manifest points to per-snapshot weight files. This step validates that the manifest is present and
   that snapshot files contain correctly encoded float16 weight blobs."

```
