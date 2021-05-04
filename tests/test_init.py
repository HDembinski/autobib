import requests
from pkg_resources import parse_version


def test_local_against_pypi_version():
    from autobib import __version__

    # make sure version is up-to-date
    pypi_versions = [
        parse_version(v)
        for v in requests.get("https://pypi.org/pypi/autobib/json").json()["releases"]
    ]
    assert parse_version(__version__) not in pypi_versions, "pypi version exists"
