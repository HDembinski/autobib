from pathlib import Path
import re
from typing import Dict, Set, List
import requests
import os


def get_bib_keys(txt) -> Set:
    return set(re.findall(r"@[a-zA-Z]+\{([^,]+),", txt))


def get_aux_bibdata(aux: Path) -> List[Path]:
    with open(aux) as f:
        # having more than one bibdata is an error
        m = re.search(r"\\bibdata{([^}]+)}", f.read())
    # split comma-separated entries
    names = m.group(1).split(",") if m else []
    # make unique while preserving order
    dir = aux.parent
    return [dir / f"{name}.bib" for name in dict.fromkeys(names)]


def get_aux_keys(aux: Path) -> Set:
    with open(aux) as f:
        txt = f.read()
    return set(re.findall(r"\\citation{([^}]+)}", txt))


def get_entry_online(key) -> Dict:
    # https://github.com/inspirehep/rest-api-doc
    r = requests.get(
        "https://inspirehep.net/api/literature", params={"q": key, "format": "bibtex"}
    )
    txt = r.content.decode()
    assert len(get_bib_keys(txt)) <= 1
    return txt


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
