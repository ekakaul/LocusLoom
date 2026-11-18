"""Command-line interface for LocusLoom."""

import argparse
import shlex
import sys
from locusloom.seq_core import (
    calculate_gc_content,
    transcribe_dna,
    reverse_complement,
    translate_rna,
    read_fasta,
    find_orfs,
)
from locusloom.motif_finder import (
    find_degenerate_motifs,
    scan_degenerate_both_strands,
    build_pwm,
    scan_with_pwm,
)

WELCOME_BANNER = """============================================================
  LocusLoom v0.4.0
  Bioinformatics Sequence Toolkit
============================================================
  Quick Commands (Aliases):
    gc <seq>                        Calculate GC percentage
    tr <seq>         (transcribe)   Transcribe coding DNA to mRNA
    rc <seq>         (revcomp)      Get reverse complement (5'->3')
    tl <seq>         (translate)    Translate mRNA to protein
    mt <seq> <motif> [-b] [-z] (motif) Scan for exact/IUPAC motifs
    pwm <seq> -m <fa> [-t <score>] [-z] Scan sequence using a PWM
    orf <seq>        (orfs)         Find forward Open Reading Frames
    fa <file>        (fasta)        Summarize sequences in a FASTA file

  Flags: -b (both strands), -z (0-based indices), -m (motifs FASTA), -t (threshold)
  Type '<command> -h' for details, or 'exit' / 'q' to quit.
============================================================"""


def handle_gc(args: argparse.Namespace) -> None:
    result = calculate_gc_content(args.sequence)
    print(f"GC Content: {result:.2f}%")


def handle_transcribe(args: argparse.Namespace) -> None:
    print(transcribe_dna(args.sequence))


def handle_revcomp(args: argparse.Namespace) -> None:
    print(reverse_complement(args.sequence))


def handle_translate(args: argparse.Namespace) -> None:
    print(translate_rna(args.sequence))


def handle_motif(args: argparse.Namespace) -> None:
    one_based = not args.zero_based
    try:
        if args.both:
            hits = scan_degenerate_both_strands(args.sequence, args.motif, one_based=one_based)
            print(f"Forward (5'->3'): {hits['forward']}")
            print(f"Reverse (5'->3'): {hits['reverse']}")
        else:
            hits = find_degenerate_motifs(args.sequence, args.motif, one_based=one_based)
            print(f"Hits: {hits}")
    except ValueError as err:
        print(f"Error: {err}")


def handle_pwm(args: argparse.Namespace) -> None:
    one_based = not args.zero_based
    try:
        records = read_fasta(args.motifs_fasta)
        if not records:
            print("Motifs FASTA file is empty.")
            return
        pwm = build_pwm(list(records.values()))
        hits = scan_with_pwm(
            args.sequence, pwm, threshold=args.threshold, one_based=one_based
        )
    except (OSError, ValueError) as err:
        print(f"Error: {err}")
        return

    if not hits:
        print(f"No PWM hits found above threshold {args.threshold}.")
        return
    for pos, window, score in hits:
        print(f"Position {pos}: {window} (score: {score:.4f})")


def handle_orfs(args: argparse.Namespace) -> None:
    orfs = find_orfs(args.sequence)
    if not orfs:
        print("No complete ORFs found.")
        return
    for idx, orf in enumerate(orfs, start=1):
        print(f"ORF {idx} ({len(orf)} nt): {orf}")


def handle_fasta(args: argparse.Namespace) -> None:
    try:
        records = read_fasta(args.filepath)
    except (OSError, ValueError) as err:
        print(f"Error reading FASTA: {err}")
        return
    if not records:
        print("FASTA file is empty.")
        return
    for header, seq in records.items():
        gc = calculate_gc_content(seq)
        print(f">{header} | {len(seq)} bp | GC: {gc:.2f}%")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="locusloom",
        description="LocusLoom: Command-line bioinformatics sequence analysis toolkit.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        title="Available Commands",
        dest="command",
        metavar="<command>",
        required=True,
    )

    # 1. GC Content
    gc_p = subparsers.add_parser("gc", help="Calculate GC percentage")
    gc_p.add_argument("sequence", type=str, help="Input DNA or RNA sequence")
    gc_p.set_defaults(func=handle_gc)

    # 2. Transcribe
    tr_p = subparsers.add_parser("transcribe", aliases=["trans", "tr"], help="Transcribe DNA to mRNA")
    tr_p.add_argument("sequence", type=str, help="Input DNA sequence")
    tr_p.set_defaults(func=handle_transcribe)

    # 3. Reverse Complement
    rc_p = subparsers.add_parser("revcomp", aliases=["rc"], help="Generate reverse complement")
    rc_p.add_argument("sequence", type=str, help="Input DNA sequence")
    rc_p.set_defaults(func=handle_revcomp)

    # 4. Translate
    tl_p = subparsers.add_parser("translate", aliases=["tl"], help="Translate mRNA to protein")
    tl_p.add_argument("sequence", type=str, help="Input mRNA sequence")
    tl_p.set_defaults(func=handle_translate)

    # 5. Motif Discovery (Exact & IUPAC Degenerate)
    mt_p = subparsers.add_parser("motif", aliases=["mt", "find"], help="Scan for exact or IUPAC motif occurrences")
    mt_p.add_argument("sequence", type=str, help="Target DNA or RNA sequence")
    mt_p.add_argument("motif", type=str, help="Motif pattern (supports IUPAC codes)")
    mt_p.add_argument("-b", "--both", action="store_true", help="Scan both forward and reverse strands")
    mt_p.add_argument("-z", "--zero-based", action="store_true", help="Return 0-based Python indices")
    mt_p.set_defaults(func=handle_motif)

    # 6. Open Reading Frames
    orf_p = subparsers.add_parser("orfs", aliases=["orf"], help="Find forward-strand Open Reading Frames")
    orf_p.add_argument("sequence", type=str, help="Input DNA or RNA sequence")
    orf_p.set_defaults(func=handle_orfs)

    # 7. FASTA Summary
    fa_p = subparsers.add_parser("fasta", aliases=["fa"], help="Inspect records in a FASTA file")
    fa_p.add_argument("filepath", type=str, help="Path to a .fasta or .fa file")
    fa_p.set_defaults(func=handle_fasta)

    # 8. PWM Scanner
    pwm_p = subparsers.add_parser("pwm", help="Build a PWM from aligned FASTA motifs and scan a sequence")
    pwm_p.add_argument("sequence", type=str, help="Target DNA sequence to scan")
    pwm_p.add_argument("-m", "--motifs-fasta", required=True, type=str, help="FASTA file of aligned motif sequences")
    pwm_p.add_argument("-t", "--threshold", type=float, default=0.0, help="Minimum log-odds score threshold (default: 0.0)")
    pwm_p.add_argument("-z", "--zero-based", action="store_true", help="Return 0-based Python indices")
    pwm_p.set_defaults(func=handle_pwm)

    return parser


def main() -> None:
    parser = build_parser()

    if len(sys.argv) > 1:
        args = parser.parse_args()
        args.func(args)
        return

    print(WELCOME_BANNER)
    while True:
        try:
            raw = input("\nlocusloom> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting LocusLoom.")
            break

        if not raw:
            continue
        if raw.lower() in ("exit", "quit", "q"):
            break

        try:
            args = parser.parse_args(shlex.split(raw))
            args.func(args)
        except SystemExit:
            continue


if __name__ == "__main__":
    main()