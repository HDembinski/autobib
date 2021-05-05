__version__ = "0.1.0"


def main():
    import argparse
    from pathlib import Path
    from . import util
    import subprocess as subp

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
    bibtexs = util.find_in_path("bibtex")
    assert len(bibtexs) > 1
    for bibtex in bibtexs:
        with open(bibtex, "rb") as f:
            if f.read(2) == b"#!":
                continue
        break
    subp.run([bibtex, aux])
