"""
This assumes that reformat.py has been ran on a given GCF file.    
"""

import json
import re
from typing import Final
from pathlib import Path

# FORMAT_FNA_FILE: Final[Path] = Path("temp2.txt")
FORMAT_FNA_FILE: Final[Path] = Path("fna_files/GCF_formatted.fna")
CHR_NUM_PATTERN: Final[re.Pattern] = re.compile(r"chromosome (\d+|X+|Y+)")
NUC_PATTERN: Final[re.Pattern] = re.compile(r"(R|Y|S|W|K|M|B|D|H|V|N)+", re.IGNORECASE)

def main() -> None:
    with FORMAT_FNA_FILE.open("r") as rf:
        for line in rf:
            if line.startswith(">"):
                print(line)
                res = CHR_NUM_PATTERN.findall(line)
                chromosome = "unplaced" if not res else res[0]
            else:
                for match in NUC_PATTERN.finditer(line):
                    print(match)
                    input("continue? ")
                pass
    

if __name__ == "__main__":
    main()
