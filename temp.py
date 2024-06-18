def main() -> None:
    line_count: int = 0
    temp_count: int = 0
    with open("GCA.fna", "r") as rf:
        line: str = rf.readline()
        while line:
            line = line[:-1]
            if line_count % 1000 == 0:
                print(line_count)
            if line_count <= 35507523 and line_count >= 35376027:
                for char in line:
                    if char == "N":
                        temp_count += 1
                    else:
                        print(f"Non N character: {line_count}")
            if line_count > 35507527:
                break
        
            line = rf.readline()
            line_count += 1

    print(temp_count)
            

if __name__ == "__main__":
    main()
