__version__ = "0.1.0"


def main():
    import argparse
    from pathlib import Path
    from . import util
    import subprocess as subp

    parser = argparse.ArgumentParser()
    parser.add_argument("auxfile", type=Path)
    args = parser.parse_args()

    aux = args.auxfile.absolute()
    assert aux.exists(), aux

    bib_files = util.get_aux_bibdata(aux)

    db = util.replace_bib_files(bib_files)
    bib = bib_files[0]
    citations = util.get_aux_citations(aux)
    for c in citations:
        if c not in db:
            db[c] = util.get_entry_online(c)
    # could be optimized so that only the new entries are written
    with open(bib, "w") as f:
        util.dump(db.values(), f)

    # now run bibtex
    subp.run(["bibtex", aux])
