"""Run notebooks/main.ipynb end-to-end and save it with its outputs.

This is the single command that reproduces everything:
    python -m src.run
"""
import sys
from pathlib import Path

import nbformat
from ipykernel.kernelspec import install as install_kernelspec
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "main.ipynb"
# Project-specific kernel registered inside the active environment (e.g. .venv), so a
# user-level "python3" kernelspec pointing at another interpreter cannot be picked up.
KERNEL_NAME = "vdl-midterm-gempa"


def ensure_kernel() -> None:
    spec_dir = Path(sys.prefix) / "share" / "jupyter" / "kernels" / KERNEL_NAME
    if spec_dir.is_dir() and KERNEL_NAME in KernelSpecManager().find_kernel_specs():
        return
    install_kernelspec(kernel_name=KERNEL_NAME, display_name="Python (vdl-midterm)", prefix=sys.prefix)


def main() -> None:
    ensure_kernel()
    nb = nbformat.read(NOTEBOOK, as_version=4)
    NotebookClient(nb, timeout=900, kernel_name=KERNEL_NAME, record_timing=False,
                   resources={"metadata": {"path": str(NOTEBOOK.parent)}}).execute()
    nbformat.write(nb, NOTEBOOK)
    print(f"executed {NOTEBOOK.relative_to(ROOT)} ({len(nb.cells)} cells)")


if __name__ == "__main__":
    main()
