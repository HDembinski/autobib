from autobib.io import parse
from pathlib import Path

cwd = Path(__file__).parent
test_document_path = cwd / "data"


def test_parse():
    d = {}
    for p in sorted(test_document_path.glob("*.bib")):
        with open(p) as f:
            d.update(parse(f.read()))

    assert list(d.keys()) == [
        "Baur:2019cpv",
        "Dembinski:2018ihc",
        "Aab:2021zfr",
        "Dembinski:2017kpa",
        "2001ICRC....3..985D",
    ]
