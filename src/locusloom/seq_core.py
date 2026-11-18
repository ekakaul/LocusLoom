def calculate_gc_content(sequence: str) -> float:
    seq = sequence.upper()
    if not seq:
        return 0.0

    g_count = seq.count("G")
    c_count = seq.count("C")
    total_length = len(seq)

    return ((g_count + c_count) / total_length) * 100

def transcribe_dna(sequence: str) -> str:
    return sequence.upper().replace("T", "U")

  
#Reverse complement funtion
def reverse_complement(sequence: str) -> str:
    complement_map = {"A": "T", "T": "A", "C": "G", "G": "C"}
    complement = ""

    for base in sequence.upper():
        complement = complement + complement_map[base]

    return complement[::-1]


#Dictionary
CODON_TABLE = {
    "AUG": "M", #Methionine (Start codon)
    "UUU": "F", #Phenylalanine
    "UUA": "L", #Leucine
    "GGU": "G", #Glycine 
    "GGC": "G",
    "UAA": "*", #Stop codons (UAA, UAG, UGA)
    "UAG": "*",
    "UGA": "*",
}


#Translate mRNA sequence into an amino acid string.
def translate_rna(rna_sequence: str) -> str:
    rna = rna_sequence.upper()
    protein = ""

    for i in range(0, len(rna), 3):
        codon = rna[i:i+3]
        if len(codon) < 3   :
            break
        amino_acid = CODON_TABLE.get(codon, "X")
        if amino_acid == "*":
            break
        protein = protein + amino_acid

    return protein


#Fasta Support
def read_fasta(filepath: str) -> dict[str, str]:
    """Parse a FASTA file into a dictionary mapping headers to uppercase sequences."""
    sequences: dict[str, str] = {}
    current_header: str | None = None
    chunks: list[str] = []

    with open(filepath, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_header is not None:
                    sequences[current_header] = "".join(chunks)
                current_header = line[1:].strip()
                chunks = []
            else:
                if current_header is None:
                    raise ValueError("FASTA file contains sequence data before any '>' header.")
                chunks.append(line.upper())

    if current_header is not None:
        sequences[current_header] = "".join(chunks)

    return sequences

def write_fasta(filepath: str, sequences: dict[str, str], line_width: int = 80) -> None:
    """Write a dictionary of {header: sequence} records to a FASTA file."""
    with open(filepath, "w", encoding="utf-8") as file:
        for header, seq in sequences.items():
            file.write(f">{header}\n")
            clean_seq = seq.upper().strip()
            for i in range(0, len(clean_seq), line_width):
                file.write(clean_seq[i : i + line_width] + "\n")


#Open Reading Frame (ORF) detection
STOP_CODONS = {"UAA", "UAG", "UGA"}

def find_orfs(sequence: str) -> list[str]:
    """Find all complete forward-strand Open Reading Frames (AUG to stop codon)."""
    rna = transcribe_dna(sequence)
    orfs: list[str] = []

    for frame in range(3):
        orf_start: int | None = None
        for i in range(frame, len(rna) - 2, 3):
            codon = rna[i : i + 3]
            if orf_start is None:
                if codon == "AUG":
                    orf_start = i
            elif codon in STOP_CODONS:
                orfs.append(rna[orf_start : i + 3])
                orf_start = None

    return orfs
