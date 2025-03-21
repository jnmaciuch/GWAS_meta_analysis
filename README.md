# Unexpected overlap: A retrospective meta-analysis of research output from Mendelian and Common Disease genomic programs
Stoeger lab rotation project (Winter 2025) by Jessica Maciuch 

## Background and significance 

Genome-wide association (GWA) studies provide the opportunity to identify alleles in the population that correlate with a given phenotype or disease. Within the past few decades, two distinct ideological “camps” have emerged in the field, each championing a distinct approach towards the application of GWA studies in disease research.  

Leveraging the benefits of GWA studies over more costly and time-consuming methods of linkage-mapping and candidate gene investigations, the “Mendelian” camp aims to characterize the genetic basis of Mendelian human disorders, seeking rare alleles with complete or very high penetrance. In contrast, the “Common Disease” camp aims to elucidate the genetic basis of complex common diseases such as hypertension and asthma, leveraging large cohorts to identify multiple risk or protective allele variants.  

However, despite the purported differential approaches to genetic disease research, there remains a possibility that the research output of these two ideological camps may contain more overlap than expected. This research project seeks to test the hypothesis that the Mendelian and Common Disease approaches did not significantly differ in terms of the specific genes and risk allele frequencies identified in published studies.  

## Methodology 

All analysis was performed using python 3.9.21. 

### Gene name comparison 

