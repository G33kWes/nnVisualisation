```markdown
# Step 07.01 — tools/mnist_assets (detailed)

Source: `tools/mnist_assets`

## High-level goal
Provide a reproducible set of MNIST test assets used by the visualization (binary images, labels, and a manifest).

## Sub-steps (one at a time)

1) Environment & prerequisites
   - Ensure Python 3.8+ and `numpy` are installed.
   - Commands:
     - `python -V`
     - `python -c "import numpy; print(numpy.__version__)"`

2) Static checks
   - Inspect `tools/mnist_assets/README.md` and the prepare script.
   - Run `python -m py_compile tools/mnist_assets/prepare_mnist_test_assets.py` if present.

3) Generate assets (agent-run)
   - Example: `python tools/mnist_assets/prepare_mnist_test_assets.py --out-dir assets/data`
   - Expected files: `mnist-test-images-uint8.bin`, `mnist-test-labels-uint8.bin`, `mnist-test-manifest.json`.
   - Agent validation: verify manifest lists correct counts and that binary lengths match expected image and label counts.

4) Human check
   - Confirm manifest contents and a few sample images decode to 28x28 bytes and labels are in range 0-9.

## Failure handling
 - On mismatch, save logs under `docs/steps/failures/07_tools__01/` and request human guidance.

## Human explanation
 - "This step creates small binary test datasets used by the visualization. It ensures fast, deterministic
   examples for validation and demos."

```
