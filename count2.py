"""
This assumes that reformat.py has been ran on a given GCF file.    
"""

import json
import re
from typing import Final
from pathlib import Path
from collections import defaultdict

FORMAT_FNA_FILE: Final[Path] = Path("output.txt")
# FORMAT_FNA_FILE: Final[Path] = Path("fna_files/GCF_formatted.fna")
OUTPUT_FILE: Final[Path] = Path("output.json")
CHR_NUM_PATTERN: Final[re.Pattern] = re.compile(r"chromosome (\d+|X+|Y+)")
NUC_PATTERN: Final[re.Pattern] = re.compile(r"(R|Y|S|W|K|M|B|D|H|V|N)+", re.IGNORECASE)

def main() -> None:
    # {Chromosome #: {k-N: (# occurrences, [(starting pos, ending pos)])}}
    # The first list will only have 2 values
    # Tuples don't support item assignment :(
    count: dict[str, dict[int, list[int, list[tuple[int, int]]]]] = {}
    n_len: int = -1
    start_pos: int = -1
    end_pos: int = -1
    
    with FORMAT_FNA_FILE.open("r") as rf:
        for line in rf:
            if line.startswith(">"):
                # print(line)
                res = CHR_NUM_PATTERN.findall(line)
                chromosome = "unplaced" if not res else res[0]
                count[chromosome] = {}
            else:
                for match in NUC_PATTERN.finditer(line):
                    start_pos, end_pos = match.start(), match.end()
                    n_len = end_pos - start_pos
                    if n_len not in count[chromosome]:
                        count[chromosome][n_len] = [0, []]

                    # add to the # occurrences
                    count[chromosome][n_len][0] += 1

                    # append to start and end positions
                    count[chromosome][n_len][1].append((start_pos, end_pos))

    with OUTPUT_FILE.open("w") as wf:
        wf.write(json.dumps(count))    

    return
                    

if __name__ == "__main__":
    main()
