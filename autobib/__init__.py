__version__ = "0.2.0"


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
            citations = util.get_aux_citations(aux)

            main = {}
            all = {}
            for bib in bib_files:
                if bib.exists():
                    with open(bib) as f:
                        db = util.load(f)
                        if not main:
                            main = db
                        all.update(db)

            bib = bib_files[0]

            unknown = citations - set(all.keys())

            if unknown:
                for c in unknown:
                    log(f"Fetching online: {c}")
                    ref = util.get_entry_online(c)
                    if not ref:
                        log(f"Warning: no entry found for '{c}'")
                    main.update(ref)
                # could be optimized so that only new entries are written
                log(f"Writing {bib}")
                with open(bib, "w") as f:
                    util.dump(main, f)

    # now run original bibtex
    bibtexs = util.find_in_path("bibtex")
    assert len(bibtexs) > 1
    for bibtex in bibtexs:
        with open(bibtex, "rb") as f:
            if f.read(2) == b"#!":
                continue
        break

    subp.run([bibtex] + args)
