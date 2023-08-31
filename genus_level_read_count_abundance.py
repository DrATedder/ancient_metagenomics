import sys
import os
import glob

def cumulative_reads(cent_out):
    cumulative_genus = {}
    for line in cent_out:
        if not line.startswith("name"):
            if "species" in line or "genus" in line:
                parts = line.split("\t")
                genus, uniqR = parts[0].split()[0], parts[5]
                cumulative_genus.setdefault(genus, []).append(int(uniqR))
    return cumulative_genus

def process_file(input_file):
    with open(input_file, "r") as f_in:
        cumulative_genus = cumulative_reads(f_in)

    total = sum(sum(values) for values in cumulative_genus.values())

    # Produce a list with each genus, total unique read count, and abundance.
    abundance_list = []
    for genus, values in cumulative_genus.items():
        abundance = (sum(values) / total) * 100
        if abundance >= float(abundance_threshold):
            abundance_list.append("{0},{1},{2:.2f}".format(genus, sum(values), abundance))

    if abundance_list:
        output_file = os.path.splitext(input_file)[0] + "_abundance.txt"
        with open(output_file, "w") as f_out:
            for result in abundance_list:
                f_out.write(result + '\n')

        print("Results written to", output_file)

def main(input_dir, abundance_threshold):
    for input_file in glob.glob(os.path.join(input_dir, '*.txt')):
        process_file(input_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_directory abundance_threshold")
        sys.exit(1)
    input_dir = sys.argv[1]
    abundance_threshold = sys.argv[2]
    main(input_dir, abundance_threshold)



