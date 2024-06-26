from ._version import version as __version__  # noqa


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
    debug = "--debug" in args
    if debug:
        args.remove("--debug")

    if len(args) == 1:
        # bibtex accepts filename without extension
        aux = Path(args[0]).with_suffix(".aux")
        if aux.exists():
            bib_files = util.get_aux_bibdata(aux)
            citations = util.get_aux_keys(aux)
            if debug:
                log(f"Found aux: {aux}")
                log("Found bib: " + " ".join(str(x) for x in bib_files))
                log("Found citations:")
                for x in sorted(citations):
                    log(f"  {x}")
            main = None
            all = set()
            for bib in bib_files:
                if bib.exists():
                    with open(bib) as f:
                        keys = util.get_bib_keys(f.read())
                        if debug:
                            log(f"Entries in {bib}:")  # noqa
                            for x in sorted(keys):
                                log(f"  {x}")
                        if main is None:
                            main = keys
                        all |= keys

            unknown = citations - all

            # Inspire is currently updating their keys. Entries are still found under
            # the old key, but an entry with the new key is returned.
            keys_need_update = []
            if unknown:
                bib = bib_files[0]
                with open(bib, "a") as f:
                    for c in unknown:
                        log(f"Fetching key online: {c}")
                        key_ref = util.get_entry_online(c)
                        if key_ref is None:
                            log(f"Warning: no entry found for '{c}'")
                            continue
                        key, ref = key_ref
                        if key != c:
                            log(f"  Fetched key {key} differs")
                            keys_need_update.append((c, key))
                            if key in all:  # already downloaded
                                continue
                        log(f"Writing {key} to {bib}")
                        f.write("\n")
                        f.write(ref)

            if keys_need_update:
                log("Updating keys in LaTeX files")
                for fr, to in keys_need_update:
                    log(f"  {fr} -> {to}")
                tex = aux.with_suffix(".tex")
                assert tex.exists()
                with open(tex) as f:
                    t = f.read()
                with open(aux) as f:
                    a = f.read()
                bak = tex.with_suffix(".tex.bak")
                for i in range(100):
                    if not bak.exists():
                        break
                    bak = tex.with_suffix(f".tex.bak.{i}")
                else:
                    raise IOError("could not create backup of tex file")
                with open(bak, "w") as f:
                    f.write(t)
                for fr, to in keys_need_update:
                    t = t.replace(fr, to)
                    a = a.replace(fr, to)
                with open(tex, "w") as f:
                    f.write(t)
                with open(aux, "w") as f:
                    f.write(a)

    if (
        len(sys.argv) == 2
        and sys.argv[1] == "--help"
        and sys.argv[0].endswith("bibtex-autobib")
    ):
        msg = """\
autobib: The easiest way to use bibtex-autobib is to create a link

    ln -s /path/to/bibtex-autobib /some/path/bibtex

where /some/path must appear in the PATH environment variable
before the original bibtex.
"""
        log(msg)

    # find original bibtex
    bibtexs = util.find_in_path("bibtex")
    bibtex = util.get_original_bibtex(bibtexs)
    if not bibtex:
        raise SystemExit(
            """\
bibtex was not found on this system. You need to install bibtex to use autobib."""
        )
    # run original bibtex
    return subp.run([bibtex] + args).returncode  # type: ignore
