# Fair Division with Indivisible Items

A library with algorithms for fair division with indivisible items.

## Installation
After cloning the repository, run the following command in the main directory:

    pip install -r requirements.txt


## Usage
Edit and run `fairdivision/main.py` script:

    python fairdivision/main.py


## Type checking
Run the following in the main directory:

    mypy fairdivision/main.py


## Running tests
Run the following in the main directory:

    python -m pytest


## Instances
Instances of the discrete fair division problem in `instances` directory follow the following standard.

- The first line specifies restrictions on valuations as a space separated strings. Only `additive` is supported now.
- The second line should contain 2 integers separated by a space. First one is the number of agents (n), and the second one is the number of items (m).
- The next n lines contain m integers separated by spaces. Each j-th number in (i+2)-th line represents i-th agent's valuation for j-th item.
- Lines containing `#` symbol or with only whitespace characters are not considered during the parsing.
