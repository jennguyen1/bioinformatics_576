# Bioinformatics Projects

* **gene_assembly**: A gene assembly program using a greedy fragment assembly algorithm. Assembles genome reads with overlapping regions into a single superstring. Test cases include a gene assembly problem for the ebola virus genome, which can be confirmed via BLAST.
* **gene_alignment**: A gene alignment program using an affine gap penalty. Aligns two sequences to the best alignment considering gaps. Takes additional arguments regarding the match/mismatch score, space/gap penalty. 
* **gene_annotation**: A hidden markov algorithm to identify exon and intron regions in the genome. Model are trained using a training sequence data and standard maximum likelihood estiamtes with Laplace smoothing. Algorithm is used to predict exon/intron regions on testing data. Also includes a program to output accuracy, recall and precision of exon predictions.
* **gene_clustering**: A hierarchical clustering algorithm for clustering genes basedon expression values under various conditions. Options for selecting linkage type ('C' for complete, 'S' for single, 'A' for average) and number of clusters to return.
