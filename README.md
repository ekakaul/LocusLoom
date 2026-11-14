# LocusLoom

[![Version](https://img.shields.io/badge/Version-0.3.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/License-Open%20Source-lightgrey.svg)](LICENSE)
[![Contributing](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

**LocusLoom** is a lightweight, modular Python bioinformatics toolkit and command-line interface (`locusloom`) for nucleotide sequence analysis, codon translation, and sequence motif discovery.

---

## Key Features

- **Core Sequence Analysis (`locusloom.seq_core`):**
  - **GC Content Calculation:** Compute nucleotide GC percentage with automatic case normalization and empty-sequence safeguards.
  - **DNA-to-mRNA Transcription:** Transcribe `5'->3'` coding DNA strands into mRNA transcripts.
  - **Reverse Complement Generation:** Generate `5'->3'` reverse-complementary DNA sequences.
  - **mRNA Codon Translation:** Translate mRNA transcripts into amino acid sequences with automatic termination at stop codons (`UAA`, `UAG`, `UGA`).
- **Motif Discovery Engine:** Identify and locate recurring sequence motifs across DNA/RNA inputs via both the Python library API and CLI.
- **Unified Python API & CLI:** Use functions directly via `import locusloom` or run fast terminal workflows using the `locusloom` CLI.

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

# Transcribe DNA to mRNA
locusloom transcribe ATGTTTGGTTAA
# AUGUUUGGUUAA

# Generate reverse complement
locusloom revcomp ATGTTTGGTTAA
# TTAACCAAACAT

# Translate mRNA into amino acids
locusloom translate AUGUUUGGUUAA
# MFG
```

Run `locusloom --help` or `locusloom <subcommand> --help` to inspect all available flags and motif-finding commands.

### Python API

```python
import locusloom

seq = "ATGTTTGGTTAA"
gc = locusloom.calculate_gc_content(seq)
mrna = locusloom.transcribe_dna(seq)
protein = locusloom.translate_rna(mrna)
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
│   └── locusloom/         # Core package source (seq_core, motif finders, CLI)
├── tests/                 # Automated pytest unit test suites
├── .gitignore             # Git ignore rules for virtual environments and caches
├── CHANGELOG.md           # Semantic Versioning release history
├── CONTRIBUTING.md        # Contribution guidelines, coding standards, and PR workflow
├── LICENSE                # Project license
├── pyproject.toml         # Package metadata, dependencies, and CLI entrypoint
├── README.md              # Project overview, installation, and quickstart guide
└── requirements.txt       # Development and runtime dependencies
```

---

## Release History

All notable changes and release notes are documented in [`CHANGELOG.md`](CHANGELOG.md).

## Contributing

Contributions from developers, researchers, and students of all experience levels are welcome. Please review [`CONTRIBUTING.md`](CONTRIBUTING.md) for local environment setup, testing expectations, and pull request guidelines.