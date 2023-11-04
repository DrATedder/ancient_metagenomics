import glob
import os
import sys

def cent_2_dict(centrifuge_file):
    centrifuge_dict = {}
    for taxa in centrifuge_file:
        name, sep, rest_of_line = taxa.partition('\t')
        if sep:
            centrifuge_dict[name] = rest_of_line.strip()
    return centrifuge_dict

def abundance_2_cent_abundance(centrifuge_file, abundance_file):
    cent_abundance = []
    centrifuge_dict = cent_2_dict(open(centrifuge_file, "r"))
    for taxa in open(abundance_file, "r"):
        if taxa.split(",")[0] in centrifuge_dict:
            name, reads, abundance = taxa.split(",")[0], taxa.split(",")[1], taxa.split(",")[2].strip()
            taxID, taxRank, genomeSize = centrifuge_dict[name].split("\t")[0], centrifuge_dict[name].split("\t")[1], centrifuge_dict[name].split("\t")[2].strip()
            cent_abundance.append("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format(name, taxID, taxRank, genomeSize, reads, reads, abundance))
    if "name" in centrifuge_dict:
        cent_abundance.append("{0}\t{1}\n".format("name",centrifuge_dict["name"]))
    return cent_abundance

def write_output(cent_in, abundance_in):
    with open(os.path.splitext(abundance_in)[0] + "_centrifuge_format.txt", "w") as f_out:
        for items in abundance_2_cent_abundance(cent_in, abundance_in):
            if items.startswith("name"):
                f_out.write(items)
        for items in abundance_2_cent_abundance(cent_in, abundance_in):
            if not items.startswith("name"):
                f_out.write(items)
    return "Output file created"

def get_files(directory, level):
    file_dict = {}
    for file in glob.glob(directory + "/*centrifugeReport.txt"):
        cent_file = file
        abundance = os.path.splitext(file)[0] + "_{0}_abundance.txt".format(level)
        if not os.path.exists(abundance):
            print(f"abundance file '{abundance}' does not exist.")
            sys.exit(1)
        file_dict[cent_file] = abundance
    return file_dict
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python abundance_2_centrifuge.py <directory> <level>")
        sys.exit(1)
    
    directory = sys.argv[1]
    level = sys.argv[2]

    for k,v in get_files(directory, level).items():
        write_output(k,v)


