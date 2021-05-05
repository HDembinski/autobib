import subprocess as subp
import shutil
from pathlib import Path
import pytest

cwd = Path(__file__).parent
test_document_path = cwd / "data"


@pytest.mark.skipif(
    subp.run(["latex", "--version"]).returncode != 0, reason="requires latex"
)
def test_autobib(tmpdir):
    shutil.copy(test_document_path / "main.tex", tmpdir / "main.tex")

    subp.run(["latex", "main.tex"], cwd=tmpdir)
    p = subp.run(["bibtex", "main"], cwd=tmpdir)
    assert p.returncode == 0
