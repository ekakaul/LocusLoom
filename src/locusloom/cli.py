"""Command-line interface for LocusLoom."""

import argparse
import shlex
import sys
from locusloom.seq_core import (
    calculate_gc_content,
    transcribe_dna,
    reverse_complement,
    translate_rna,
)
from locusloom.motif_finder import (
    find_motif_positions,
    scan_both_strands,
)


WELCOME_BANNER = """============================================================
  LocusLoom v0.3.0 — Bioinformatics Sequence Toolkit
============================================================
  Quick Commands (Aliases):
    gc <seq>                  Calculate GC percentage
    tr <seq>   (transcribe)   Transcribe coding DNA to mRNA
    rc <seq>   (revcomp)      Get reverse complement (5'->3')
    tl <seq>   (translate)    Translate mRNA to protein
    mt <seq> <motif> [-b] [-z] (motif) Scan for motif hits

  Flags for 'mt': -b (both strands), -z (0-based indices)
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
    if args.both:
        hits = scan_both_strands(args.sequence, args.motif, one_based=one_based)
        print(f"Forward (5'->3'): {hits['forward']}")
        print(f"Reverse (5'->3'): {hits['reverse']}")
    else:
        hits = find_motif_positions(args.sequence, args.motif, one_based=one_based)
        print(f"Positions: {hits}")


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

    # 5. Motif Discovery
    mt_p = subparsers.add_parser("motif", aliases=["mt", "find"], help="Scan for motif occurrences")
    mt_p.add_argument("sequence", type=str, help="Target DNA or RNA sequence")
    mt_p.add_argument("motif", type=str, help="Motif pattern to search for")
    mt_p.add_argument("-b", "--both", action="store_true", help="Scan both forward and reverse strands")
    mt_p.add_argument("-z", "--zero-based", action="store_true", help="Return 0-based Python indices")
    mt_p.set_defaults(func=handle_motif)

    return parser


def main() -> None:
    parser = build_parser()

    # One-shot CLI mode: e.g., `locusloom mt ATATATA ATA -b`
    if len(sys.argv) > 1:
        args = parser.parse_args()
        args.func(args)
        return

    # Interactive REPL mode when invoked with no arguments (`locusloom`)
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
            # Prevents argparse errors or `-h` from closing the interactive session
            continue


if __name__ == "__main__":
    main()