import sys
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Import the 3D plotting module
import os
import glob
import pandas as pd

def read_abundance_data(input_folder):
    abundance_data = []

    for input_file in glob.glob(os.path.join(input_folder, '*_abundance.txt')):
        with open(input_file, "r") as f_in:
            abundance_list = [float(line.strip().split(',')[2]) for line in f_in]
            abundance_data.append(abundance_list)

    max_length = max(len(abundance_list) for abundance_list in abundance_data)

    for i, abundance_list in enumerate(abundance_data):
        if len(abundance_list) < max_length:
            abundance_data[i] += [0] * (max_length - len(abundance_list))

    return np.array(abundance_data)

def plot_pca(abundance_matrix, output_folder, metadata_file=None, pca_type='3D', show_variance=False):
    if pca_type == '3D':
        pca = PCA(n_components=3)  # Use n_components=3 for 3D PCA
    elif pca_type == '2D':
        pca = PCA(n_components=2)  # Use n_components=2 for 2D PCA
    else:
        print("Invalid PCA type. Please specify '2D' or '3D'.")
        return

    principal_components = pca.fit_transform(abundance_matrix)

    if pca_type == '3D':
        pc1, pc2, pc3 = principal_components[:, 0], principal_components[:, 1], principal_components[:, 2]
    else:
        pc1, pc2 = principal_components[:, 0], principal_components[:, 1]

    explained_variance = pca.explained_variance_ratio_

    fig = plt.figure(figsize=(8, 6))
    
    if pca_type == '3D':
        ax = fig.add_subplot(111, projection='3d')  # Create a 3D axis
    else:
        ax = fig.add_subplot(111)  # Create a 2D axis

    colors = 'b'  # Default color if no metadata provided

    if metadata_file:
        try:
            metadata = pd.read_csv(metadata_file)
            sample_group_mapping = dict(zip(metadata['sample_name'], metadata['grouping']))

            # Create a color mapping based on grouping
            unique_groups = metadata['grouping'].unique()
            cmap = plt.get_cmap('tab10', len(unique_groups))

            colors = []
            for name in file_names:
                grouping = sample_group_mapping.get(name, -1)
                if grouping in unique_groups:
                    color = cmap(unique_groups.tolist().index(grouping))
                else:
                    color = 'gray'  # Default color for unknown groups
                colors.append(color)

            # Create a legend
            legend_labels = {group: color for group, color in zip(unique_groups, cmap.colors)}
            handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=group) for group, color in legend_labels.items()]
            ax.legend(handles=handles, title='Grouping')
        except Exception as e:
            print(f"Error reading metadata: {e}")

    if pca_type == '3D':
        ax.scatter(pc1, pc2, pc3, c=colors, marker='o')
        ax.set_title('3D PCA of Species Abundance Data')
        ax.set_xlabel(f'PC 1 (Explained Variance: {explained_variance[0]:.2f})')
        ax.set_ylabel(f'PC 2 (Explained Variance: {explained_variance[1]:.2f})')
        ax.set_zlabel(f'PC 3 (Explained Variance: {explained_variance[2]:.2f})')

        if file_names:
            for i, txt in enumerate(file_names):
                ax.text(pc1[i], pc2[i], pc3[i], txt)  # Add the 'txt' argument to specify the text to display
    else:
        ax.scatter(pc1, pc2, c=colors, marker='o')
        ax.set_title('2D PCA of Species Abundance Data')
        ax.set_xlabel(f'PC 1 (Explained Variance: {explained_variance[0]:.2f})')
        ax.set_ylabel(f'PC 2 (Explained Variance: {explained_variance[1]:.2f})')

        if file_names:
            for i, txt in enumerate(file_names):
                ax.text(pc1[i], pc2[i], txt)  # Add the 'txt' argument to specify the text to display

    ax.grid(True)

    # Save the plot as a PDF file
    if pca_type == '3D':
        plt.savefig(os.path.join(output_folder, 'pca_plot_3d.pdf'))
    else:
        plt.savefig(os.path.join(output_folder, 'pca_plot_2d.pdf'))

    plt.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python script.py input_folder output_folder [metadata_file] [pca_type] [show_variance]")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    metadata_file = sys.argv[3] if len(sys.argv) > 3 else None
    pca_type = sys.argv[4] if len(sys.argv) > 4 else '3D'  # Default to 3D PCA
    show_variance = sys.argv[5].lower() == 'true' if len(sys.argv) > 5 else False

    if pca_type not in ['2D', '3D']:
        print("Invalid PCA type. Please specify '2D' or '3D'.")
        sys.exit(1)

    file_names = [os.path.splitext(os.path.basename(file))[0].split("_")[0] for file in glob.glob(os.path.join(input_folder, '*_abundance.txt'))]
    abundance_matrix = read_abundance_data(input_folder)
    plot_pca(abundance_matrix, output_folder, metadata_file, pca_type, show_variance)
