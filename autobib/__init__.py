__version__ = "0.1.0"


def main():
    import argparse
    from pathlib import Path
    from . import util
    import subprocess as subp
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("auxfile", type=Path)
    args = parser.parse_args()

    aux = args.auxfile.with_suffix(".aux")
    assert aux.exists(), aux

    # bibtex accepts filename without extension
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

    # now run original bibtex
    for path in os.environ["PATH"].split(":"):
        bibtex = None
        for p in Path(os.path.expandvars(path)).glob("bibtex"):
            assert bibtex is None
            with open(p, "rb") as f:
                if f.read(2) != b"#!":
                    bibtex = p
        if bibtex is not None:
            break

    subp.run([bibtex, aux])
