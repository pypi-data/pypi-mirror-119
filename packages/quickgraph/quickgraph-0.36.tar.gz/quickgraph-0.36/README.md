

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
```python
>>> import quickgraph as qg
>>> from igraph import *
>>> G = Graph.Barabasi(1024)
>>> qg.info(G)
Number of Nodes: 1024, Number of Edges: 1023
Avg. degree: 1.998, Avg. clustering coefficient: 0.0
Modularity (Leidenalg): 0.9347, Modularity (Label_Propagation): 0.8443
Number of connected components: 1, Number of nodes in LCC: 1024 ( 100.0 %)
Time (G_info): 0.946691689000005
>>> qg.LCC_analysis(G)
LCC: Avg. degree = 1.998, Avg. clustering coefficient = 0.0, Modularity (Leidenalg): 0.9345, Modularity (Label_Propagation): 0.8402
(rough) shortest path length = 1 : 1 ( 0.1 %), 2 : 1 ( 0.1 %), 3 : 13 ( 1.3 %), 4 : 23 ( 2.3 %), 5 : 34 ( 3.4 %), 6 : 44 ( 4.4 %), 7 : 66 ( 6.6 %), 8 : 68 ( 6.8 %), 9 : 73 ( 7.3 %), 10 : 70 ( 7.0 %), 11 : 32 ( 3.2 %), 12 : 33 ( 3.3 %), 13 : 24 ( 2.4 %), 14 : 8 ( 0.8 %), 15 : 8 ( 0.8 %), 16 : 2 ( 0.2 %), Avg. shortest path length = 8.51
Time (LCC): 0.13979007699999357
```

# License

See the LICENSE file for license rights and limitations (MIT).

