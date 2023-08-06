

## Introduction 

QuickGraph library can help you get a quick overview of a social graph in an extremely convenient way. QuickGraph will show the basic information of a graph, plot the CDF of selected metrics, characterize the largest connected component (LCC).

## Overview

QuickGraph library can help you get a quick overview of a social graph in an extremely convenient way.
Show the basic information of a graph, plot the CDF of selected metrics, characterize the largest connected component (LCC), compute representative structural hole related indexes.  
Copyright (C) <2021-2026> by Qingyuan Gong, Fudan University (gongqingyuan@fudan.edu.cn)

## Before Installation

Please upgrade to Python 3.5

## System Requirements

We have tested QuickGraph on both MacOSX (version 11.5.1) and Ubuntu (Version: 20.04 LTS). This library have not been tested on other platforms.

## Usage

Please run the following commond and install the dependent libiraires:

Run 
`conda config --add channels conda-forge`

`conda update –all`
to make the libraries fit to the operation system

Run
`pip install python-igraph` 
to install the iGraph library

Run `pip install leidenalg` 
to help the modularity related analysis 

Note: Please change to `pip3 install` if you are using Apple M1 Chip

## Functions
quickgraph.info(G) returns the the basic information of a graph and plots the CDF of selected metrics. 

quickgraph.LCC_analysis(G) characterizes the largest connected component (LCC) of the input graph G on selected metrics. 

## Example
We utilize the SCHOLAT Social Network dataset as one example. 
https://www.scholat.com/research/opendata/#social_network

```python
>>> import quickgraph
>>> quickgraph.demo()
Number of Nodes: 16007, Number of Edges: 202248
Avg. degree: 25.2699, Avg. clustering coefficient: 0.5486
Modularity (Leidenalg): 0.8651, Modularity (Label_Propagation): 0.8372
Number of connected components: 5423, Number of nodes in LCC: 9583 ( 59.8676 %)
Time (G_info): 4.675
LCC: Avg. degree = 40.023, Avg. clustering coefficient = 0.625, Modularity (Leidenalg): 0.8551, Modularity (Label_Propagation): 0.8209
(rough) shortest path length = 1 : 1 ( 0.1 %), 2 : 26 ( 2.6 %), 3 : 98 ( 9.8 %), 4 : 162 ( 16.2 %), 5 : 133 ( 13.3 %), 6 : 65 ( 6.5 %), 7 : 12 ( 1.2 %), 8 : 3 ( 0.3 %), Avg. shortest path length = 4.316
Time (LCC): 1.907
```

# License

See the LICENSE file for license rights and limitations (MIT).

