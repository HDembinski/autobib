from autobib import util
from autobib.util import Key
from pathlib import Path
import pytest

cwd = Path(__file__).parent
test_document_path = cwd / "data"
aux_path = test_document_path / "main.aux"


def test_get_bib_keys():
    with open(test_document_path / "main.bib") as f:
        keys = util.get_bib_keys(f.read())

    assert set(keys) == {
        Key(s)
        for s in (
            "PierreAuger:2021qsd",
            "Dembinski:2017kpa",
            "2001ICRC....3..985D",
            "Arnold2009",
            "REVTEX42Control",
            "apsrev42Control",
        )
    }


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
        Key(s)
        for s in (
            "2020Univ....6..102M",
            "Vanthieghem:2021akb",
            "Baur:2019cpv",
            "Aab:2021zfr",
            "Dembinski:2018ihc",
        )
    }


def test_get_aux_keys_bug():
    with pytest.raises(ValueError):
        util.get_aux_keys(test_document_path / "bug.aux")


def test_get_entry_online_1():
    key = Key("PierreAuger:2021qsd")

    key2, entry = util.get_entry_online(key)
    assert key == key2

    assert util.get_entry_online("foobarbaz") is None


def test_get_entry_online_2():
    key = Key("2011ApJ...737..103S")
    key2, entry = util.get_entry_online(key)
    assert key == key2
