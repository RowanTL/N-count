from pathlib import Path
from typing import Final, Optional
import re
import json

INPUT_FILE: Final[Path] = Path("GCA.fna")
CHR_NUM_PATTERN: Final[re.Pattern] = re.compile(r"chromosome (\d+|X+|Y+)")

def main() -> None:
    # Form of {chromosome label : {k-N # : How many times k-N occures}}
    n_count: dict[str, dict[int, int]] = {}
    chromosome: str = ""
    temp_count: int = 0

    with INPUT_FILE.open("r") as rf:
        line: str = rf.readline()
        line_count: int = 0
        while line:
            line = line[:-1] # remove the \n at the end of a line
            if line.startswith(">"):
                res: Optional[re.Match] = CHR_NUM_PATTERN.findall(line)
                chromosome = "unplaced" if res is None else res[0]
                n_count[chromosome] = {} # intialize the k-n dict
            else:
                # This else block will run for a majority of the fasta file
                for char in line:
                    if char == "N":
                        temp_count += 1
                    elif temp_count != 0:
                        if temp_count not in n_count[chromosome]:
                            n_count[chromosome][temp_count] = 0
                        n_count[chromosome][temp_count] += 1
                        temp_count = 0

            line = rf.readline()            
            line_count += 1
            #print(n_count)                        

    with open("output.json", "w") as wf:
        wf.write(json.dumps(n_count))
                                    
if __name__ == "__main__":
    main()
