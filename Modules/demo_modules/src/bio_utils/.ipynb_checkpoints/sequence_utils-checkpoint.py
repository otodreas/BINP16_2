# demo_modules/src/bio_utils/sequence_utils.py
from collections import Counter

def clean_dna(seq: str) -> str:
    """Returns an uppercase DNA string with only A, C, G, T, N. Other characters, including spaces, become 'N'."""
    allowed = {'A', 'C', 'G', 'T', 'N'}
    cleaned = []
    for char in seq.upper():
        cleaned.append(char if char in allowed else 'N')
    return ''.join(cleaned)

def gc_content(seq: str) -> float:
    """Returns fraction of G and C bases (0.0 to 1.0), ignoring N."""
    s = clean_dna(seq)
    gc_count = s.count('G') + s.count('C')
    total = len(s) - s.count('N')
    return gc_count / total if total > 0 else 0.0

def revcomp(seq: str) -> str:
    """Returns the reverse complement of a DNA sequence."""
    s = clean_dna(seq)
    complement = str.maketrans('ACGTN', 'TGCAN')
    return s.translate(complement)[::-1]

def count_base(seq: str, base: str) -> int:
    """Returns count of a specific base (A, C, G, T, or N)."""
    s = clean_dna(seq)
    base = base.upper()
    if base not in {'A', 'C', 'G', 'T', 'N'}:
        raise ValueError("Base must be A, C, G, T, or N")
    return s.count(base)

def hamming(a: str, b: str) -> int:
    """Returns number of differing positions (equal length required)."""
    sa = clean_dna(a)
    sb = clean_dna(b)
    if len(sa) != len(sb):
        raise ValueError("Sequences must have equal length")
    return sum(1 for x, y in zip(sa, sb) if x != y)

def kmer_counts(seq: str, k: int) -> dict:
    """Returns dictionary of k-mer frequencies (overlapping, skips N)."""
    if k <= 0:
        raise ValueError("k must be positive")
    s = clean_dna(seq)
    counts = {}
    for i in range(len(s) - k + 1):
        kmer = s[i:i+k]
        if 'N' in kmer:
            continue
        counts[kmer] = counts.get(kmer, 0) + 1
    return counts

def find_motif(seq: str, motif: str) -> list:
    """Returns 0-based start positions of exact motif matches."""
    s = clean_dna(seq)
    m = clean_dna(motif)
    if not m:
        return []
    k = len(m)
    positions = []
    for i in range(len(s) - k + 1):
        if s[i:i+k] == m:
            positions.append(i)
    return positions

def base_counts(seq: str) -> dict:
    """Returns counts of A, C, G, T, N and total length ('LEN')."""
    s = clean_dna(seq)
    counts = Counter(s)
    counts['LEN'] = len(s)
    defaults = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'N': 0, 'LEN': len(s)}
    defaults.update(counts)
    return defaults