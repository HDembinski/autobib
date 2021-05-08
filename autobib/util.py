from pathlib import Path
import re
from typing import Dict, Set, List
import requests
from .io import parse
import os


def load(f) -> Dict:
    return parse(f.read())


def dump(dict, f):
    for entry in dict.values():
        f.write(f"{entry}\n\n")


def get_aux_bibdata(aux: Path) -> List[Path]:
    with open(aux) as f:
        names = re.findall(r"\\bibdata{([^}]+)}", f.read())
    # split comma-separated entries
    names = sum((name.split(",") for name in names), [])
    # make unique while preserving order
    dir = aux.parent
    return [dir / f"{name}.bib" for name in dict.fromkeys(names)]


def get_aux_citations(aux: Path) -> Set:
    with open(aux) as f:
        txt = f.read()
        tmp = re.findall(r"\\citation{([^}]+)}", txt)
    # split multi-citations
    result = set()
    for c in tmp:
        result.update(c.split(","))
    return result


def get_entry_online(key) -> Dict:
    # https://github.com/inspirehep/rest-api-doc
    r = requests.get(
        "https://inspirehep.net/api/literature", params={"q": key, "format": "bibtex"}
    )
    return parse(r.content.decode())


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
