import subprocess as subp
import shutil
from pathlib import Path

cwd = Path(__file__).parent
test_document_path = cwd / "data"


def test_autobib(tmpdir):
    for fn in test_document_path.glob("*.*"):
        shutil.copy(fn, tmpdir)

    subp.run(["latex", "main.tex"], cwd=tmpdir)
    p = subp.run(["autobib", "main"], cwd=tmpdir)
    assert p.returncode == 0
