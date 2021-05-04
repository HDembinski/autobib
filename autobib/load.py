from pathlib import Path
from typing import Dict
import bibtexparser


def load(bib: Path) -> Dict:
    db = {}
    with open(bib) as f:
        for entry in bibtexparser.load(f).entries:
            db[entry["ID"]] = entry
    return db


# from lark import Lark

# bibtex_parser = Lark("""
# entry: "@" bibkey "{" body "}" ","?
#
# bibkey : /a-zA-Z0-9:/
#
# body :
#
# %import common.ESCAPED_STRING
# %import common.WS
# %ignore WS
#
# """, start="entry")
