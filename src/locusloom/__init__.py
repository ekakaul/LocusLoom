"""LocusLoom: Modular bioinformatics toolkit for sequence analysis and motif discovery."""

from locusloom.seq_core import (
    calculate_gc_content,
    transcribe_dna,
    reverse_complement,
    translate_rna,
    read_fasta,
    find_orfs,
)
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

__version__ = "0.4.0"

__all__ = [
    "__version__",
    "calculate_gc_content",
    "transcribe_dna",
    "reverse_complement",
    "translate_rna",
    "read_fasta",
    "find_orfs",
    "find_motif_positions",
    "scan_both_strands",
    "iupac_to_regex",
    "find_degenerate_motifs",
    "scan_degenerate_both_strands",
    "build_pwm",
    "score_sequence_with_pwm",
    "scan_with_pwm",
]