from autobib import util
from pathlib import Path
import pytest

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
