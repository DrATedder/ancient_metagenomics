import os
import sys
import glob
import itertools
import pandas as pd
from scipy.stats import entropy  # Import the entropy function from scipy.stats
from scipy.spatial.distance import braycurtis

def calculate_alpha_diversity(input_dir, output_file):
    # Initialize an empty list to store the results
    alpha_diversity_results = []

    # Iterate through all abundance files in the directory
    abundance_files = glob.glob(os.path.join(input_dir, "*_abundance.txt"))
    for file in abundance_files:
        # Extract the sample name from the filename
        sample_name = os.path.basename(file).split("_")[0]

        # Read the abundance file into a DataFrame (assuming no header)
        df = pd.read_csv(file, header=None, names=["species", "count", "abundance"], sep=',')

        # Calculate alpha diversity using Shannon index
        counts = df["count"]
        alpha_diversity = entropy(counts, base=2)  # Calculate Shannon index using scipy.stats.entropy

        # Append the result to the list
        alpha_diversity_results.append({"sample": sample_name, "alpha_diversity": alpha_diversity})

    # Create a DataFrame from the results list
    results_df = pd.DataFrame(alpha_diversity_results)

    # Generate a default output file name
    if not output_file:
        output_file = "alpha_diversity_results.csv"

    # Save the results to a CSV file
    results_df.to_csv(output_file, index=False)

    print("Alpha diversity calculation completed. Results saved to", output_file)

def create_count_matrix(input_dir, output_file):
    # Initialize an empty dictionary to store counts for each sample
    count_matrix = {}

    # Get a list of all species names from the input files
    species_set = set()

    # Iterate through all abundance files in the directory
    abundance_files = glob.glob(os.path.join(input_dir, "*_abundance.txt"))
    for file in abundance_files:
        # Extract the sample name from the filename
        sample_name = os.path.basename(file).split("_")[0]

        # Read the abundance file into a DataFrame (assuming CSV format)
        df = pd.read_csv(file, header=None, names=["species", "count", "abundance"], sep=',')

        # Add counts for each species to the count matrix
        for _, row in df.iterrows():
            species = row["species"]
            count = row["count"]

            # Add the species to the set of all species names
            species_set.add(species)

            # Initialize the count matrix if it's not already
            if sample_name not in count_matrix:
                count_matrix[sample_name] = {}

            # Add the count to the count matrix
            count_matrix[sample_name][species] = count

    # Create a DataFrame from the count matrix
    count_matrix_df = pd.DataFrame.from_dict(count_matrix, orient="index")

    # Fill missing values with zeros
    count_matrix_df = count_matrix_df.fillna(0)

    # Generate a default output file name
    if not output_file:
        output_file = "count_matrix.csv"

    # Save the count matrix to a CSV file
    count_matrix_df.to_csv(output_file)

    print("Count matrix created and saved to", output_file)

def calculate_beta_diversity(count_matrix_file, output_file):
    # Load the count matrix
    count_matrix_df = pd.read_csv(count_matrix_file, index_col=0)

    # Get the individual (row) names
    individuals = count_matrix_df.index

    # Initialize a DataFrame for beta diversity
    beta_diversity_df = pd.DataFrame(index=individuals, columns=individuals)

    # Calculate beta diversity (Bray-Curtis dissimilarity) for each pair of individuals
    for individual1, individual2 in itertools.combinations(individuals, 2):
        counts1 = count_matrix_df.loc[individual1]
        counts2 = count_matrix_df.loc[individual2]
        beta_value = braycurtis(counts1, counts2)
        beta_diversity_df.at[individual1, individual2] = beta_value
        beta_diversity_df.at[individual2, individual1] = beta_value

    # Generate a default output file name
    if not output_file:
        output_file = "beta_diversity_matrix.csv"

    # Save the beta diversity matrix to a CSV file
    beta_diversity_df.to_csv(output_file)

    print("Beta diversity matrix calculated and saved to", output_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_directory")
        sys.exit(1)

    input_dir = sys.argv[1]

    # Specify None as the output_file argument to trigger default file name generation
    calculate_alpha_diversity(input_dir, None)
    create_count_matrix(input_dir, None)
    calculate_beta_diversity("count_matrix.csv", None)
