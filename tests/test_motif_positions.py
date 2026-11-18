import pytest
from locusloom.motif_finder import (
    find_motif_positions,
    scan_both_strands,
    iupac_to_regex,
    find_degenerate_motifs,
    scan_degenerate_both_strands,
    build_pwm,
    score_sequence_with_pwm,
    scan_with_pwm,
)


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


def test_iupac_to_regex():
    assert iupac_to_regex("TATAWAW") == "TATA[AT]A[AT]"
    with pytest.raises(ValueError):
        iupac_to_regex("TATAZ")


def test_find_degenerate_motifs():
    seq = "GGTATAAAACCCTATATAAGG"
    assert find_degenerate_motifs(seq, "TATAWAW") == [
        (3, "TATAAAA"),
        (13, "TATATAA"),
    ]


def test_scan_degenerate_both_strands():
    # Forward 'GAATTC' is also 'GAATTC' on reverse complement
    hits = scan_degenerate_both_strands("ATGAATTCGC", "GAATTC")
    assert hits["forward"] == [(3, "GAATTC")]
    assert hits["reverse"] == [(3, "GAATTC")]


def test_build_pwm_scores_and_validation():
    motifs = ["ATG", "ATG", "ACG", "TTG"]
    pwm = build_pwm(motifs, pseudocount=1.0)

    # Position 1: A=3/4 -> (3+1)/8 = 0.5 -> log2(0.5/0.25) = 1.0
    assert pwm[0]["A"] == pytest.approx(1.0)
    assert pwm[0]["C"] == pytest.approx(-1.0)
    assert pwm[0]["T"] == pytest.approx(0.0)

    with pytest.raises(ValueError):
        build_pwm([])
    with pytest.raises(ValueError):
        build_pwm(["ATG", "ATGC"])  # Mismatched motif lengths


def test_score_and_scan_with_pwm():
    motifs = ["ATG", "ATG", "ACG", "TTG"]
    pwm = build_pwm(motifs, pseudocount=1.0)

    # Consensus 'ATG' gets highest positive score
    assert score_sequence_with_pwm("ATG", pwm) == pytest.approx(3.321928, rel=1e-4)

    hits = scan_with_pwm("CCATGGTA", pwm, threshold=2.0)
    assert len(hits) == 1
    assert hits[0][0] == 3
    assert hits[0][1] == "ATG"
    assert hits[0][2] == pytest.approx(3.3219, rel=1e-4)