import subprocess as subp
import shutil
from pathlib import Path

cwd = Path(__file__).parent
test_document_path = cwd / "data"


def test_autobib(tmpdir):
    for fn in test_document_path.glob("*.*"):
        shutil.copy(fn, tmpdir)

    p = subp.run(["autobib", tmpdir / "main.aux"])
    assert p.returncode == 0
