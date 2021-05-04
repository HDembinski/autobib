__version__ = "0.1.0"


def main():
    import argparse
    from pathlib import Path
    from . import util

    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=Path)
    args = parser.parse_args()

    aux = util.get_aux_path(args.input_path)

    bib_files, citations = util.scan_aux(aux)

    db = {}

    with util.replace_bib_files(bib_files, db):
        pass
