import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

def load_data(alpha_diversity_file, metadata_file):
    # Load alpha diversity data and metadata
    alpha_diversity_df = pd.read_csv(alpha_diversity_file)
    metadata_df = pd.read_csv(metadata_file)

    return alpha_diversity_df, metadata_df

def calculate_wilcoxon_p_values(alpha_diversity_df, metadata_df):
    # Merge alpha diversity data with metadata based on 'sample'
    merged_df = pd.merge(alpha_diversity_df, metadata_df, left_on='sample', right_on='sample_name')

    # Identify the unique groups from the metadata
    unique_groups = merged_df['grouping'].unique()

    # Create a dictionary to store p-values for group comparisons
    p_values = {}

    # Calculate the Wilcoxon test p-value for each unique group pair
    for group1 in unique_groups:
        for group2 in unique_groups:
            if group1 != group2:
                data_group1 = merged_df[merged_df['grouping'] == group1]['alpha_diversity']
                data_group2 = merged_df[merged_df['grouping'] == group2]['alpha_diversity']
                _, p_value = wilcoxon(data_group1, data_group2)
                comparison_label = f'{group1} vs. {group2}'
                p_values[comparison_label] = p_value

    return merged_df, p_values

def plot_alpha_diversity_boxplot(merged_df, p_values):
    # Create a box and whisker plot for alpha diversity grouped by 'grouping'
    plt.figure(figsize=(10, 6))
    ax = merged_df.boxplot(column='alpha_diversity', by='grouping', grid=False)
    ax.set_ylabel('Alpha Diversity')
    ax.set_xlabel('Grouping')

    # Join the p-values to the plot title, displaying each value only once
    p_value_str = ", ".join(set([f'p={value:.4f}' for value in p_values.values()]))
    plt.title(f'Alpha Diversity by Grouping\n{p_value_str}')

    # Save the plot to a file
    plt.savefig("alpha_diversity_boxplot.png")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py alpha_diversity_data.csv metadata.csv")
        sys.exit(1)

    alpha_diversity_file = sys.argv[1]
    metadata_file = sys.argv[2]

    alpha_diversity_df, metadata_df = load_data(alpha_diversity_file, metadata_file)
    merged_df, p_values = calculate_wilcoxon_p_values(alpha_diversity_df, metadata_df)
    plot_alpha_diversity_boxplot(merged_df, p_values)

