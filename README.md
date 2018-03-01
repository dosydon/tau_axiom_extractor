# About
This repository contains the codes to find τ-axioms described in the paper "Automatic Extraction of Axioms in Planning".

# Dependencies
- psutil

## Lemon Graph Library 1.3.1

The program requires the lemon graph library to be installed globally.

- official site (http://lemon.cs.elte.hu/trac/lemon)

# Installation

```
git clone --recursive git@github.com:dosydon/tau_axiom_extractor.git
cd tau_axiom_extractor
cmake .
make
```

# Test
```
./test_all.sh
```

# How to Use

--candidate\_gen=opgraph runs the graph based algorithm described in the paper.
--candidate\_gen=top runs the variable based algorithm described in the paper.

```
usage: encode.py [-h] [--output OUTPUT] [--candidate_gen CANDIDATE_GEN]
                 sas_file

positional arguments:
  sas_file

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT
  --candidate_gen CANDIDATE_GEN
```
