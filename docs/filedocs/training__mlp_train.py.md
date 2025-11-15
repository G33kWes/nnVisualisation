# File: `training/mlp_train.py`

- Size: 20009 bytes
- Lines: 529
- SHA256: `fbf28a381530e4a510ed44c87b28a1c83dfa31accbeb2f50b0a2d1e0e338319e`

## Top of file (first lines)
```
"""Utility for training a small MNIST MLP and exporting weights for the visualization."""
from __future__ import annotations

import argparse
import base64
import json
import math
import os
import re
import shutil
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

MNIST_MEAN = 0.1307
MNIST_STD = 0.3081
BASE_DATASET_SIZE = 60_000


def resolve_device(preferred: str | None = None) -> torch.device:
    """Return the best available device, prioritising MPS for Apple silicon."""
    if preferred:
        if preferred == "mps" and torch.backends.mps.is_available():
            return torch.device("mps")
        if preferred == "cuda" and torch.cuda.is_available():
            return torch.device("cuda")
        if preferred == "cpu":
            return torch.device("cpu")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


class SmallMLP(nn.Module):
    """Simple fully connected network for MNIST digits."""

    def __init__(self, input_dim: int, hidden_dims: Sequence[int], num_classes: int = 10):
        super().__init__()
        dims = [input_dim, *hidden_dims, num_classes]
        layers: list[nn.Module] = []
        for idx in range(len(dims) - 1):
            layers.append(nn.Linear(dims[idx], dims[idx + 1]))
            if idx < len(dims) - 2:
                layers.append(nn.ReLU())
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        x = x.view(x.size(0), -1)
        return self.net(x)


@dataclass
class LayerMetadata:
    """Lightweight structural description of a dense layer."""

    layer_index: int
    type: str
    name: str
    activation: str
    weight_shape: tuple[int, int]
    bias_shape: tuple[int]


@dataclass
class LayerSnapshot:
    """Snapshot of a dense layer's parameters."""

    metadata: LayerMetadata
    weight: torch.Tensor
    bias: torch.Tensor
```

## Suggested validation / test commands
- Syntax check: `python -m py_compile "training/mlp_train.py"`
- Run (if safe): `python "training/mlp_train.py"`  # only if the file is intended to be executable

## Functions & responsibilities (extracted)
- `resolve_device(preferred=None)` : choose torch device (mps/cuda/cpu)
- `SmallMLP` : model class (constructor: input_dim, hidden_dims, num_classes)
- `LayerMetadata`, `LayerSnapshot`, `TimelineMilestone` : dataclasses describing export format
- `export_model(output_path, layer_metadata, timeline)` : write manifest (network + timeline)
- `evaluate(model, loader, device)` : compute test accuracy
- `capture_layer_snapshots(model, activations)` : collect per-layer weights/biases
- `build_network_payload(layers)` : construct network metadata dict
- `tensor_to_base64(tensor)` : encode tensor as base16 float16 base64 payload
- `write_snapshot_file(snapshots, directory, order, identifier)` : write per-snapshot JSON files
- `build_default_timeline(dataset_size)` : return list[TimelineMilestone]
- `main()` : CLI entrypoint that trains (or skips) and exports snapshots + manifest

## Expected outputs and formats
- `exports/mlp_weights.json` (manifest):
  - JSON `version` (int), `dtype` (string), `weights.storage` (per_snapshot_files),
     `network` (architecture and per-layer metadata) and `timeline` (array of entries).
- Snapshot files: saved under `exports/mlp_weights/<NN>/` with filenames like `000_initial.json`,
  each file contains `version`, `dtype`, `layers` array where each layer has `weights.shape`,
  `weights.data` (base64 16-bit little-endian bytes), and similar for `biases`.

## Suggested runnable checks (one-step-at-a-time)
1. Syntax check
    - `python -m py_compile training/mlp_train.py`
2. Export initial (no training)
    - `python training/mlp_train.py --skip-train --export-path exports/mlp_weights.json --data-dir data`
    - Check `exports/mlp_weights.json` exists and contains `network` and at least one `timeline` entry.
3. Quick train smoke run (short)
    - `python training/mlp_train.py --epochs 1 --batch-size 256 --hidden-dims 64 32 --export-path exports/mlp_weights.json --data-dir data`
    - Confirm `exports/mlp_weights/` directory contains snapshot files and that their JSON parses.
4. Validate snapshot structure
    - `python -c "import json; s=json.load(open('exports/mlp_weights.json')); print(s['network']['architecture'])"`
5. Validate base64 weights decoding (quick script)
    - Use Python to load a snapshot JSON, decode base64 and confirm length matches `shape` product * 2 (float16 bytes).

## Human guidance: what to look for and how to judge success
- The agent should not proceed to subsequent steps until a human confirms:
  - The manifest (`exports/mlp_weights.json`) is present and contains a non-empty `timeline`.
  - Snapshot files parse as JSON and include `weights.data` and `biases.data` base64 strings.
  - Decoding base64 for at least one layer yields a byte length equal to `prod(shape) * 2` (float16 = 2 bytes).
  - A smoke training run shows printed epoch lines and timeline capture logs like `[Timeline] Captured ...`.

If any of the above fail, the agent should report the failure and pause for human instruction.