# ediclean
A Python package to strip non-standard text blocks from UN/EDIFACT messages.

[![CircleCI](https://circleci.com/gh/janotaz/ediclean/tree/main.svg?style=shield&circle-token=709edaf489003821e0bd2209bacb8f5713097e58)](https://circleci.com/gh/janotaz/ediclean/tree/main)

<!-- ABOUT THE PROJECT -->
## About The Project
UN/EDIFACT files often contain headers and footers that are added by applications during their transport. Ediclean removes these non-standard blocks and formats the output to contain one segment per line.

## Installation 
```
pip3 install -U ediclean
```

## Usage
```shell
$ ediclean -h
usage: ediclean [-h] [filename]

Clean UN/EDIFACT PAXLST files from unsupported characters.

positional arguments:
  filename    File containing UN/EDIFACT PAXLST message

optional arguments:
  -h, --help  show this help message and exit

```

## Currently supported message types
- UN/EDIFACT PAXLST up to [v. D rel. 21A (2021-06-10)](https://service.unece.org/trade/untdid/latest/trmd/paxlst_c.htm)

<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE` for more information.
