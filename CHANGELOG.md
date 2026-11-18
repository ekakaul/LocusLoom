# Changelog

All notable changes to **LocusLoom** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.4.0] - 2026-11-18

### Added
- **IUPAC Degenerate Motif Scanning (`locusloom.motif_finder`)**: Added `iupac_to_regex`, `find_degenerate_motifs`, and `scan_degenerate_both_strands` to match ambiguous nucleotide codes (`R`, `Y`, `W`, `S`, `K`, `M`, `B`, `D`, `H`, `V`, `N`) across both DNA strands with overlapping lookahead support.
- **Position Weight Matrix (PWM) Scoring**: Implemented `build_pwm` (log-odds scoring with configurable pseudocounts), `score_sequence_with_pwm`, and `scan_with_pwm` for sliding-window binding-site discovery.
- **ORF & FASTA Parsing Utilities (`locusloom.seq_core`)**: Added `find_orfs` for Open Reading Frame detection and `read_fasta` for multi-record FASTA parsing.
- **Interactive REPL Shell & Expanded CLI (`locusloom`)**: Added an interactive `locusloom>` shell mode alongside subcommand aliases (`tr`, `rc`, `tl`, `mt`, `orf`, `fa`) and the new `locusloom pwm` subcommand (`-m`, `-t`, `-z`).
- **Citation Metadata**: Added `CITATION.cff` for standardized academic software citation.

### Changed
- **Upgraded `locusloom motif` CLI Subcommand**: Upgraded `handle_motif` to support both exact and IUPAC degenerate patterns seamlessly with `-b` (both strands) and `-z` (0-based indexing).
- **Top-Level Package Exports (`locusloom.__init__`)**: Exported all Module 1 and Module 2 utilities under `__all__` and bumped `__version__` to `"0.4.0"`.

---

## [0.3.0] - 2026-11-14

### Added
- **Motif Finding Engine & CLI Integration**: Added sequence motif discovery utilities to identify, locate, and index recurring DNA/RNA patterns across biological sequences, exposed via both the Python API and the `locusloom` CLI.
- **Motif Unit Test Suite**: Added comprehensive `pytest` coverage (`tests/test_motif*.py`) validating exact motif matching, overlapping occurrences, case insensitivity, and empty/no-match edge cases.
- **Project Documentation Suite**: Added `CONTRIBUTING.md` establishing contribution workflows, branch/commit conventions, and PR checklists, and introduced `CHANGELOG.md` following Semantic Versioning.

### Changed
- **Streamlined `README.md`**: Refocused the main repository landing page on core bioinformatics capabilities, installation, Python/CLI quickstart usage, and repository architecture, delegating release history to `CHANGELOG.md`.

---

## [0.2.0] - 2026-11-13

### Added
- **Command-Line Interface (`locusloom`)**: Added an `argparse`-powered CLI with built-in usage examples (`locusloom --help`) and four subcommands:
  - `locusloom gc <sequence>` — Calculate GC percentage of a DNA/RNA sequence.
  - `locusloom transcribe <sequence>` — Transcribe coding DNA (`5'->3'`) into mRNA.
  - `locusloom revcomp <sequence>` — Generate the reverse complement (`5'->3'`) of a DNA strand.
  - `locusloom translate <sequence>` — Translate an mRNA sequence into amino acids, halting at stop codons (`UAA`, `UAG`, `UGA`).
- **Top-Level Package Exports**: Exposed core sequence functions directly under the `locusloom` namespace alongside `__version__ = "0.2.0"`.
- **Sequence Core Unit Test Suite**: Added automated unit tests in `tests/test_seq_core.py` covering GC content, transcription, reverse complement, translation, lowercase normalization, and edge cases.

### Fixed
- **Case Normalization & Empty Input Guard**: Updated `calculate_gc_content` to normalize lowercase inputs (`.upper()`) and safely return `0.0` for empty strings instead of raising a `ZeroDivisionError`.

---

## [0.1.0] - 2026-11-12

### Added
- **Installable Python Package Layout**: Initialized modern `pyproject.toml` packaging structure for `locusloom`.
- **Core Sequence Analysis Module (`locusloom.seq_core`)**: Implemented foundational bioinformatics utilities:
  - `calculate_gc_content` for nucleotide composition analysis.
  - `transcribe_dna` for DNA-to-mRNA transcription.
  - `reverse_complement` for complementary DNA strand generation.
  - `translate_rna` for standard genetic code mRNA codon translation.