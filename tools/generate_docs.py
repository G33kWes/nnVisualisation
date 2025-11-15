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
        else:
            out.append(f"- File type: {path.suffix or 'unknown'} — manual inspection suggested")
    target = FILEDOCS / f"{info['rel'].replace('/', '__')}.md"
    safe_mkdir(target.parent)
    target.write_text("\n".join(out), encoding="utf-8")
    return target


def component_step(path: Path, index: int) -> Path:
    name = path.name
    title = f"Step {index:02d} — {name}"
    out = [f"# {title}", "", f"Source: `{str(path.relative_to(ROOT)).replace('\\', '/')}`", ""]
    out.append("## Purpose")
    if path.is_dir():
        out.append(f"This directory contains {len(list(path.iterdir()))} items.\n")
        out.append("## Files and substeps")
        for child in sorted(path.iterdir()):
            out.append(f"- `{str(child.relative_to(ROOT)).replace('\\', '/')}`")
    else:
        out.append("This is a single file. See the file-specific doc for details.")
    out.append("")
    out.append("## Recreate / validate")
    out.append("- Follow `filedocs/` for per-file commands to validate or recreate artifacts.")
    out.append("")
    out.append("## Notes")
    out.append("- Consider isolating steps so each is independently testable.")
    p = STEPS / f"{index:02d}_{name}.md"
    safe_mkdir(p.parent)
    p.write_text("\n".join(out), encoding="utf-8")
    return p


def generate_master(components: list[Path]):
    out = ["# Master: nnVisualisation reproduction process", "", "This master file lists the ordered steps an agent\nshould follow to reproduce the `nnVisualisation` project from scratch.", ""]
    out.append("## Steps (in recommended order)")
    for i, c in enumerate(components, start=1):
        rel = str(c.relative_to(ROOT)).replace('\\', '/')
        out.append(f"{i}. `{rel}` — see `steps/{i:02d}_{c.name}.md` for details")
    out.append("")
    out.append("## Agent workflow guidance")
    out.append("See `README_agent.md` for detailed instructions the agent should follow (one step at a time,\nrun tests, request human approval, then continue).")
    p = DOCS / "master.md"
    p.write_text("\n".join(out), encoding="utf-8")
    return p


def generate_agent_readme():
    out = [
        "# Agent README — Reproduce nnVisualisation one step at a time",
        "",
        "This document instructs an LLM-driven agent how to use the generated markdown to recreate the project.",
        "",
        "Workflow (strict):",
        "1. Open `docs/master.md` and select the first step from `docs/steps/`.",
        "2. Open the step file (e.g. `docs/steps/01_assets.md`) and the per-file docs in `docs/filedocs/`.",
        "3. For each file to produce, run the suggested validation commands. For Python files, run `python -m py_compile`.",
        "4. After generating code for a step, create small test scripts (unit or smoke) that verify behavior.",
        "5. Present test results to a human for approval. Only after explicit human approval, proceed to the next step.",
        "",
        "Notes:",
        "- Prefer Python for code generation where possible. If another language is required, declare why and include\n  the commands the agent will run to validate the produced artifacts.",
        "- Keep changes small and verifiable. Each step should be independently testable.",
    ]
    p = DOCS / "README_agent.md"
    p.write_text("\n".join(out), encoding="utf-8")
    return p


def main():
    safe_mkdir(DOCS)
    safe_mkdir(STEPS)
    safe_mkdir(FILEDOCS)

    # Collect top-level components (ignore .git and docs)
    components = []
    for child in sorted(ROOT.iterdir()):
        if child.name in ('.git', 'docs'):
            continue
        components.append(child)

    # Create per-component step files
    for i, comp in enumerate(components, start=1):
        component_step(comp, i)

    # Create filedocs for every file under the project (skip git)
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '.git' not in str(p):
            write_filedoc(p)

    generate_master(components)
    generate_agent_readme()
    print(f"Docs generated into {DOCS}")


if __name__ == '__main__':
    main()
