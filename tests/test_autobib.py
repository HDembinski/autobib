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
            "Vanthieghem:2021akb",
            "Aab:2021zfr",
        }
        # "Dembinski:2018ihc" is not in main.bib, because it is in foo.bib
        # "Baur:2019cpv" is not in main.bib, because it is in bar.bib

    assert subp.run(["bibtex", "foobarbaz"], cwd=tmpdir).returncode != 0
