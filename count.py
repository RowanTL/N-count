from pathlib import Path
from typing import Final
import re

INPUT_FILE: Final[Path] = Path("GCA.fna")
CHR_NUM_PATTERN: Final[re.Pattern] = re.compile(r"chromosome (\d+)")

def main() -> None:
    # Form of {chromosome # : {k-n # : How many times k-n occures}}
    n_count: dict[dict[int, int]] = {}
    chromosome_num: int = -1
    temp_count: int = 0

    with INPUT_FILE.open("r") as f:
        line: str = f.readline()
        while line:
            line.replace("\n", "")
            if line.startswith(">"):
                chromosome_num = int(CHR_NUM_PATTERN.findall(line)[0])
                n_count[chromosome_num] = {} # intialize the k-n dict
            else:
                # This else block will run for a majority of the fasta file
                for char in line:
                    if char == "N":
                        temp_count += 1
                    elif temp_count != 0:
                        if temp_count not in n_count[chromosome_num]:
                            n_count[chromosome_num][temp_count] = 0
                        n_count[chromosome_num][temp_count] += 1
                        temp_count = 0

            line = f.readline()            
            #print(n_count)                        
                                    
if __name__ == "__main__":
    main()
