# ConnectomeMatch
Python implementation of preprocessing and significance testing with inexact graph matching accross a population. 

This is a Python implementation built upon the techniques used in [Osmanlıoğlu et al (2019)](https://pubmed.ncbi.nlm.nih.gov/31141738/).

It also allows for multi-threading of the more consuming proccesses (density matching and permutation testing).

# Usage
First install the package. 
```
pip install ConnectomeMatch
```
Then import 
```python
import ConnectomeMatch as cm
```
## Preprocessing
### Density Matching
Sometimes we are matching groups of graphs with different densities. For instance a sparse DTI-MRI connectome against a fully connected MEG connectome. 

Given two group of N graphs (shape=N x Node x Node), we threshold the sample matrix to match the target matrix

```python
sample_matrix = cm.match_density(sample_matrix, target_matrix, 0.2, 0.01,100)
```

## Matching

One function executes the matching on the group level. It normalises per graph pair and allows for built in multithreading. 

```python
 diagonal_matches, binary_matrices, euclidean_distances = cm.match_graphs(sample_matrix, target_matrix, njobs=4, log=True) 
```
the function returns the matches along each graphs diagonal, binary matrixes for each participant and the euclidean distance between nodes of each graph. 

## Inference

A permutation function generates a null distribution of binary matches for the sample.
This can then be compared to the average matching accuracy from binary matching matrices above
```python
import numpy as np
null = cm.generate_null_dist(sample_matrix, target_matrix,perms=100, njobs=4) # get null distribution
montecarlo_thresh = np.percentile(null, 0.95, axis=2) # get threshold values for matching matrix
significance_mask = binary_matrices.mean(axis=0) > montecarlo_thresh # mask for all significant values
```
