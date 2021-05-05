# autobib

Automatically generate and manage a BibTeX file.

## Usage

`autobib` wraps the `bibtex` command. Call `autobib` instead of `bibtex` with the same arguments. `autobib` will fetch citation keys that were added to the LaTeX document but are not yet in the `.bib` file automatically from [Inspire](https://inspirehep.net/).

For this to work, the citation key has to be the Inspire key.

## Planned features

- Also fetch from [adsabs](https://ui.adsabs.harvard.edu/)
- Smart-detect duplicates with some similarity metric, e.g. if the same paper is cited once using the adsabs key and once using the Inspire key
