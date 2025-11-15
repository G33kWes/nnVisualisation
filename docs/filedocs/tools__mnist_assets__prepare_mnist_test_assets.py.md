# File: `tools/mnist_assets/prepare_mnist_test_assets.py`

- Size: 5961 bytes
- Lines: 170
- SHA256: `b2652e5dd77e49c8b01fb7ff8e7d0feae817fff2f8656c59d3641f514f75a3e5`

## Top of file (first lines)
```
"""Prepare browser-friendly MNIST test assets for the visualisation.

This script converts the canonical IDX files from the MNIST test split
into compact binary blobs that are easy to fetch in the browser.
"""

from __future__ import annotations

import argparse
import gzip
import json
import struct
from pathlib import Path


MNIST_MAGIC_IMAGES = 2051
MNIST_MAGIC_LABELS = 2049
DEFAULT_IMAGE_FILENAME = "mnist-test-images-uint8.bin"
DEFAULT_LABEL_FILENAME = "mnist-test-labels-uint8.bin"
DEFAULT_MANIFEST_FILENAME = "mnist-test-manifest.json"


def read_idx_bytes(path: Path) -> bytes:
    """Return the raw bytes for an IDX file, transparently handling .gz files."""
    if path.exists():
        return path.read_bytes()
    gz_path = path.with_name(path.name + ".gz")
    if gz_path.exists():
        with gzip.open(gz_path, "rb") as handle:
            return handle.read()
    raise FileNotFoundError(f"Neither {path} nor {gz_path} could be located.")


def load_idx(path: Path, expected_magic: int) -> tuple[tuple[int, ...], bytes]:
    """Load an IDX file and return (shape, payload_bytes)."""
    raw = read_idx_bytes(path)
    if len(raw) < 8:
        raise ValueError(f"{path} is too short to contain a valid IDX header.")
    magic, = struct.unpack_from(">I", raw, 0)
    if magic != expected_magic:
        raise ValueError(f"{path} has magic {magic}, expected {expected_magic}.")
    num_dimensions = raw[3]
    if num_dimensions <= 0:
        raise ValueError(f"{path} reports non-positive dimension count: {num_dimensions}.")
    offset = 4
    shape = []
    for idx in range(num_dimensions):
        offset += 4
        if offset > len(raw):
            raise ValueError(f"{path} has truncated dimension metadata at index {idx}.")
        size = struct.unpack_from(">I", raw, offset - 4)[0]
        if size <= 0:
            raise ValueError(f"{path} has non-positive size for dimension {idx}: {size}.")
        shape.append(size)
    payload = raw[offset:]
    expected_length = 1
    for dim in shape:
        expected_length *= dim
    if len(payload) != expected_length:
        raise ValueError(
            f"{path} payload length mismatch: expected {expected_length}, found {len(payload)}.",
        )
    return tuple(shape), payload


def ensure_matching_counts(image_shape: tuple[int, ...], label_shape: tuple[int, ...]) -> int:
    """Validate that the number of images matches the number of labels."""
    if len(image_shape) < 1 or len(label_shape) < 1:
        raise ValueError("Image and label shapes must each have at least one dimension.")
    num_images = image_shape[0]
    num_labels = label_shape[0]
    if num_images != num_labels:
        raise ValueError(f"Image count ({num_images}) does not equal label count ({num_labels}).")
    return num_images


def write_assets(
    image_bytes: bytes,
    label_bytes: bytes,
    output_dir: Path,
```

## Suggested validation / test commands
- Syntax check: `python -m py_compile "tools/mnist_assets/prepare_mnist_test_assets.py"`
- Run (if safe): `python "tools/mnist_assets/prepare_mnist_test_assets.py"`  # only if the file is intended to be executable