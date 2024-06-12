import matplotlib.pyplot as plt


def count_consecutive_Ns(sequence):
    """
    Counts the consecutive 'N's in the given genome sequence.
    Args: sequence (str): The genome sequence as a string.
    Returns: dict: A dictionary with the number of consecutive 'N's as keys and 
          their frequencies as values.
    """
    counts = {}
    i = 0
    n = len(sequence)
    
    while i < n:
        if sequence[i] == 'N':
            count = 0
            while i < n and sequence[i] == 'N':
                count += 1
                i += 1
            if count in counts:
                counts[count] += 1
            else:
                counts[count] = 1
        else:
            i += 1
    
    return counts

def read_genome_sequence(file_path):
   
    with open(file_path, 'r') as file:
        genome_sequence = file.read().replace('\n', '')
    return genome_sequence

def main(file_path):

    genome_sequence = read_genome_sequence(file_path)
    counts = count_consecutive_Ns(genome_sequence)
    
    # Print
    for length, count in sorted(counts.items()):
        print(f"{length}: {count}")

    plt.hist(counts)
    plt.show() 

if __name__ == "__main__":
    file_path = 'data.txt'
    main(file_path)
