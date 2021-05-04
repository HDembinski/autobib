from typing import Dict
import bibtexparser


def load(fo) -> Dict:
    db = {}
    for entry in bibtexparser.load(fo).entries:
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
