import json
import matplotlib.pyplot as plt
import numpy as np
from typing import Final

ARBITRARY_CUTOFF: Final[int] = 500000

def main() -> None:
    data = {}
    with open(r"json_files/GCF_prim.json", "r") as file:
        data = json.load(file)

    x_list: list[int] = []
    y_list: list[int] = []
    for chromosome, counts in data.items():
        sorted_counts = {k: v for k, v in sorted(counts.items(), key=lambda item: int(item[0]))}
        sorted_counts = {k: v for k, v in sorted_counts.items() if k != "-1"}
        #print(data[chromosome]["-1"][1])
        x_list = list(range(*data[chromosome]["-1"][1][0]))
        #print(len(x_list))
        y_list = [0 for _ in range(len(x_list))]
        for kn, info in sorted_counts.items():
            # print(f"looking at {kn} data rn")
            # kn_int: int = int(kn)
            # kn_int = kn_int if kn_int < ARBITRARY_CUTOFF else ARBITRARY_CUTOFF
            for start_pos, end_pos in info[1]:
                for num in range(start_pos, end_pos):
                    # y_list[num] = kn_int
                    y_list[num] = 1
                y_list.insert(start_pos, 0)
                x_list.insert(start_pos, start_pos)
                y_list.insert(end_pos + 2, 0)
                x_list.insert(end_pos + 1, end_pos - 1)

        x_list = np.array(x_list)
        y_list = np.array(y_list)

        plt.figure(figsize=(14, 2))
        plt.suptitle(f"Chromosome {chromosome} N Positions")
        plt.xlabel("Position")
        plt.ylabel("Is N (1 yes, 0 no)")
        plt.plot(x_list,y_list)
        # plt.show()
        print(f"attempting to save figure {chromosome}")
        plt.savefig(f"{chromosome}_position.png")

        x_list = []
        y_list = []
        

if __name__ == "__main__":
    main()