PubMed’s advanced search tool was used to pull PubMed IDs for studies associated with grant numbers awarded to either the Center for Mendelian Genomics (CMG)[1] or the Center for Common Disease Genomics (CCDG)[2] by the National Human Genome Research Institute, as listed on their respective websites. Genes listed in the title or abstract of any study published on PubMed was pulled from the AI search tool Pubtator3 [3]. If a gene was attributed to at least one publication from a given ideological camp, it was added to a list for that camp (including CMG, CCDG, or "Joint” for the n=12 joint collaboration publications between CMG and CCDG). Gene overlap was plotted using python’s UpSetPlot package (0.9.0) [4]. To determine statistical significance of the gene overlap, columns with binary values denoting whether each gene listed in the pubtator3 data set was identified in at least one CMG or CCDG-associated study were cross-tabulated. Fisher’s exact test was performed using the fisher_exact() function from scipy.stats (1.11.1) [5]. 

### Cohort size vs. risk allele frequency comparison 

GWAS metadata (“All associations v1.0.2” and “All studies v1.0.3.1”) was obtained from the NHGRI-EBI Catalog GWAS catalog [6]. Cohort size was taken from the “initial cohort size” column in the associations data. Since cohort size was reported in a string containing both numeric and character values (e.g. “10,000 cases, 20,000 controls” or “40,000 European and African ancestry participants”), cohort sizes were obtained by iteratively removing special characters (i.e. “,”), splitting string by whitespace delimiters, filtering for numeric substrings (i.e. could be converted into float data type without error), and summing float values for a total cohort size. Risk allele frequencies reported as a range (i.e. 0.1-0.2) were converted to the median value of the range, and entries that could not be converted to a float value (i.e. contained additional text information) were converted to NA values. Histograms and scatter plots were generated using the matplotlib package (3.7.2) [7]. Pearson correlation coefficients and corresponding p-values for log10 cohort size and median risk allele frequency were generated using the pearsonr() function from scipy.stats. 

## Results 

The NHGRI grants awarded to the Center for Mendelian Genomics (CMG) and the Center for Common Disease Genomics (CCDG) provide a method of identifying publications with their respective ideological camp. We obtained a list of publications associated with the grant numbers for either camp using PubMed’s advanced search tool. Gene names listed in either the title or abstract of studies on PubMed were pulled from the AI tool Pubtator3 and cross-referenced with PubMed IDs associated with either camp. Of the 496 genes pulled from titles and abstracts in publications attributed to either camp, 4 appeared in joint collaboration studies, and 3 overlapped in independent studies from the CMG and CCDG. 
![image](./Figures/title_abstract_gene_mentions_by_CMG_CCDG.png)
This overlap was statistically significant if joint collaboration studies were counted as an overlap to increase the independence assumption of the Fisher’s exact test (p = 9.45e-05), and approached but was not statistically significant if joint collaboration studies were excluded as confounders (p = 0.07).  

We next turned to curated GWAS metadata from NHGRI-EBI, which would provide information on a larger amount of GWAS publications as well as their cohort size and risk allele frequencies. Since <10 studies total in this database overlapped with the NHGRI grant numbers for CMG or CCDG, we used cohort size as a proxy measure given that the Common Disease camp references large cohort sizes in its own mission statement. As opposed to an expected bimodal distribution of cohort sizes from either Mendelian or Common Disease studies, we observed a trend towards a central cohort size in the 1000-10000 range, indicating an “ideal” cohort size for GWA studies regardless of ideological motivation. 
![image](./Figures/cohort_size_dist.png)
We also observed more unimodal distributions of median and minimum risk allele frequencies identified in studies.  
![image](./Figures/median_risk_allele_frequency_dist.png)
![image](./Figures/min_risk_allele_frequency_dist.png)
Finally, we found that there was no statistically significant correlation between total cohort size and the median risk allele frequency identified in a study (coefficient = -0.02, p = 0.20). 
![image](./Figures/median_risk_allele_frequency_cohort_size_correlation.png)
There was a weak, albeit statistically significant correlation between total cohort size and minimum risk allele frequency (coefficient = -0.03, p = 0.04).  
![image](./Figures/min_risk_allele_frequency_cohort_size_correlation.png)

## Conclusion 

Taken together, these findings provide preliminary evidence that the two distinct ideological camps of genomic research, Mendelian and Common Disease, did not end up generating two distinct programs of research output differing in cohort size and the rarity of identified risk allele frequencies. There is also evidence of greater-than-expected overlap in the genes that were emphasized from CMG and CCDG studies. 

There were several limitations of this research project. The text-scraping capabilities of pubtator3 are not completely accurate, as the program may be prone to missing gene names in the text based on text formatting, or to mistaking a word used semantically for a gene name (i.e. mistaking the word “crop” for the gene “CROP”). Due to large number of papers identified and the short time frame of this project, manual verification was not possible in all cases. 

Furthermore, the amount of studies attributed to each camp may have been vastly underestimated—particularly for the CCDG cohorts—by limiting searches to studies listing the aforementioned NHGRI grant numbers. Sequencing data from cohorts is often made available to researchers on public platforms such as dbGap, and the research output of these studies is likely not attributed to the original grant numbers. As part of this analysis, we attempted to gauge this phenomenon by tracking whether researchers who publicly requested access to CCDG data sets generated an independent publication which references the dbGap data set in the citations or text. Unfortunately, this proved impossible due to inconsistency in how the data sets were cited, which precluded the possibility of matching based on dbGap accession number. Therefore, a large percentage of relevant studies belonging to either camp may have been inadvertently excluded from this analysis. This observation may have implications for the accurate assessment of the extent to which publicly funded GWA studies are being utilized and contributing to biomedical research.  

Future studies may be able to leverage as-yet-unpublished GWAS metadata databases to provide more accurate assessments of the research output, and their potential overlap, from the Mendelian and Common Disease genomic research programs.  

## References 

1. Rutgers University. (2022, February 9). Centers for Mendelian Genomics. https://cmg.rutgers.edu/ 

2. Rutgers University. (2020, July 9). Centers for Common Disease Genomics. https://ccdg.rutgers.edu/ 

3. Wei, C.-H., Allot, A., Lai, P.-T., Leaman, R., Tian, S., Luo, L., Jin, Q., Wang, Z., Chen, Q., & Lu, Z. (2024). PubTator 3.0: An AI-powered literature resource for unlocking biomedical knowledge. Nucleic Acids Research, 52(W1). https://doi.org/10.1093/nar/gkae235 

4. Lex, A., Gehlenborg, N., Strobelt, H., Vuillemot, R., & Pfister, H. (2014). Upset: Visualization of intersecting sets. IEEE Transactions on Visualization and Computer Graphics, 20(12), 1983–1992. https://doi.org/10.1109/tvcg.2014.2346248 

5. Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., Burovski, E., Peterson, P., Weckesser, W., Bright, J., van der Walt, S. J., Brett, M., Wilson, J., Millman, K. J., Mayorov, N., Nelson, A. R., Jones, E., Kern, R., Larson, E., … Vázquez-Baeza, Y. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in python. Nature Methods, 17(3), 261–272. https://doi.org/10.1038/s41592-019-0686-2 

6. Cerezo, M., Sollis, E., Ji, Y., Lewis, E., Abid, A., Bircan, K. O., Hall, P., Hayhurst, J., John, S., Mosaku, A., Ramachandran, S., Foreman, A., Ibrahim, A., McLaughlin, J., Pendlington, Z., Stefancsik, R., Lambert, S. A., McMahon, A., Morales, J., … Harris, L. W. (2024). The nhgri-EBI GWAS catalog: Standards for reusability, sustainability and Diversity. Nucleic Acids Research, 53(D1). https://doi.org/10.1093/nar/gkae1070 

7. Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90–95. https://doi.org/10.1109/mcse.2007.55

## Setup

Change name of desired home folder in modify_home_folder.py.