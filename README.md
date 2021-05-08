# autobib

![PyPI](https://img.shields.io/pypi/v/autobib)
![PyPI - License](https://img.shields.io/pypi/l/autobib)
![PyPI - Status](https://img.shields.io/pypi/status/autobib)

`autobib` automatically fetches BibTeX entries from online databases (currently Inspire and ADS) based on references that were added to the LaTeX document but not yet to the `.bib` file. The automatically fetched entries are appended to the first `.bib` file defined in your LaTeX source (first entry of `\bibliography{...}`). For this to work, the cite key has to be a key used by the online database.

In other words, you still need to look up a citation online and copy the cite key to your LaTeX file, but you don't have to also copy the whole BibTeX entry to your local `.bib` file (essentially adding it twice), since `autobib` does the latter for you.

`autobib` only appends new entries to your `.bib` file and otherwise leaves it as is. Using it is therefore safe.

## Installation and usage

`pip install autobib`

This installs a new script called `bibtex`, which is a drop-in replacement of the original `bibtex` command. The same name is chosen to make it work automatically with tooling like `latexmk`, which is otherwise hard to achieve.

Make sure that the `bibtex` script installed by `autobib` is found first by shell lookup. The path where the script is located must come first in the search paths listed by `PATH`, before the original `bibtex`.

### ADS token

No extra steps are needed to download from Inspire, but to download from ADS you need to [follow these instructions](https://github.com/adsabs/adsabs-dev-api#access) to get an API token. Export this token in your shell as ADS_TOKEN, e.g. `export ADS_TOKEN=<insert token here>`.

## Planned features

- Smart-detect duplicates with some similarity metric, e.g. if the same paper is cited once using the adsabs key and once using the Inspire key
