```markdown
# Step 08.01 — training/mlp_train.py (detailed)

Source: `training/mlp_train.py`

## High-level goal
Produce a reproducible weights export and timeline snapshots from a small MNIST MLP so the visualization
can animate training progress. The agent must perform small, verifiable actions and get human approval
before proceeding.

## Sub-steps (one at a time)

1) Environment & prerequisites
   - Ensure Python 3.8+ is available and `torch`, `torchvision`, and `numpy` are installed.
   - Commands:
     - `python -V`
     - `python -c "import torch, torchvision, numpy; print(torch.__version__)"`
   - Human check: confirm GPU device selection is acceptable (MPS/CUDA/CPU).

2) Static checks
   - Run `python -m py_compile training/mlp_train.py`.
   - Human check: syntax ok.

3) Export initial weights (no training)
   - Run: `python training/mlp_train.py --skip-train --export-path exports/mlp_weights.json --data-dir data`
   - Expected outcome:
     - `exports/mlp_weights.json` exists and includes a `network` object and at least one `timeline` entry.
     - A directory `exports/mlp_weights` (or similar) containing `000_initial.json` snapshot file.
   - Test commands (agent-run): parse the JSON and verify `timeline[0]['id']=='initial'`.
   - Human check: confirm manifest looks sensible.

4) Quick training smoke run
   - Run a short training (small epochs):
     - `python training/mlp_train.py --epochs 1 --batch-size 256 --hidden-dims 64 32 --export-path exports/mlp_weights.json --data-dir data`
   - Expected outcome: console prints epoch status and `[Timeline] Captured ...` messages.
   - Agent validation: check snapshot folder contains at least one additional snapshot file and parse JSON.
   - Human check: confirm accuracy printed and snapshot count increased.

5) Validate snapshot payloads
   - For a chosen snapshot file (e.g., `exports/mlp_weights/000_initial.json`):
     - Verify JSON `version` and `dtype` fields.
     - Decode `weights.data` (base64) and confirm byte length matches `prod(shape) * 2`.
   - Provide a short helper snippet in the step (agent can run):
     ```python
     import json, base64, numpy as np
     s=json.load(open('exports/mlp_weights/000_initial.json'))
     layer=s['layers'][0]
     b64=layer['weights']['data']
     data=base64.b64decode(b64)
     shape=layer['weights']['shape']
     assert len(data)==(np.prod(shape)*2)
     print('OK')
     ```
   - Human check: confirm helper prints `OK`.

6) Full run (if desired)
   - Run with default or larger epochs to produce full timeline as defined by `build_default_timeline`.

## Sub-sub-steps (what to do for changed files)
- If the agent modifies `mlp_train.py`, it must:
  1. Re-run static checks.
  2. Re-run export-initial and quick-train steps above.
  3. Re-run snapshot validation helper.

## Failure handling and human prompts
- If a step fails (missing file, JSON parse error, base64 mismatch), the agent should:
  - Save the failing file and a short log under `docs/steps/failures/08_training__01/`.
  - Request human guidance and do not proceed to other steps until human approves.

## Human-readable explanation to show the user
- "This step trains a small fully-connected network on MNIST and writes a manifest plus per-snapshot
  weight files. The manifest (`exports/mlp_weights.json`) tells the visualization how the network is
  structured and where snapshots live. Each snapshot contains compressed (float16) weight blobs encoded
  as base64. To verify the step, run the short validation snippet — it checks that the base64 payload
  length matches the expected number of float16 values."

``` 
