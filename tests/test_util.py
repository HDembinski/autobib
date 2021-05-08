from autobib import util
from pathlib import Path

cwd = Path(__file__).parent
test_document_path = cwd / "data"
aux_path = test_document_path / "main.aux"


def test_get_aux_bibdata():
    bib_files = util.get_aux_bibdata(aux_path)

    assert bib_files == [test_document_path / "main.bib"]


def test_get_aux_keys():
    citations = util.get_aux_keys(aux_path)

    assert citations == {"Aab:2021zfr", "Dembinski:2018ihc", "Baur:2019cpv"}


def test_get_entry_online():
    key = "Aab:2021zfr"

    entry = util.get_entry_online(key)
    assert key in entry

    assert util.get_entry_online("foobarbaz") == ""
