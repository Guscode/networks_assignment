#!/usr/bin/env python

"""
Produce network graph and metrics df from edgelist dataframe including columns 'nodeA' and 'nodeB'.
Parameters:
    path: edgelist.csv
    threshold: 500

Example:
    $ python networks.py -p edgelist.csv -t 500

Find virtual environmnet at github.com/guscode/networks_assignment
"""

# Load packages
import os

import matplotlib.pyplot as plt
import pandas as pd

import argparse
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
from collections import Counter

import networkx as nx
import scipy
import matplotlib.pyplot as plt

#Function for reading an edgelist and turning it into a weighted dataframe with a threshold
def read_edgelist(path, threshold=0):
    #reading path
    edges_df = pd.read_csv(path)
    #defining which columns are needed
    edges_df = edges_df[["nodeA", "nodeB"]]
    #converting dataframe into list of tuples
    edge_tuples = [tuple(x) for x in edges_df.values]

    #Creating empty list for edge counts
    counted_edges = []

    #looping through counted list of tuples, saving nodes and weight in counted_edges list
    for pair,weight in Counter(edge_tuples).items():
        nodeA = pair[0]
        nodeB = pair[1]
        counted_edges.append((nodeA,nodeB,weight))

    #Converting counted_edges to dataframe
    edges_df = pd.DataFrame(counted_edges, columns=["nodeA", "nodeB", "weight"])

    #Filtering weight by threshold
    filtered_df = edges_df[edges_df["weight"]>threshold]

    #returning dataframe
    return filtered_df

#Function for extracting network centrality metrics from network object
def get_metrics_df(G):
    #creating list of all metrics
    all_metrics = [nx.degree_centrality(G), nx.eigenvector_centrality(G),nx.betweenness_centrality(G)]
    #creating empty dict for saving metrics
    all_metrics_dict = {}
    #formatting metrics into tuples
    for k in nx.degree_centrality(G).keys():
        all_metrics_dict[k] = tuple(m[k] for m in all_metrics)

    #Making dataframe
    metrics_df = pd.DataFrame.from_dict(all_metrics_dict, orient="index", columns = ["degrees", "eigenvector", "betweenness"])

    #Making sure the index is numbers, and creating a column called 'node' with all the nodes.
    metrics_df["node"]=metrics_df.index
    metrics_df.index = [i for i in range(len(metrics_df))]

    #returning dataframe
    return metrics_df

def main():

    #Create ouput folder if it isn't there already
    if not os.path.exists("viz"):
        os.makedirs("viz")
        
    # Define function arguments 
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required = True, help= "Path to edgelist.csv")
    ap.add_argument("-t", "--threshold", required = True, help= "threshold for weights")
    
    args = vars(ap.parse_args())
    
    edgelist_file = args["path"] #Path to egdelist file
    threshold = int(args["threshold"])#Threshold for weights

    #Execute read function - returns dataframe with weighted edges
    edgelist_df = read_edgelist(edgelist_file) 
    
    #Creating a network with networkx and edgelist_df
    G = nx.from_pandas_edgelist(edgelist_df, "nodeA", "nodeB", ["weight"])

    #plotting network
    pos = nx.drawing.nx_pylab.draw_spring(G,node_size=5, with_labels=False)
    fig1 = plt.gcf()

    #saving network graph
    plt.savefig("viz/network.png", dpi=300, bbox_inches="tight")
    print("saved network graph at viz/network.png")

    #using the get_metrics function, returning a dataframe with centrality metrics
    metrics_df = get_metrics_df(G)

    #Saving metrics
    metrics_df.to_csv("big_metrics.csv")
    print("saved metrics in dataframe at big_metrics.csv")

    
# Define behaviour when called from command line
if __name__=="__main__":
    main()
