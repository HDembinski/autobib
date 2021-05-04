import bibtexparser
from bibtexparser.bibdatabase import BibDatabase


def dump(db, f):
    bdb = BibDatabase()
    bdb.entries = list(db.values())
    bibtexparser.dump(bdb, f)
