from locusloom.motif_finder import find_motif_positions, scan_both_strands

def test_overlapping_motifs():
    assert find_motif_positions("ATATATA", "ATA") == [1, 3, 5]

def test_zero_based_coordinates():
    assert find_motif_positions("ATATATA", "ATA", one_based=False) == [0, 2, 4]

def test_case_insensitivity():
    assert find_motif_positions("AtAtAtA", "ata") == [1, 3, 5]

def test_edge_cases():
    assert find_motif_positions("ATGC", "GGGG") == []      # Not found
    assert find_motif_positions("", "ATG") == []          # Empty sequence
    assert find_motif_positions("ATGC", "") == []         # Empty motif
    assert find_motif_positions("AT", "ATGC") == []       # Motif longer than sequence

def test_scan_both_strands():
    result = scan_both_strands("ATGCGTTA", "TAAC")
    assert result == {
        "forward": [],
        "reverse": [1],
    }