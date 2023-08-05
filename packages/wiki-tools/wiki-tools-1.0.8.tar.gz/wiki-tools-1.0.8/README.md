# WikiTools
![Travis Build](https://api.travis-ci.com/machinexa2/WikiTools.svg?branch=master)
## WikiFiller<hr>
## Description
WikiFiller generates and fills templates of Wikipedia with ease. It does all the stuff behind the scenes using selenium and other modules so you don't have to.

## Usage
```
usage: WikiFiller [-h] [-c | -d] [-n NAME] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -c, --chembox         Generates chembox
  -d, --drugbox         Generates drugbox
  -n NAME, --name NAME  Enter pubchem compound name from pubchem url
  -o OUTPUT, --output OUTPUT
                        Enter output filename
```

## Example
1. Generate and fill chembox template of Ascorbic acid taken from (https://pubchem.ncbi.nlm.nih.gov/compound/Ascorbic-acid). The output is automatically copied to system clipboard
* ```WikiFiller -c -n 'Ascorbic-acid'```
2. Generate and fill drugbox template of Salvinorin A taken from (https://pubchem.ncbi.nlm.nih.gov/compound/Salvinorin-A) and generates output.
* ```WikiFiller -d -n 'Salvinorin-A' -o SalvinorinDraft```

## Limitations
1. Might fetch wrong data or sometimes no data. Wrong data being rare while no data being common

## WikiFinder<hr>
## Description
Developmental
