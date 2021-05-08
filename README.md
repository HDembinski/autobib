# autobib

Automatically download new entries for your bibliography file.

`autobib` automatically fetches BibTeX entries from online databases (currently restricted to Inspire) based on references that were added to the LaTeX document but not yet to the `.bib` file. The automatically fetched entries are appended to the first `.bib` file defined in your LaTeX source (first entry of `\bibliography{...}`). For this to work, the cite key has to be a key used by the online database.

In other words, you still need to look up a citation online and copy the cite key to your LaTeX file, but you don't have to also copy the whole BibTeX entry to your local `.bib` file (essentially adding it twice), since `autobib` does the latter for you.

## Installation and usage

`pip install autobib`

This installs a new script called `bibtex`, which is a drop-in replacement of the original `bibtex` command. The same name is chosen to make it work automatically with tooling like `latexmk`, which is otherwise hard to achieve.

Make sure that the `bibtex` script installed by `autobib` is found first by shell lookup. The path where the script is located must come first in the search paths listed by `PATH`, before the original `bibtex`.

## Planned features

- Also fetch from [adsabs](https://ui.adsabs.harvard.edu/)
- Smart-detect duplicates with some similarity metric, e.g. if the same paper is cited once using the adsabs key and once using the Inspire key
