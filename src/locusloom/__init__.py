"""LocusLoom: A modular bioinformatics toolkit for sequence analysis."""

__version__ = "0.3.0"

from .seq_core import (
    calculate_gc_content,
    transcribe_dna,
    reverse_complement,
    translate_rna,
)
from .motif_finder import (
    find_motif_positions,
    scan_both_strands,
)

__all__ = [
    "calculate_gc_content",
    "transcribe_dna",
    "reverse_complement",
    "translate_rna",
    "find_motif_positions",
    "scan_both_strands",
]