# ancient_metagenomics

A set of python scripts intended to help in the analysis of ancient metagenomic data files processed through [centrifuge](https://ccb.jhu.edu/software/centrifuge/ "Link to Centrifuge homepage"). The order of use isn't fixed, and you can use many of the scripts independently. That said, it's worth reading the specific requirements for each step.

## 1. cent_out_2_pie_chart.py
Takes either a single centrifuge output file (*centrifugeReport.txt) or a directory containing centrifuge output files (txt; minimum 1) from a standard metagenomic OTU identification analysis and produces a pie chart (or charts) which shows the proportion of OTUs at each taxRank (i.e. 'kingdom', 'family', 'genera', 'species' etc...).

**Basic usage:** `python cent_out_2_pie_chart.py /path/to/directory/containing/centrifuge_output(s/) [output format]`

**Note**. Centrifuge output files should be named in the following manner:
> shortname_anything_centrifugeReport.txt

1.    shortname: used to label the pie chart
2.    anything: not used, but can be anything
3.    centrifugeReport.txt: used by the programme to identify the correct files within the given directory
4.    underscores ('_') must be used between file name elements as these are used for splitting file names

An example output can be seen below:
<img src="https://github.com/DrATedder/cent_2_pie/blob/4d1450706915204e24590eb9e8ecd979e283d664/ERR9638259_fastp_trimmed_decon_centrifugeReport_chart.png" width=80% height=80%>

A Java GUI version of this script can be found [here](https://github.com/DrATedder/cent_2_pie/tree/main "Link to cent_2_pie Java GUI").
