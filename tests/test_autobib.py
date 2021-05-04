import subprocess as subp
import shutil
from pathlib import Path

cwd = Path(__file__).parent
test_document_path = cwd / "data"


def test_autobib(tmpdir):
    for fn in test_document_path.glob("*.*"):
        shutil.copy(fn, tmpdir)

    p = subp.Popen(["autobib", tmpdir])
    try:
        p.wait(timeout=0.5)  # should not abort
        assert False
    except subp.TimeoutExpired:
        pass
