import sys
import os
import glob

def cumulative_taxa(cent_out, level):
    cumulative_reads = {}
    taxon_keyword = "species" if level == "species" else "genus"
    
    for line in cent_out:
        if not line.startswith("name") and taxon_keyword in line:
            parts = line.split("\t")
            if len(parts[0].split()) > 1:
                taxon_name = parts[0].split()[0] + " " + parts[0].split()[1] if level == "species" else parts[0].split()[0]
                uniq_reads = int(parts[4])
                cumulative_reads.setdefault(taxon_name, []).append(uniq_reads)
            else:
                taxon_name = parts[0].split()[0]
                uniq_reads = int(parts[4])
                cumulative_reads.setdefault(taxon_name, []).append(uniq_reads)
    
    return cumulative_reads

def process_file(input_file, abundance_threshold, level):
    with open(input_file, "r") as f_in:
        cumulative_reads = cumulative_taxa(f_in, level)

    total = sum(sum(values) for values in cumulative_reads.values())

    abundance_list = []
    for taxon, values in cumulative_reads.items():
        abundance = (sum(values) / total) * 100
        if abundance >= float(abundance_threshold):
            abundance_list.append(f"{taxon},{sum(values)},{abundance:.2f}")

    if abundance_list:
        output_file = os.path.splitext(input_file)[0] + f"_{level}_abundance.txt"
        with open(output_file, "w") as f_out:
            for result in abundance_list:
                f_out.write(result + '\n')

        print(f"Results written to {output_file}")

def main(input_dir, abundance_threshold, level):
    for input_file in glob.glob(os.path.join(input_dir, '*centrifugeReport.txt')):
        process_file(input_file, abundance_threshold, level)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python species_level_read_count_abundance.py input_directory abundance_threshold level[species or genus]")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    abundance_threshold = sys.argv[2]
    level = sys.argv[3].lower()
    main(input_dir, abundance_threshold, level)








