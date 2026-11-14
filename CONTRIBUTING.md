# Contributing to LocusLoom

Thank you for your interest in contributing to **LocusLoom**. We welcome contributions from developers, bioinformaticians, researchers, and students of all experience levels. Whether you are fixing an edge case in sequence parsing, adding a new motif-discovery algorithm, or improving documentation, your work helps make this toolkit more accurate and reliable.

Please review these guidelines before submitting your contributions.

---

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Types of Contributions](#types-of-contributions)
3. [Getting Started](#getting-started)
4. [Code & Testing Standards](#code--testing-standards)
5. [Branching & Commit Standards](#branching--commit-standards)
6. [Submitting a Pull Request](#submitting-a-pull-request)

---

## Code of Conduct

All contributors and maintainers are expected to uphold a respectful, constructive, and inclusive environment. Please engage professionally during issue discussions and code reviews, offer actionable feedback, and assume good intent.

---

## Types of Contributions

You can contribute to LocusLoom in several ways:

* **Bioinformatics & Sequence Algorithms:** Implement new sequence analysis utilities, motif finders, or scoring metrics within the core package modules.
* **CLI Enhancements:** Add or refine `argparse` subcommands, flags, and output formatting for the `locusloom` command-line interface.
* **Bug Reports & Edge Cases:** Report reproducible sequence-handling bugs (e.g., ambiguous IUPAC bases, lowercase inputs, or boundary conditions) with minimal test cases.
* **Testing & Quality Assurance:** Expand `pytest` coverage across `tests/` to strengthen reliability across edge cases.
* **Documentation:** Improve docstrings, CLI `--help` examples, or setup guides in `README.md`.

---

## Getting Started

1. **Fork and Clone the Repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/LocusLoom.git
   cd LocusLoom
   ```

2. **Configure Upstream Remote:**
   ```bash
   git remote add upstream https://github.com/ekanshkaul/LocusLoom.git
   ```

3. **Create a Virtual Environment & Install in Editable Mode:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"     # Or: pip install -e . pytest
   ```

4. **Run the Test Suite:**
   ```bash
   pytest
   ```

---

## Code & Testing Standards

* **Input Resilience:** Sequence functions should gracefully handle lowercase inputs, whitespace, and empty strings without unhandled exceptions (such as `ZeroDivisionError`).
* **Unit Tests Required:** All new algorithms, motif utilities, and bug fixes must include corresponding unit tests in `tests/` runnable via `pytest`.
* **Clean Public Exports:** Expose stable user-facing functions cleanly through `locusloom/__init__.py` and wire CLI subcommands consistently in the CLI entrypoint.

---

## Branching & Commit Standards

* **Create a Dedicated Branch:** Always branch off `main` using a descriptive prefix:
  * `feat/<short-description>` for new features or algorithms
  * `fix/<short-description>` for bug fixes
  * `test/<short-description>` for test suite additions
  * `docs/<short-description>` for documentation updates
* **Write Clear Commit Messages:** Use concise, imperative commit messages (e.g., `feat: add IUPAC degenerate motif matching` or `fix: handle lowercase RNA input in translate_rna`).

---

## Submitting a Pull Request

Before opening a Pull Request (PR), please verify the following checklist:

* [ ] All existing and newly added tests pass locally (`pytest`).
* [ ] Changes follow the existing package layout, naming conventions, and docstring style.
* [ ] Relevant documentation (`README.md` or CLI `--help` text) has been updated if user-facing behavior changed.
* [ ] Your PR description clearly explains **what** changed and **why**, referencing any related issues.

Once submitted, a maintainer will review your PR and provide feedback if adjustments are needed. Thank you for contributing to LocusLoom!