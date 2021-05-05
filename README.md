# autobib

Automatically generate and manage a BibTeX file.

`autobib` will automatically fetch citation keys from online repositories that were added to the LaTeX document but not yet to the `.bib` file. The automatically fetched entries are added to the local `.bib` file for the next run. For this to work, the citation key has to be the Inspire key.

In essence, you still need to look up a citation online, but you don't have to add it twice, to your LaTeX document and to your `.bib` file. `autobib` does the latter for you.

## Installation and usage

`pip install autobib`

This installs a new script called `bibtex`, which is a drop-in replacement of the original `bibtex` command. The same name is chosen to make it work automatically with tooling like `latexmk`, which is otherwise hard to achieve.

Make sure that the `bibtex` script installed by `autobib` is found first by shell lookup. The path where the script is located must come first in the search paths listed by `PATH`, before the original `bibtex`.

## Planned features

- Also fetch from [adsabs](https://ui.adsabs.harvard.edu/)
- Smart-detect duplicates with some similarity metric, e.g. if the same paper is cited once using the adsabs key and once using the Inspire key
