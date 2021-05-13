__version__ = "0.6.0"


def main() -> int:
    import sys
    from pathlib import Path
    from . import util
    import subprocess as subp

    args = sys.argv[1:]

    def log(x: str) -> None:
        print(f"autobib: {x}")

    if "--version" in args:
        print(f"autobib {__version__}")
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
                        keys = util.get_bib_keys(f.read())
                        if main is None:
                            main = keys
                        all |= keys

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
                        f.write("\n")
                        f.write(ref)

    # find original bibtex
    bibtexs = util.find_in_path("bibtex")
    assert len(bibtexs) > 1
    # check that we are first in path and skip all other instances of the bibtex script
    for i, bibtex in enumerate(bibtexs):
        with open(bibtex, "rb") as fb:
            is_script = fb.read(2) == b"#!"
        if is_script:
            continue
        else:
            assert i > 0
            break

    # run original bibtex
    return subp.run([bibtex] + args).returncode  # type: ignore
