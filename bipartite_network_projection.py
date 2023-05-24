"""
This module contains functions for building the projection of the (actor, topic) bipartite network.

Functions:
- build_bipartite_edgelist(data, data_column, keyword_column):
    Build a bipartite edgelist with format (actor_node, topic_node).

- build_projected_edgelist(data, data_column, keyword_column):
    Build a bipartite graph from bipartite edgelist and
    project it to obtain the projected network edgelist.

- calc_weight_save_df(data, column, name):
    Calculate weights of nodes, save the DataFrame to a CSV file.

"""

import pandas as pd
import networkx as nx


def build_bipartite_edgelist(data, data_column, keyword_column):
    """
    Build a bipartite edgelist with format (actor_node, topic_node).

    Args:
        data (pd.DataFrame): Input DataFrame containing actor and topic information.
        data_column (str): Name of the column in `data` representing the actor nodes.
        keyword_column (str): Name of the column in `data` representing the topic nodes.

    Returns:
        list: Bipartite edgelist in the format (actor_node, topic_node).
    """

    actor_list = list(data[data_column].unique())
    topic_list = list(data[keyword_column].unique())

    actor_topic_edge_list = list(zip(data[data_column], data[keyword_column]))

    return actor_topic_edge_list

def build_projected_edgelist(data, data_column, keyword_column):
    """
    Build a bipartite graph from bipartite edgelist and
    project it to obtain the projected network edgelist.

    Args:
        data (pd.DataFrame): Input DataFrame containing actor and topic information.
        data_column (str): Name of the column in `data` representing the actor nodes.
        keyword_column (str): Name of the column in `data` representing the topic nodes.

    Returns:
        pd.DataFrame: Projected network edgelist.
    """

    unique_actor_list = list(data[data_column].unique())
    unique_keyword_list = list(data[keyword_column].unique())

    actor_topic_edge_list = build_bipartite_edgelist(data, data_column, keyword_column)

    B = nx.Graph()
    B.add_nodes_from(unique_actor_list, bipartite=0)
    B.add_nodes_from(unique_keyword_list, bipartite=1)
    B.add_edges_from(actor_topic_edge_list)

    P = nx.projected_graph(B, unique_actor_list)

    projection_edgelist_df = nx.to_pandas_edgelist(P, nodelist=unique_actor_list)
    return projection_edgelist_df


def calc_weight_save_df (data, column, name):
    """
    Calculate weights, save the DataFrame to a CSV file.

    Args:
        data (pd.DataFrame): Input DataFrame containing actor and topic information.
        column (str): Name of the column in `data` representing the actor nodes.
        name (str): Name of the output CSV file.

    Returns:
        pd.DataFrame: DataFrame with weights.
    """

    df = build_projected_edgelist(data, column, 'keywords')
    # Calculate the node weights
    node_weights = df.groupby('source').size().reset_index(name='weight')
    # Join the weights back to original DataFrame
    df = df.merge(node_weights, on='source', how='left')
    df.to_csv(name, index=False)
    return df


# to be put into main:
 # load input data from bipartite_data_powerbi script:
per_data = pd.read_csv('bipart_actors_per_par.csv')
org_data = pd.read_csv('bipart_organizations_per_par.csv')

edgelist_org_topic_df = calc_weight_save_df(org_data, 'organizations_list',
'projection_organizations_per_par.csv')
edgelist_per_topic_df = calc_weight_save_df(per_data, 'actors_list',
'projection_actors_per_par.csv')
