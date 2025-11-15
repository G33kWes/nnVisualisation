# File: `tools/generate_docs.py`

- Size: 7038 bytes
- Lines: 176
- SHA256: `7e5ac5c1ffc84c43655f06aed4d02e3c20533a621c064ccf54e21dcd09be592c`

## Top of file (first lines)
```
"""Generate step-by-step markdown docs for the nnVisualisation project.

Produces the following under `docs/` in the project root:
- `master.md` : master process / high-level steps
- `steps/NN_<component>.md` : per-component step descriptions
- `filedocs/<relative_path>.md` : per-file extracted header, suggested tests and commands
- `README_agent.md` : instructions for an LLM agent to reproduce the project one step at a time

Intended usage:
  python tools/generate_docs.py

The generated files are intended to be consumed by an external LLM-based agent
that will implement or re-generate the project by following the steps and running
the suggested tests. Each step includes suggested CLI commands to validate.
"""
from __future__ import annotations
import os
from pathlib import Path
import hashlib
import textwrap
import json


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
STEPS = DOCS / "steps"
FILEDOCS = DOCS / "filedocs"


def safe_mkdir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def file_summary(path: Path) -> dict:
    try:
        b = path.read_bytes()
    except Exception:
        return {"error": "unable to read"}
    sha = hashlib.sha256(b).hexdigest()
    try:
        txt = b.decode("utf-8")
    except Exception:
        txt = b.decode("utf-8", errors="replace")
    lines = txt.splitlines()
    header = "\n".join(lines[:80])
    return {
        "rel": str(path.relative_to(ROOT)).replace('\\', '/'),
        "size_bytes": len(b),
        "sha256": sha,
        "lines": len(lines),
        "header": header,
    }


def write_filedoc(path: Path):
    info = file_summary(path)
    out = []
    out.append(f"# File: `{info.get('rel')}`")
    out.append("")
    if "error" in info:
        out.append("Could not read file contents.")
    else:
        out.append(f"- Size: {info['size_bytes']} bytes")
        out.append(f"- Lines: {info['lines']}")
        out.append(f"- SHA256: `{info['sha256']}`")
        out.append("")
        out.append("## Top of file (first lines)")
        out.append("```")
        out.append(info['header'])
        out.append("```")
        out.append("")
        out.append("## Suggested validation / test commands")
        rel = info['rel']
        if rel.endswith('.py'):
            out.append(f"- Syntax check: `python -m py_compile \"{rel}\"`")
            out.append(f"- Run (if safe): `python \"{rel}\"`  # only if the file is intended to be executable")
        elif rel.endswith('.html'):
            out.append(f"- Inspect in browser: open the `index.html` or render with a static server")
        elif rel.endswith('.sh') or rel.endswith('.ps1'):
            out.append(f"- Shell script: run on appropriate shell (`bash` or `powershell`) and inspect outputs")
```

## Suggested validation / test commands
- Syntax check: `python -m py_compile "tools/generate_docs.py"`
- Run (if safe): `python "tools/generate_docs.py"`  # only if the file is intended to be executable