__version__ = "0.1.3"


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

            main = []
            all = []
            for bib in bib_files:
                with open(bib) as f:
                    db = util.load(f)
                    if not main:
                        main = db
                    all += db

            bib = bib_files[0]

            known = set(x["ID"] for x in all)

            need_update = False
            for c in citations:
                if c not in known:
                    log(f"Fetching online: {c}")
                    main.append(util.get_entry_online(c))
                    need_update = True

            if need_update:
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
