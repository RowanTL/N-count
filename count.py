from pathlib import Path
from typing import Final, Optional
import re
import json

INPUT_FILE: Final[Path] = Path("GCF.fna")
CHR_NUM_PATTERN: Final[re.Pattern] = re.compile(r"chromosome (\d+|X+|Y+)")
AMBIGUOUS_BASES: Final[set[str]] = {
    "N",
    "R",
    "Y",
    "S",
    "W",
    "K",
    "M",
    "B",
    "D",
    "H",
    "V",
}


def add_count(
    counts: dict[str, dict[str, dict[int, int]]], chromosome: str, base: str, count: int
) -> None:
    if count not in counts[base][chromosome]:
        counts[base][chromosome][count] = 0
    counts[base][chromosome][count] += 1


def main() -> None:
    # Initialize a dictionary for each ambiguous base
    counts: dict[str, dict[str, dict[int, int]]] = {
        base: {} for base in AMBIGUOUS_BASES
    }

    with INPUT_FILE.open("r") as rf:
        chromosome: str = ""
        current_base: Optional[str] = None
        temp_count: int = 0

        line: str = rf.readline()
        while line:
            line = line[:-1]  # remove the \n at the end of a line
            if line.startswith(">"):
                # Handle leftover counts before changing chromosome
                if current_base and temp_count != 0:
                    add_count(counts, chromosome, current_base, temp_count)
                    current_base = None
                    temp_count = 0

                res: Optional[re.Match] = CHR_NUM_PATTERN.findall(line)
                chromosome = "unplaced" if not res else res[0]
                # print(f"Processing {chromosome}")
                for base in AMBIGUOUS_BASES:
                    if chromosome not in counts[base]:
                        counts[base][
                            chromosome
                        ] = {}  # initialize the k-n dict for each base
            else:
                for char in line:
                    if char in AMBIGUOUS_BASES:
                        if char == current_base:
                            temp_count += 1
                        else:
                            if current_base and temp_count != 0:
                                add_count(counts, chromosome, current_base, temp_count)
                            current_base = char
                            temp_count = 1
                    else:
                        if current_base and temp_count != 0:
                            add_count(counts, chromosome, current_base, temp_count)
                            current_base = None
                            temp_count = 0

            line = rf.readline()

        # Handle any remaining counts at the end of the file
        if current_base and temp_count != 0:
            add_count(counts, chromosome, current_base, temp_count)

    # Write each dictionary to its respective JSON file
    for base in AMBIGUOUS_BASES:
        with open(f"{base}.json", "w") as wf:
            wf.write(json.dumps(counts[base], indent=4))


if __name__ == "__main__":
    main()
