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
``` shell
$ ediclean -h
usage: ediclean [-h] [filename]

Clean UN/EDIFACT PAXLST files from unsupported characters.

positional arguments:
  filename    File containing UN/EDIFACT PAXLST message

optional arguments:
  -h, --help  show this help message and exit
```

### Examples

Original file
``` shell
$ cat ediclean/tests/testfiles/original/A.txt
CICA	 

.HDQCRA9 130631
UNA:+.? 'UNB+UNOA:4+CICA-A9:A9+ABCAPIS:ZZ+210713:0631+2107130631
++APIS'UNG+PAXLST+CICA-A9:ZZ+ABCAPIS:ZZ+210713:0631+1+UN+D:05B'U
NH+PAX001+PAXLST:D:05B:UN:IATA+A92707/210713/1200+02'BGM+745'NAD
+MS+++CICA HELP DESK'COM+231384 373 2:TE+1 232 3234 4:FX'TDT+20+
A92707'LOC+125+VIE'DTM+189:2107131100:201'LOC+87+VIE'DTM+232:210
7131200:201'NAD+FL+++DJEMFISJER:REDJAE'ATT+2++M'DTM+329:930408'M
EA+CT++:0'FTX+BAG+++NULL'LOC+22+VIE'LOC+178+TBS'LOC+179+VIE'NAT+
2+ABC'RFF+AVF:ABC123'RFF+SEA:9F'DOC+P:110:111+3DEJ2ED3E'DTM+36:28
0907'LOC+91+LIM'CNT+42:4
7'UNT+159+PAX001'UNE+1+1'UNZ+1+2107130631'



Email secured by UN Antivirus

```

Cleansed file
``` shell
$ ediclean ediclean/tests/testfiles/original/A.txt 
UNA:+.? '
UNB+UNOA:4+CICA-A9:A9+ABCAPIS:ZZ+210713:0631+2107130631++APIS'
UNG+PAXLST+CICA-A9:ZZ+ABCAPIS:ZZ+210713:0631+1+UN+D:05B'
UNH+PAX001+PAXLST:D:05B:UN:IATA+A92707/210713/1200+02'
BGM+745'
NAD+MS+++CICA HELP DESK'
COM+231384 373 2:TE+1 232 3234 4:FX'
TDT+20+A92707'
LOC+125+VIE'
DTM+189:2107131100:201'
LOC+87+VIE'
DTM+232:2107131200:201'
NAD+FL+++DJEMFISJER:REDJAE'
ATT+2++M'
DTM+329:930408'
MEA+CT++:0'
FTX+BAG+++NULL'
LOC+22+VIE'
LOC+178+TBS'
LOC+179+VIE'
NAT+2+ABC'
RFF+AVF:ABC123'
RFF+SEA:9F'
DOC+P:110:111+3DEJ2ED3E'
DTM+36:280907'
LOC+91+LIM'
CNT+42:47'
UNT+159+PAX001'
UNE+1+1'
UNZ+1+2107130631'

```

## Currently supported message types
- UN/EDIFACT PAXLST up to [v. D rel. 21A (2021-06-10)](https://service.unece.org/trade/untdid/latest/trmd/paxlst_c.htm)

<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE` for more information.
