# demo_modules/tests/test_sequence_utils.py
import unittest
from bio_utils.sequence_utils import (
    clean_dna, gc_content, revcomp, count_base, hamming,
    kmer_counts, find_motif, base_counts
)

class TestSequenceUtils(unittest.TestCase):
    def test_clean_dna(self):
        self.assertEqual(clean_dna('acgtRY'), 'ACGTNN')
        self.assertEqual(clean_dna(''), '')
        self.assertEqual(clean_dna('ACGT'), 'ACGT')
        self.assertEqual(clean_dna('XYZ123'), 'NNNNNN')
        self.assertEqual(clean_dna('AT CG N'), 'ATNCGNN')

    def test_gc_content(self):
        self.assertAlmostEqual(gc_content('GCGC'), 1.0)
        self.assertAlmostEqual(gc_content('GCGCAAA'), 4/7)
        self.assertEqual(gc_content('NNNN'), 0.0)
        self.assertEqual(gc_content(''), 0.0)
        self.assertAlmostEqual(gc_content('GCxyGC'), 1.0)

    def test_revcomp(self):
        self.assertEqual(revcomp('ATGC'), 'GCAT')
        self.assertEqual(revcomp('ATGCNN'), 'NNGCAT')
        self.assertEqual(revcomp(''), '')
        self.assertEqual(revcomp('atXYgc'), 'GCNNAT')
        self.assertEqual(revcomp('A'), 'T')

    def test_count_base(self):
        self.assertEqual(count_base('AAGCT', 'A'), 2)
        self.assertEqual(count_base('AAGCT', 'N'), 0)
        self.assertEqual(count_base('', 'A'), 0)
        self.assertEqual(count_base('XYZA', 'A'), 1)
        with self.assertRaises(ValueError):
            count_base('ACGT', 'X')

    def test_hamming(self):
        self.assertEqual(hamming('ACGT', 'ACGA'), 1)
        self.assertEqual(hamming('ACGT', 'ACGT'), 0)
        self.assertEqual(hamming('axyz', 'ACGT'), 3)
        with self.assertRaises(ValueError):
            hamming('ACG', 'ACGT')
        self.assertEqual(hamming('', ''), 0)

    def test_kmer_counts(self):
        self.assertEqual(kmer_counts('ACGTCG', 2), {'AC': 1, 'CG': 2, 'GT': 1, 'TC': 1})
        self.assertEqual(kmer_counts('ACGT', 5), {})
        self.assertEqual(kmer_counts('ACGN', 2), {'AC': 1, 'CG': 1})
        self.assertEqual(kmer_counts('', 1), {})
        with self.assertRaises(ValueError):
            kmer_counts('ACGT', 0)

    def test_find_motif(self):
        self.assertEqual(find_motif('ACGTCG', 'CG'), [1, 4])
        self.assertEqual(find_motif('ACGT', 'GT'), [2])
        self.assertEqual(find_motif('ACGT', ''), [])
        self.assertEqual(find_motif('ACGN', 'CG'), [1])
        self.assertEqual(find_motif('', 'CG'), [])

    def test_base_counts(self):
        self.assertEqual(base_counts('ACGTN'), {'A': 1, 'C': 1, 'G': 1, 'T': 1, 'N': 1, 'LEN': 5})
        self.assertEqual(base_counts(''), {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'N': 0, 'LEN': 0})
        self.assertEqual(base_counts('xyz'), {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'N': 3, 'LEN': 3})
        self.assertEqual(base_counts('acGT'), {'A': 1, 'C': 1, 'G': 1, 'T': 1, 'N': 0, 'LEN': 4})
        self.assertEqual(base_counts('AT CG'), {'A': 1, 'C': 1, 'G': 1, 'T': 1, 'N': 1, 'LEN': 5})

if __name__ == '__main__':
    unittest.main()