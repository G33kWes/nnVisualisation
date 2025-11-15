# Manifest schema (spec for new implementations)

Purpose: provide a concise, implementation-agnostic schema the next LLM should follow when producing
an `exports/mlp_weights.json` manifest. The new project must produce a manifest matching this schema.

Top-level keys:
- `version`: integer (e.g., 2)
- `dtype`: string (e.g., `float16`)
- `weights`: object
  - `storage`: string (e.g., `per_snapshot_files`)
  - `format`: string (e.g., `layer_array_v1`)
  - `precision`: string (e.g., `float16`)
- `network`: object (architecture and per-layer metadata)
  - `architecture`: array of integers (e.g., [784, 128, 64, 10])
  - `layers`: array of layer objects
    - `layer_index`: int
    - `type`: string (`dense`)
    - `name`: string
    - `activation`: string (`relu`, `linear`, etc.)
    - `weight_shape`: [rows, cols]
    - `bias_shape`: [n]
  - `input_dim`: int
  - `output_dim`: int
  - `normalization`: object with `mean` and `std`
- `timeline`: array of timeline entries
  - each entry must contain:
    - `id`: string
    - `order`: int
    - `label`: string
    - `kind`: string (`initial`, `approx`, `dataset_multiple`)
    - `target_images`: int
    - `images_seen`: int
    - `batches_seen`: int
    - `dataset_passes`: float
    - `description`: string
    - `metrics`: object (e.g., `test_accuracy`, `avg_training_loss`)
    - `weights`: object with `path`, `dtype`, `format`

Notes for the agent implementing a new project:
- The agent should produce the manifest as JSON with pretty indentation for readability.
- `weights.path` should be a POSIX-style relative path (use forward slashes) pointing to per-snapshot files in
  `exports/mlp_weights/` (or equivalent relative directory in the new project).
- Do not reference or copy payloads from the example snapshots in this repository; produce new snapshots by training
  or synthesizing weights.

Minimal example (pseudocode):

{
  "version": 2,
  "dtype": "float16",
  "weights": { "storage": "per_snapshot_files", "format": "layer_array_v1", "precision": "float16" },
  "network": { "architecture": [784,128,64,10], "layers": [ ... ], "input_dim": 784, "output_dim": 10 },
  "timeline": [ { "id":"initial","order":0,...} ]
}

Acceptance criteria:
- Manifest parses as JSON and contains `network` and `timeline` keys.
- `timeline` entries reference snapshot files that exist relative to the manifest path.
