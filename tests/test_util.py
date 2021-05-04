from autobib import util
from pathlib import Path
import pytest
import shutil

cwd = Path(__file__).parent
test_document_path = cwd / "test_document"
aux_path = test_document_path / "main.aux"


def test_get_aux_path():

    with pytest.raises(ValueError):
        util.get_aux_path(Path("foobar"))

    assert util.get_aux_path(test_document_path) == aux_path
    assert util.get_aux_path(test_document_path / "main.aux") == aux_path
    assert util.get_aux_path(test_document_path / "main.tex") == aux_path


def test_scan_aux():
    bib_files, citations = util.scan_aux(aux_path)

    assert bib_files == {test_document_path / "main.bib"}
    assert citations == {"Aab:2021zfr"}


def test_replace_bib_files(tmpdir):
    bib = test_document_path / "main.bib"
    with open(bib) as f:
        db_ref = util.load(f)

    shutil.copy(bib, tmpdir / "main.bib")
    bib = tmpdir / "main.bib"

    autobib_backup = tmpdir / "main.bib-autobib-backup"
    assert not autobib_backup.exists()

    with util.replace_bib_files({bib}, {}):
        pass

    assert autobib_backup.exists()

    with open(bib) as f:
        assert util.load(f) == db_ref
