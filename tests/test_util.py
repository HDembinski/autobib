from autobib import util
from pathlib import Path

cwd = Path(__file__).parent
test_document_path = cwd / "data"
aux_path = test_document_path / "main.aux"


def test_get_aux_bibdata():
    bib_files = util.get_aux_bibdata(aux_path)

    assert bib_files == [
        test_document_path / "main.bib",
        test_document_path / "foo.bib",
        test_document_path / "bar.bib",
    ]


def test_get_aux_keys():
    citations = util.get_aux_keys(aux_path)

    assert citations == {
        "2020Univ....6..102M",
        "Vanthieghem:2021akb",
        "Baur:2019cpv",
        "Aab:2021zfr",
        "Dembinski:2018ihc",
    }


def test_get_entry_online_1():
    key = "Aab:2021zfr"

    entry = util.get_entry_online(key)
    assert key in entry

    assert util.get_entry_online("foobarbaz") == ""


def test_get_entry_online_2():
    key = "2011ApJ...737..103S"
    entry = util.get_entry_online(key)
    assert key in entry

    assert util.get_entry_online("123foobarbaz") == ""
