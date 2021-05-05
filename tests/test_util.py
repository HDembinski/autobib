from autobib import util
from pathlib import Path
import pytest
import shutil

cwd = Path(__file__).parent
test_document_path = cwd / "data"
aux_path = test_document_path / "main.aux"


def test_get_aux_path():

    with pytest.raises(ValueError):
        util.get_aux_path(Path("foobar"))

    assert util.get_aux_path(test_document_path) == aux_path
    assert util.get_aux_path(test_document_path / "main.aux") == aux_path
    assert util.get_aux_path(test_document_path / "main.tex") == aux_path


def test_get_aux_bibdata():
    bib_files = util.get_aux_bibdata(aux_path)

    assert bib_files == [test_document_path / "main.bib"]


def test_get_aux_citations():
    citations = util.get_aux_citations(aux_path)

    assert citations == {"Aab:2021zfr"}


def test_get_entry_online():
    key = "Aab:2021zfr"

    entry = util.get_entry_online(key)
    assert entry["collaboration"] == "Pierre Auger"


def test_replace_bib_files(tmpdir):
    bib = test_document_path / "main.bib"
    with open(bib) as f:
        db_ref = util.load(f)

    shutil.copy(bib, tmpdir / "main.bib")
    bib = Path(tmpdir / "main.bib")

    autobib_backup = Path(tmpdir / "main.bib-autobib-backup")
    assert not autobib_backup.exists()

    db = util.replace_bib_files({bib})

    assert db == db_ref
    assert autobib_backup.exists()
