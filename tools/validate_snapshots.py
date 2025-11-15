"""Validate exported manifest and snapshot files for nnVisualisation.

This helper performs the following checks:
- Parse the manifest JSON (`exports/mlp_weights.json`) and ensure it contains `network` and `timeline`.
- Optionally load the first timeline entry's snapshot file and decode base64-encoded weight/bias blobs.
- Confirm decoded byte lengths match the declared shapes (float16 => 2 bytes per element).

Usage examples:
  python tools/validate_snapshots.py --manifest exports/mlp_weights.json --check-first
  python tools/validate_snapshots.py --snapshot exports/mlp_weights/000_initial.json
"""
from __future__ import annotations
import argparse
import base64
import json
import os
from pathlib import Path
import sys
import math
import numpy as np


def load_json(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def decode_and_check(data_b64: str, shape: list[int]) -> tuple[bool, int]:
    raw = base64.b64decode(data_b64)
    expected = int(np.prod(shape) * 2)
    return (len(raw) == expected), len(raw)


def check_manifest(manifest_path: Path, check_first: bool = False):
    m = load_json(manifest_path)
    ok = True
    if 'network' not in m or 'timeline' not in m:
        print(f"ERROR: manifest {manifest_path} missing 'network' or 'timeline' keys")
        ok = False
    else:
        print(f"Manifest {manifest_path} parsed. network.layers: {len(m['network'].get('layers', []))}, timeline: {len(m.get('timeline', []))}")
    if check_first and m.get('timeline'):
        first = m['timeline'][0]
        weights_path = Path(manifest_path.parent) / first['weights']['path']
        if not weights_path.exists():
            print(f"ERROR: snapshot file not found: {weights_path}")
            return False
        s = load_json(weights_path)
        layers = s.get('layers', [])
        for idx, layer in enumerate(layers):
            wshape = layer['weights']['shape']
            ws = layer['weights']['data']
            ok_shape, raw_len = decode_and_check(ws, wshape)
            print(f"Layer {idx}: expected bytes {int(np.prod(wshape)*2)} got {raw_len} -> {'OK' if ok_shape else 'MISMATCH'}")
            if not ok_shape:
                ok = False
    return ok


def check_snapshot(snapshot_path: Path):
    s = load_json(snapshot_path)
    layers = s.get('layers', [])
    all_ok = True
    for idx, layer in enumerate(layers):
        wshape = layer['weights']['shape']
        ws = layer['weights']['data']
        ok_shape, raw_len = decode_and_check(ws, wshape)
        print(f"Layer {idx}: expected bytes {int(np.prod(wshape)*2)} got {raw_len} -> {'OK' if ok_shape else 'MISMATCH'}")
        if not ok_shape:
            all_ok = False
    return all_ok


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', type=Path, help='Manifest JSON path (exports/mlp_weights.json)')
    p.add_argument('--snapshot', type=Path, help='Snapshot JSON path to validate directly')
    p.add_argument('--check-first', action='store_true', help='When given --manifest, check the first timeline snapshot')
    args = p.parse_args()
    if args.manifest:
        ok = check_manifest(args.manifest, check_first=args.check_first)
        sys.exit(0 if ok else 2)
    if args.snapshot:
        ok = check_snapshot(args.snapshot)
        sys.exit(0 if ok else 2)
    print('No action specified. Provide --manifest or --snapshot')
    sys.exit(1)


if __name__ == '__main__':
    main()
