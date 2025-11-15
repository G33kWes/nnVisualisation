# Snapshot format (per-snapshot file spec)

Purpose: specify the JSON layout for per-snapshot weight files that the visualization expects.

Required top-level keys:
- `version`: int (e.g., 1)
- `dtype`: string (e.g., `float16`)
- `layers`: array of layer objects

Each layer object contains:
- `layer_index`: int
- `name`: string
- `activation`: string
- `weights`: object
  - `shape`: [rows, cols]
  - `data`: base64 string encoding little-endian float16 bytes representing weights in row-major order
- `biases`: object
  - `shape`: [n]
  - `data`: base64 string encoding little-endian float16 bytes representing biases

Notes & validation rules for the agent:
- When producing `data`, take care to encode float16 values to little-endian 2-byte floats and base64-encode the bytes.
- Validation rule: decoded bytes length == prod(shape) * 2 for float16 arrays.
- Use compact JSON (no extra whitespace) for snapshot files if desired; the manifest should reference them.

Example layer payload (pseudocode):

{
  "layer_index": 0,
  "name": "dense_0",
  "activation": "relu",
  "weights": { "shape": [128,784], "data": "<base64>" },
  "biases": { "shape": [128], "data": "<base64>" }
}
