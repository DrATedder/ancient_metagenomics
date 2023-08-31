import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import glob

def taxRank_OTU_dict(cent_out):
    tmp_dict = {}
    for line in cent_out:
        if not line.startswith("name"):
            OTU_name, taxRank = line.split("\t")[0], line.split("\t")[2]
            tmp_dict.setdefault(taxRank, []).append(OTU_name)
    return tmp_dict

def taxRank_dict_2_count(taxRank_dict):
    OTU_count_dict = {taxRank: len(OTU_names) for taxRank, OTU_names in taxRank_dict.items()}
    return OTU_count_dict

def create_pie_chart(data_dict, color_mapping, data_file):
    names = list(data_dict.keys())
    values = list(data_dict.values())
    colors = [color_mapping[name] for name in names]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(values, labels=names, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.axis('equal')
    ax.set_title('Distribution of OTUs in {0}'.format(os.path.basename(data_file).split("_")[0]))

    return fig

def main(input_folder):
    cent_outputs = os.path.join(input_folder, '*.txt')

    category_colors = {
        'superkingdom': 'blue',
        'genus': 'green',
        'species': 'red',
        'order': 'grey',
        'family': 'cyan',
        'subspecies': 'pink',
        'leaf': 'brown',
        'phylum': 'purple',
        'class': 'yellow',
        'kingdom': 'orange',
    }

    for data_file in glob.glob(cent_outputs):
        with open(data_file, "r") as d_in:
            chart = create_pie_chart(taxRank_dict_2_count(taxRank_OTU_dict(d_in)), category_colors, data_file)
            pdf_filename = "{0}_chart.pdf".format(os.path.splitext(data_file)[0])
            with PdfPages(pdf_filename) as pdf:
                pdf.savefig(chart)
                print("Saved pie chart to {0}".format(pdf_filename))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py input_folder")
        sys.exit(1)
    input_folder = sys.argv[1]
    main(input_folder)
