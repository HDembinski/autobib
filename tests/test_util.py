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
