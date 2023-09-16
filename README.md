# ancient_metagenomics

A set of python scripts intended to help in the analysis of ancient metagenomic data files processed through [centrifuge](https://ccb.jhu.edu/software/centrifuge/ "Link to Centrifuge homepage"). The order of use isn't fixed, and you can use many of the scripts independently. That said, it's worth reading the specific requirements for each step.

## 1. centrifuge_env_decontam.py
Decontamination of ancient DNA (aDNA) samples (or indeed, any metagenomic samples) is really important. If you have access to either a sequenced 'lab blank' and/or an environmental sample (for example a bone sample from the same burial site if you are working on ancient oral microbiomes), you will be able to taxonomically identify OTUs which may otherwise be erroneously attributed to your aDNA sample.

**Prerequisites:** All samples ('real' and 'contaminants') should have been run through centrifuge to produce 'centrifugeReport.txt' files.

**Requirements:**
1.  directory containing sample files (*centrifugeReport.txt format; see below for naming protocols)
2.  directory containing either contaminents (*centrifugeReport.txt format; can be the same folder as the samples are given in)
3.  metadata file (CSV format, see below for details)
4.  taxonomic level (either 'total', 'genus' or 'species'; see below for explanation)

**Basic usage:** `python centrifuge_env_decontam.py [sample_folder] [contaminent_folder] [metadata_file] [tax_level]`

**File naming protocol:** Centrifuge output files should be named in the following manner:
> shortname_anything_centrifugeReport.txt

1.    shortname: used to link files to the metadata
2.    anything: not used, but can be anything
3.    centrifugeReport.txt: used by the programme to identify the correct files within the given directory
4.    underscores ('_') must be used between file name elements as these are used for splitting file names

**Metadata format:** Metadata should be in two column CSV format as shown below (example can be downloaded [here](https://github.com/DrATedder/ancient_metagenomics/blob/42e6d56453cc1c63e0ee8885aeb0acfc4acc42d1/decontamination_metadata_example.csv "Decontaminant metadata example file")). The first column should contain the sequence 'shortname' for each file you want to process, and the second column should contain the sequence 'shortname' for the contaminant file. **Note.** If either file (sample or contaminent) is in the metadata but not in the directories given, they will be ignored. 

|sample|contaminent|
|---|---|
|ERR9638263|ERR9638259|
|ERR9638253|ERR9638262|
|ERR9638254|ERR9638262|
|ERR9638255|ERR9638262|
|ERR9638256|ERR9638262|

**Taxonomic level:** Taxonomic level explains what OTUs from the contaminant sample will be reomved from the 'real' sample. Brief explanations for these are given below:

*total* - This will remove **any** OTUs which overlap at any taxRank level. This is likely to be super conservative, and may only be useful in certain circumstance.

*genus* - This will remove overlapping OTUs from the genus level down (inc. 'genus', 'species', 'subspecies' & 'leaf').

*species* - This will remove overlapping OTUs from the species level down (inc. 'species', 'subspecies' & 'leaf').

**Output files:** Output file, still in 'centrifugeReport.txt' format will be output into the directory containing the samples. File names will have been appended in the following way:
> shortname_anything_<tax_level>_decontam_centrifugeReoprt.txt

A Java GUI version of this script can be found [here](https://github.com/DrATedder/centrifuge_decontamination "centrifuge_decontamination Java App").

## 2. cent_out_2_pie_chart.py
Takes either a single centrifuge output file (*centrifugeReport.txt) or a directory containing centrifuge output files (txt; minimum 1) from a standard metagenomic OTU identification analysis and produces a pie chart (or charts) which shows the proportion of OTUs at each taxRank (i.e. 'kingdom', 'family', 'genera', 'species' etc...).

**Basic usage:** `python cent_out_2_pie_chart.py /path/to/directory/containing/centrifuge_output(s/) [output format]`

**Note**. Centrifuge output files should be named in the following manner:
> shortname_anything_centrifugeReport.txt

1.    shortname: used to label the pie chart
2.    anything: not used, but can be anything
3.    centrifugeReport.txt: used by the programme to identify the correct files within the given directory
4.    underscores ('_') must be used between file name elements as these are used for splitting file names

**output format** can be either 'pdf' or 'png'.

An example output can be seen below:
<img src="https://github.com/DrATedder/cent_2_pie/blob/4d1450706915204e24590eb9e8ecd979e283d664/ERR9638259_fastp_trimmed_decon_centrifugeReport_chart.png" width=80% height=80%>

A Java GUI version of this script can be found [here](https://github.com/DrATedder/cent_2_pie/tree/main "Link to cent_2_pie Java GUI").

## 3. genus_level_read_count_abundance.py
Takes a directory containing centrifuge output files (*centrifugeReport.txt; minimum 1) from a standard metagenomic OTU identification analysis and a user defined abundance threshold and produces a comma separated txt file containing 'genera' and 'species' (combined 'species' and 'leaf' OTUs) with read count abundance greater than the threshold specified, 'number of unique reads' and 'abundance' (example output below).

### Example output file ###

|  OTU   |  UniqR   | Abundance   |
| --- | --- | --- |
|Azorhizobium caulinodans | 1725 | 0.03|
|Cellulomonas gilvus | 2019 | 0.03|
|Myxococcus xanthus | 5519 | 0.08|
|Myxococcus macrosporus | 4463 | 0.07|
|Stigmatella aurantiaca | 1622 | 0.02|
|Cystobacter fuscus | 2504 | 0.04|
|Archangium gephyra | 3011 | 0.04|
|Chondromyces crocatus | 1719 | 0.03|
|Sorangium cellulosum | 16403 | 0.24|
|Vitreoscilla filiformis | 1746 | 0.03|
|Lysobacter enzymogenes | 44962 | 0.66|
|Stella humosa | 2887 | 0.04| 

**Note**. Column headers are for illustrative purposes only. Abundance files are output without headers.

**Basic usage:** `python cent_out_2_pie_chart.py /path/to/directory/containing/centrifuge_outputs/ [threshold]`

**Threshold** can be any integer/float below 100, and output files are written into the directory containing input files. Please be aware that the threshold chosen isn't incorporated into the output file name, so you run the risk of overwriting previous abundance files if you run the script multiple times with different thresholds.

## 4. abundance_PCA_3D_variance.py

