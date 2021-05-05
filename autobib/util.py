from pathlib import Path
import re
from typing import Dict, Set, List
import requests
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
import os


def load(fo) -> Dict:
    db = {}
    for entry in bibtexparser.load(fo).entries:
        db[entry["ID"]] = entry
    return db


def dump(entries, f):
    bdb = BibDatabase()
    bdb.entries = entries
    bibtexparser.dump(bdb, f)


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


def get_aux_bibdata(aux: Path) -> List[Path]:
    dir = aux.parent
    with open(aux) as f:
        txt = f.read()
        bib_files = [
            dir / f"{name}.bib" for name in set(re.findall(r"\\bibdata{([^}]+)}", txt))
        ]

    # make unique while preserving order
    bib_files = list(dict.fromkeys(bib_files))
    return bib_files


def get_aux_citations(aux: Path) -> Set:
    with open(aux) as f:
        txt = f.read()
        citations = set(re.findall(r"\\citation{([^}]+)}", txt))
    return citations


def get_entry_online(key) -> Dict:
    # https://github.com/inspirehep/rest-api-doc
    r = requests.get(
        "https://inspirehep.net/api/literature", params={"q": key, "format": "bibtex"}
    )
    return bibtexparser.loads(r.content).entries[0]


def replace_bib_files(bib_files: List[Path]):
    db = {}
    for bib in bib_files:
        if bib.exists():
            with open(bib) as f:
                db.update(load(f))
    for bib in bib_files[1:]:
        with open(bib, "w") as f:
            f.write("")
    return db


def find_in_path(name):
    paths = ["/bin", "/usr/bin", "/usr/local/bin"]
    for path in os.environ["PATH"].split(":"):
        path = os.path.expandvars(path)
        paths.append(path)

    results = []
    for path in paths:
        for p in Path(os.path.expandvars(path)).glob(name):
            results.append(p)

    return results
