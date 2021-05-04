from pathlib import Path
import shutil
import os
import re
from typing import Dict, Set


def get_aux_path(input_path: Path) -> Path:
    if not input_path.exists():
        raise ValueError(f"{input_path} does not exist")

    if input_path.is_dir():
        aux = None
        for fn in input_path.glob("*.aux"):
            if aux is not None:
                raise ValueError("too many aux files in this directory")
            aux = input_path / fn
        if aux is None:
            raise ValueError("no aux file in this directory")
        return aux

    return input_path.with_suffix(".aux")


def scan_aux(aux: Path) -> (Set[Path], Set):
    dir = aux.parent
    with open(aux) as f:
        txt = f.read()
        bib_files = {
            dir / f"{name}.bib" for name in set(re.findall(r"\\bibdata{([^}]+)}", txt))
        }
        citations = set(re.findall(r"\\citation{([^}]+)}", txt))
    return bib_files, citations


def replace_bib_files(bib_files: Set[Path], db: Dict):

    for bib in bib_files:
        if bib.exists():
            shutil.move(bib, bib + ".autobib-backup")
        os.mkfifo(bib)
