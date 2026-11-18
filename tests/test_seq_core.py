import pytest
from locusloom.seq_core import (
    calculate_gc_content,
    transcribe_dna,
    reverse_complement,
    translate_rna,
    read_fasta,
    write_fasta,
    find_orfs,
)

#Testing the GC content calculations
def test_calculate_gc_content():
    assert calculate_gc_content("ATGC") == 50.0
    assert calculate_gc_content("GGCC") == 100.0
    assert calculate_gc_content("AATT") == 0.0
    assert calculate_gc_content("atgc") == 50.0  # Lowercase input
    assert calculate_gc_content("") == 0.0       # Empty string edge case

#Testing the DNA transcribe
def test_transcribe_dna():
    assert transcribe_dna("ATGTTT") == "AUGUUU"
    assert transcribe_dna("atgttt") == "AUGUUU"
    assert transcribe_dna("GCGC") == "GCGC"

#Testing the Reverse Complement
def test_reverse_complement():
    assert reverse_complement("ATGC") == "GCAT"
    assert reverse_complement("ATGTTTGGTTAA") == "TTAACCAAACAT"
    assert reverse_complement("atgc") == "GCAT"

#Testing the DNA Translation 
def test_translate_rna():
    #Standard translation stopping at UAA
    assert translate_rna("AUGUUUGGUUAA") == "MFG"
    #Codon not in starter table maps to 'X'
    assert translate_rna("AUGCCCUAA") == "MX"
    #Trailing incomplete codon (< 3 bases) is ignored
    assert translate_rna("AUGUUUGG") == "MF"
    #Lowercase input
    assert translate_rna("auguuugguuaa") == "MFG"

#Testing Fasta
def test_fasta_roundtrip(tmp_path):
    fasta_file = tmp_path / "sample.fasta"
    records = {
        "seq_01": "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGG",
        "seq_02": "ATGGCCATTGTAATGGGCCGCTGA",
    }
    write_fasta(str(fasta_file), records, line_width=20)
    assert read_fasta(str(fasta_file)) == records

def test_read_fasta_edge_cases(tmp_path):
    # Empty file returns empty dictionary
    empty_file = tmp_path / "empty.fasta"
    empty_file.write_text("", encoding="utf-8")
    assert read_fasta(str(empty_file)) == {}

    # Sequence before '>' header raises ValueError
    bad_file = tmp_path / "malformed.fasta"
    bad_file.write_text("ATGGTGCATCTG\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read_fasta(str(bad_file))

#Testing ORF
def test_find_orfs():
    # Frame-shifted DNA ORF (starts at index 1: ATG TTT GGT TAA)
    assert find_orfs("CATGTTTGGTTAA") == ["AUGUUUGGUUAA"]
    # Incomplete ORF (start codon with no stop codon) is discarded
    assert find_orfs("AUGUUUGGU") == []
    # Empty string edge case
    assert find_orfs("") == []