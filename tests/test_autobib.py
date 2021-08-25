import subprocess as subp
import shutil
from pathlib import Path
from autobib.util import find_in_path, get_bib_keys
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
            "2020Univ....6..102M",
            "Vanthieghem:2021akb",
            "PierreAuger:2021qsd",
        }
        # "Dembinski:2018ihc" is not in main.bib, because it is in foo.bib
        # "Baur:2019cpv" is not in main.bib, because it is in bar.bib

    assert subp.run(["bibtex", "foobarbaz"], cwd=tmpdir).returncode != 0


@pytest.mark.skipif(not find_in_path("latex"), reason="requires latex")
def test_autobib_updated_key(tmpdir):
    # test renamed key Abe:1993xy -> CDF:1993wpv

    with (tmpdir / "main.tex").open("w") as f:
        f.write(
            r"""
\documentclass{article}
\begin{document}
\cite{Abe:1993xy}
\bibliographystyle{plain}
\bibliography{main}
\end{document}
"""
        )

    with (tmpdir / "main.bib").open("w") as f:
        f.write("")

    subp.run(["latex", "main.tex"], cwd=tmpdir)
    assert (tmpdir / "main.aux").exists()
    p = subp.run(["bibtex", "main"], cwd=tmpdir, stderr=subp.PIPE)
    assert p.returncode == 1
    # autobib deletes the aux file in this case, to force latex to re-create it next time
    assert not (tmpdir / "main.aux").exists()

    with open(tmpdir / "main.bib") as f:
        assert get_bib_keys(f.read()) == {"CDF:1993wpv"}

    assert (
        b"""Error: Keys need update in LaTeX document
  Abe:1993xy -> CDF:1993wpv
"""
        in p.stderr
    )
