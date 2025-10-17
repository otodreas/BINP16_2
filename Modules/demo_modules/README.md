# bio_utils

A Python package for DNA sequence analysis, designed for bioinformatics tasks.

## Installation
```bash
pip install .
```

## Usage
```python
from bio_utils.sequence_utils import clean_dna, gc_content
print(clean_dna('atcgXY'))  # Outputs: ATCGNN
print(gc_content('GCGC'))   # Outputs: 1.0
```

## Functions
- `clean_dna`: Standardize DNA sequences.
- `gc_content`: Calculate GC content.
- `revcomp`: Compute reverse complement.
- `count_base`: Count specific bases.
- `hamming`: Calculate Hamming distance.
- `kmer_counts`: Count k-mers.
- `find_motif`: Find motif positions.
- `base_counts`: Count all bases and sequence length.

## Running Tests
```bash
python -m unittest discover tests
```
