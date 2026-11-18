"""Motif discovery and sequence pattern scanning utilities."""

import math
import re
from locusloom.seq_core import reverse_complement

IUPAC_TO_REGEX = {
    "A": "A", "C": "C", "G": "G", "T": "T", "U": "U",
    "R": "[AG]", "Y": "[CT]", "S": "[GC]", "W": "[AT]",
    "K": "[GT]", "M": "[AC]", "B": "[CGT]", "D": "[AGT]",
    "H": "[ACT]", "V": "[ACG]", "N": "[ACGT]",
}


def find_motif_positions(sequence: str, motif: str, one_based: bool = True) -> list[int]:
    """Find all exact starting positions of a motif (including overlapping hits)."""
    seq = sequence.upper()
    pat = motif.upper()
    if not seq or not pat or len(pat) > len(seq):
        return []

    offset = 1 if one_based else 0
    positions: list[int] = []
    start = 0
    while True:
        idx = seq.find(pat, start)
        if idx == -1:
            break
        positions.append(idx + offset)
        start = idx + 1
    return positions


def scan_both_strands(sequence: str, motif: str, one_based: bool = True) -> dict[str, list[int]]:
    """Scan both forward and reverse complement strands for an exact DNA motif."""
    return {
        "forward": find_motif_positions(sequence, motif, one_based=one_based),
        "reverse": find_motif_positions(reverse_complement(sequence), motif, one_based=one_based),
    }


def iupac_to_regex(motif: str) -> str:
    """Convert an IUPAC nucleotide motif string into a regex pattern."""
    pattern_parts: list[str] = []
    for base in motif.upper():
        if base not in IUPAC_TO_REGEX:
            raise ValueError(f"Invalid IUPAC nucleotide character: '{base}'")
        pattern_parts.append(IUPAC_TO_REGEX[base])
    return "".join(pattern_parts)


def find_degenerate_motifs(
    sequence: str, motif: str, one_based: bool = True
) -> list[tuple[int, str]]:
    """Find all (position, matched_subsequence) hits for an IUPAC motif."""
    seq = sequence.upper()
    if not seq or not motif:
        return []

    regex_pattern = iupac_to_regex(motif)
    lookahead = re.compile(f"(?=({regex_pattern}))")
    offset = 1 if one_based else 0

    return [
        (match.start() + offset, match.group(1))
        for match in lookahead.finditer(seq)
    ]


def scan_degenerate_both_strands(
    sequence: str, motif: str, one_based: bool = True
) -> dict[str, list[tuple[int, str]]]:
    """Scan both forward and reverse complement strands for an IUPAC motif."""
    return {
        "forward": find_degenerate_motifs(sequence, motif, one_based=one_based),
        "reverse": find_degenerate_motifs(reverse_complement(sequence), motif, one_based=one_based),
    }


def build_pwm(
    aligned_motifs: list[str], pseudocount: float = 1.0
) -> list[dict[str, float]]:
    """Build a log-odds Position Weight Matrix (PWM) from aligned DNA motifs."""
    if not aligned_motifs:
        raise ValueError("aligned_motifs cannot be empty.")

    motif_len = len(aligned_motifs[0])
    if any(len(seq) != motif_len for seq in aligned_motifs):
        raise ValueError("All aligned motifs must have the same length.")

    num_seqs = len(aligned_motifs)
    denominator = num_seqs + 4 * pseudocount
    pwm: list[dict[str, float]] = []

    for pos in range(motif_len):
        counts = {"A": 0, "C": 0, "G": 0, "T": 0}
        for seq in aligned_motifs:
            base = seq[pos].upper()
            if base not in counts:
                raise ValueError(f"Invalid DNA base '{base}' at position {pos}.")
            counts[base] += 1

        scores = {
            base: math.log2(((count + pseudocount) / denominator) / 0.25)
            for base, count in counts.items()
        }
        pwm.append(scores)

    return pwm


def score_sequence_with_pwm(sequence: str, pwm: list[dict[str, float]]) -> float:
    """Calculate the log-odds score of a fixed-length sequence window against a PWM."""
    if len(sequence) != len(pwm):
        raise ValueError("Sequence length must match PWM length.")

    total_score = 0.0
    for i, base in enumerate(sequence.upper()):
        if base not in pwm[i]:
            raise ValueError(f"Invalid DNA base '{base}' at position {i}.")
        total_score += pwm[i][base]
    return total_score


def scan_with_pwm(
    sequence: str,
    pwm: list[dict[str, float]],
    threshold: float = 0.0,
    one_based: bool = True,
) -> list[tuple[int, str, float]]:
    """Slide a PWM across a sequence and return (position, window, score) hits >= threshold."""
    seq = sequence.upper()
    motif_len = len(pwm)
    if not seq or motif_len == 0 or len(seq) < motif_len:
        return []

    offset = 1 if one_based else 0
    hits: list[tuple[int, str, float]] = []

    for i in range(len(seq) - motif_len + 1):
        window = seq[i : i + motif_len]
        score = score_sequence_with_pwm(window, pwm)
        if score >= threshold:
            hits.append((i + offset, window, round(score, 4)))

    return hits