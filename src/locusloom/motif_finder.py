"""Motif discovery and sequence pattern scanning utilities."""

from locusloom.seq_core import reverse_complement

def find_motif_positions(sequence: str, motif: str, one_based: bool = True) -> list[int]:
    """Find all starting positions (including overlapping) of a motif in a sequence.

    Args:
        sequence: Target DNA or RNA sequence.
        motif: Short nucleotide pattern to search for.
        one_based: Return 1-based genomic coordinates if True, else 0-based Python indices.

    Returns:
        List of starting positions where the motif occurs.
    """
    seq = sequence.upper()
    pat = motif.upper()

    if not seq or not pat or len(pat) > len(seq):
        return[]

    offset = 1 if one_based else 0
    positions = []

    for i in range(len(seq) - len(pat) +1):
        if seq[i : i + len(pat)] == pat:
            positions.append(i + offset)

    return positions

def scan_both_strands(sequence: str, motif: str, one_based: bool = True) -> dict[str, list[int]]:
    """Scan both the forward (5'->3') and reverse complement strands for a DNA motif."""
    forward_hits = find_motif_positions(sequence, motif, one_based=one_based)
    rev_seq = reverse_complement(sequence)
    reverse_hits = find_motif_positions(rev_seq, motif, one_based=one_based)

    return {
        "forward": forward_hits,
        "reverse": reverse_hits,
    }