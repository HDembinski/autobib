import subprocess as subp
import shutil
from pathlib import Path
from autobib.util import find_in_path, get_bib_keys, Key
import pytest

cwd = Path(__file__).parent
test_document_path = cwd / "data"


@pytest.mark.skipif(not find_in_path("latex"), reason="requires latex")
def test_autobib(tmpdir):
    for fn in ("main.tex", "bar.bib", "foo.bib"):
        shutil.copy(test_document_path / fn, tmpdir / fn)

    subp.run(["latex", "main.tex"], cwd=tmpdir)
    p = subp.run(["bibtex", "main"], cwd=tmpdir)
    assert p.returncode == 0

    with open(tmpdir / "main.bib") as f:
        assert get_bib_keys(f.read()) == {
            Key(s)
            for s in (
                "2020Univ....6..102M",
                "Vanthieghem:2021akb",
                "PierreAuger:2021qsd",
            )
        }
        # "Dembinski:2018ihc" is not in main.bib, because it is in foo.bib
        # "Baur:2019cpv" is not in main.bib, because it is in bar.bib

    assert subp.run(["bibtex", "foobarbaz"], cwd=tmpdir).returncode != 0


@pytest.mark.skipif(not find_in_path("latex"), reason="requires latex")
def test_autobib_updated_key(tmpdir):
    # test renamed key Abe:1993xy -> CDF:1993wpv
    tex = r"""\documentclass{article}
\begin{document}
\cite{Abe:1993xy}
\bibliographystyle{plain}
\bibliography{main}
\end{document}
"""

    with (tmpdir / "main.tex").open("w") as f:
        f.write(tex)

    subp.run(["latex", "main.tex"], cwd=tmpdir)
    assert (tmpdir / "main.aux").exists()

    p = subp.run(["bibtex", "main"], cwd=tmpdir, stdout=subp.PIPE)

    with open(tmpdir / "main.bib") as f:
        assert get_bib_keys(f.read()) == {Key("CDF:1993wpv")}

    with open(tmpdir / "main.tex.bak") as f:
        assert f.read() == tex

    with open(tmpdir / "main.tex") as f:
        assert f.read() == tex.replace("Abe:1993xy", "CDF:1993wpv")

    assert (
        b"""autobib: Updating keys in LaTeX files
autobib:   Abe:1993xy -> CDF:1993wpv
"""
        in p.stdout
    )


@pytest.mark.skipif(not find_in_path("latex"), reason="requires latex")
def test_autobib_backup_failure(tmpdir):
    tex = r"""\documentclass{article}
\begin{document}
\cite{Abe:1993xy}
\bibliographystyle{plain}
\bibliography{main}
\end{document}
"""
    with (tmpdir / "main.tex").open("w") as f:
        f.write(tex)

    subp.run(["latex", "main.tex"], cwd=tmpdir)
    assert (tmpdir / "main.aux").exists()

    with (tmpdir / "main.aux").open() as f:
        aux = f.read()

    p = subp.run(["bibtex", "main"], cwd=tmpdir)
    assert p.returncode == 0
    assert (tmpdir / "main.tex.bak").exists()

    for i in range(3):
        with open(tmpdir / "main.aux", "w") as f:
            f.write(aux)
        p = subp.run(["bibtex", "main"], cwd=tmpdir)
        assert (tmpdir / f"main.tex.bak.{i}").exists()
        assert p.returncode == 0
