import bibtexparser
from bibtexparser.bibdatabase import BibDatabase


def dump(entries, f):
    bdb = BibDatabase()
    bdb.entries = entries
    bibtexparser.dump(bdb, f)
