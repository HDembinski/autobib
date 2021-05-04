__version__ = "0.1.0"


def main():
    import argparse
    from pathlib import Path
    from . import util
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=Path)
    args = parser.parse_args()

    aux = util.get_aux_path(args.input_path)
    aux_time = aux.stats().st_mtime

    bib_files, citations = util.scan_aux(aux)

    db = {}
    with util.replace_bib_files(bib_files, db):
        bib = bib_files[0]
        while True:
            t = aux.stats().st_mtime
            if t > aux_time:
                citations = util.get_aux_citations(aux)
                for c in citations:
                    if c not in db:
                        db[c] = util.get_entry_online(c)
                with open(bib, "w") as f:
                    util.dump(db, f)
                aux_time = t
            time.sleep(0.1)
