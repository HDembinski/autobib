__version__ = "0.3.0"


def main():
    import sys
    from pathlib import Path
    from . import util
    import subprocess as subp

    args = sys.argv[1:]

    def log(x):
        print(f"autobib: {x}")

    print(f"autobib {__version__} called with args: {' '.join(args)}")
    if len(args) == 1:
        # bibtex accepts filename without extension
        aux = Path(args[0]).with_suffix(".aux")
        if aux.exists():
            log(f"Found {aux}")
            bib_files = util.get_aux_bibdata(aux)
            citations = util.get_aux_keys(aux)

            main = None
            all = set()
            for bib in bib_files:
                if bib.exists():
                    with open(bib) as f:
                        db = util.load(f)
                        if main is None:
                            main = db
                        all |= db

            unknown = citations - all

            if unknown:
                bib = bib_files[0]
                with open(bib, "a") as f:
                    for c in unknown:
                        log(f"Fetching online: {c}")
                        ref = util.get_entry_online(c)
                        if not ref:
                            log(f"Warning: no entry found for '{c}'")
                        log(f"Writing {c} to {bib}")
                        f.write(ref)

    # now run original bibtex
    bibtexs = util.find_in_path("bibtex")
    assert len(bibtexs) > 1
    for bibtex in bibtexs:
        with open(bibtex, "rb") as f:
            if f.read(2) == b"#!":
                continue
        break

    subp.run([bibtex] + args)
