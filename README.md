# LocusLoom

[![Version](https://img.shields.io/badge/Version-0.4.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/License-GPL--3.0-lightgrey.svg)](LICENSE)
[![Contributing](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

**LocusLoom** is a lightweight, modular Python bioinformatics toolkit and command-line interface (`locusloom`) for nucleotide sequence analysis, codon translation, Open Reading Frame (ORF) detection, and motif discovery.

---

## Key Features

- **Core Sequence Analysis (`locusloom.seq_core`):**
  - **GC Content Calculation:** Compute nucleotide GC percentage with automatic case normalization and empty-sequence safeguards.
  - **DNA-to-mRNA Transcription:** Transcribe `5'->3'` coding DNA strands into mRNA transcripts.
  - **Reverse Complement Generation:** Generate `5'->3'` reverse-complementary DNA sequences.
  - **mRNA Codon Translation:** Translate mRNA transcripts into amino acid sequences with automatic termination at stop codons (`UAA`, `UAG`, `UGA`).
  - **ORF Detection & FASTA Parsing:** Identify forward-strand Open Reading Frames (`find_orfs`) and inspect multi-record `.fasta`/`.fa` files (`read_fasta`).
- **Motif Discovery & PWM Engine (`locusloom.motif_finder`):**
  - **Exact & IUPAC Degenerate Scanning:** Locate overlapping exact motifs or ambiguous IUPAC patterns (e.g., `TATAWAW`) across forward and reverse strands.
  - **Position Weight Matrix (PWM) Scoring:** Build log-odds PWMs from aligned binding sites (`build_pwm`) and scan sequences using sliding-window thresholds (`scan_with_pwm`).
- **Dual CLI Modes (Direct & Interactive REPL):** Run single commands with short aliases (`gc`, `tr`, `rc`, `tl`, `mt`, `pwm`, `orf`, `fa`) or launch `locusloom` with no arguments to enter an interactive `locusloom>` shell.

---

## Installation

Clone the repository and install `locusloom` locally using `pip`:

```bash
git clone https://github.com/ekanshkaul/LocusLoom.git
cd LocusLoom
pip install -e .
```

---

## Quick Usage

### Command-Line Interface (`locusloom`)

```bash
# Calculate GC percentage
locusloom gc ATGTTTGGTTAA
# GC Content: 25.00%

# Transcribe DNA to mRNA (alias: tr)
locusloom transcribe ATGTTTGGTTAA
# AUGUUUGGUUAA

# Generate reverse complement (alias: rc)
locusloom revcomp ATGTTTGGTTAA
# TTAACCAAACAT

# Translate mRNA into amino acids (alias: tl)
locusloom translate AUGUUUGGUUAA
# MFG

# Scan both strands for an IUPAC degenerate motif (alias: mt)
locusloom motif GGTATAAAACCCTATATAAGG TATAWAW -b

# Build a PWM from aligned FASTA motifs and scan a sequence
locusloom pwm CCATGGTA -m binding_sites.fasta -t 2.0

# Launch the interactive REPL shell
locusloom
```

Run `locusloom --help` or `locusloom <subcommand> --help` to inspect all available flags and aliases.

### Python API

```python
import locusloom

seq = "ATGTTTGGTTAA"
gc = locusloom.calculate_gc_content(seq)
mrna = locusloom.transcribe_dna(seq)
protein = locusloom.translate_rna(mrna)

# IUPAC degenerate motif search
hits = locusloom.find_degenerate_motifs("GGTATAAAACCCTATATAAGG", "TATAWAW")

# PWM construction and sliding-window scan
pwm = locusloom.build_pwm(["ATG", "ATG", "ACG", "TTG"])
pwm_hits = locusloom.scan_with_pwm("CCATGGTA", pwm, threshold=2.0)
```

---

## Running Tests

LocusLoom uses `pytest` for automated unit testing across core sequence operations and motif finders:

```bash
pytest
```

---

## Repository Structure

```text
.
├── src/
│   └── locusloom/         # Core package source (seq_core, motif_finder, CLI)
├── tests/                 # Automated pytest unit test suites
├── .gitignore             # Git ignore rules for virtual environments and caches
├── CHANGELOG.md           # Semantic Versioning release history
├── CITATION.cff           # Machine-readable software citation metadata
├── CONTRIBUTING.md        # Contribution guidelines, coding standards, and PR workflow
├── LICENSE                # GNU GPL-3.0 license
├── pyproject.toml         # Package metadata, dependencies, and CLI entrypoint
├── README.md              # Project overview, installation, and quickstart guide
└── requirements.txt       # Development and runtime dependencies
```

---

## Release History

All notable changes and release notes are documented in [`CHANGELOG.md`](CHANGELOG.md).

## Contributing

Contributions from developers, researchers, and students of all experience levels are welcome. Please review [`CONTRIBUTING.md`](CONTRIBUTING.md) for local environment setup, testing expectations, and pull request guidelines.