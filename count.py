from pathlib import Path
from typing import Final, Optional
import re
import json

INPUT_FILE: Final[Path] = Path("GCF.fna")
CHR_NUM_PATTERN: Final[re.Pattern] = re.compile(r"chromosome (\d+|X+|Y+)")


def add_chromosome(
    n_count: dict[str, dict[int, int]], chromosome: str, count: int
) -> dict[str, dict[int, int]]:
    if count not in n_count[chromosome]:
        n_count[chromosome][count] = 0
    n_count[chromosome][count] += 1

    return n_count


def main() -> None:
    # Form of {chromosome label : {k-N # : How many times k-N occures}}
    n_count: dict[str, dict[int, int]] = {}
    chromosome: str = ""
    temp_count: int = 0

    with INPUT_FILE.open("r") as rf:
        line: str = rf.readline()
        line_count: int = 0
        while line:
            # counld optimize here by checking for \n with an if statement
            # rather than cutting it out here
            line = line[:-1]  # remove the \n at the end of a line
            if line.startswith(">"):
                if temp_count != 0:
                    n_count = add_chromosome(n_count, chromosome, temp_count)
                    temp_count = 0

                res: Optional[re.Match] = CHR_NUM_PATTERN.findall(line)
                print(res)
                chromosome = "unplaced" if not res else res[0]
                if chromosome not in n_count:
                    n_count[chromosome] = {}  # intialize the k-n dict

            # This else block will run for a majority of the fasta file
            else:
                for char in line:
                    if char == "N":
                        temp_count += 1
                    elif temp_count != 0:
                        n_count = add_chromosome(n_count, chromosome, temp_count)
                        temp_count = 0

            line = rf.readline()
            line_count += 1

    # last addition as file could end and Ns could be lost
    if temp_count != 0:
        n_count = add_chromosome(n_count, chromosome, temp_count)

    with open("output.json", "w") as wf:
        wf.write(json.dumps(n_count))


if __name__ == "__main__":
    main()
