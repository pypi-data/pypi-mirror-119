# WikiTools
![Travis Build](https://api.travis-ci.com/machinexa2/WikiTools.svg?branch=master)

## Description
### WikiFiller
WikiFiller generates and fills templates of Wikipedia with ease. It does all the stuff behind the scenes using selenium and other modules so you don't have to.
<hr>
### WikiFinder
WikiFinder finds other isomers of molecular formula based on compound name and directly. Atoms changes is also available for given molecular formula. (It isn't much use of normal wiki editing)

## Installation
* `pip install wiki-tools`
* `python3 setup.py install`

## Usage
### WikiFillder
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
<hr>
### WikiFinder
```
usage: WikiFinder [-h] [-m MOLECULAR_FORMULA | -n NAME] [-c [CHANGE ...]]
                  [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -m MOLECULAR_FORMULA, --molecular-formula MOLECULAR_FORMULA
                        Outputs list of chemicals from molecular formula
  -n NAME, --name NAME  Ouputs list of chemicals matching compound molecular
                        formula from name
  -c [CHANGE ...], --change [CHANGE ...]
                        Enter atom change of compound using spaces. '+'
                        increases atom while '_' decreases. Eg -c '_C1' '+H3'
  -o OUTPUT, --output OUTPUT
                        Enter output filename
```

## Example
### WikiFiller
1. Generate and fill chembox template of Ascorbic acid taken from (https://pubchem.ncbi.nlm.nih.gov/compound/Ascorbic-acid). The output is automatically copied to system clipboard
* ```WikiFiller -c -n 'Ascorbic-acid'```
2. Generate and fill drugbox template of Salvinorin A taken from (https://pubchem.ncbi.nlm.nih.gov/compound/Salvinorin-A) and generates output.
* ```WikiFiller -d -n 'Salvinorin-A' -o SalvinorinDraft```
<hr>
### WikiFinder
Later.

## Limitations
1. Might fetch wrong data or sometimes no data.
2. WikiFinder is in developmental stage
