# autobib

Automatically generate and manage a BibTeX file.

## Notes

- Need to monitor tex file, since aux file may be deleted
  immediately and we cannot react fast enough
- We cannot replace .bib files with blocking fifos, because
  Atom tries to read all files in a directory frequently
