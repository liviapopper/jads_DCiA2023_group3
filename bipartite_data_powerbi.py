"""
This module contains functions for preparing output data of the topic modelling
notebook for our bipartite visualization in the PowerBI dashboard.

Functions:
- modify_and_split_columns(data, orig_columns, extracted_list_ver):
	Extracts specific columns, modifies the values in those columns by removing
	square brackets and single quotes, and splits the modified string values into lists.
- explode_column(data, column_filter, column, column_list, csv_name):
	Transforms a DataFrame by exploding a specified column.
"""

import pandas as pd


def modify_and_split_columns(data, orig_columns, extracted_list_ver):
    '''
    extracts specific columns, modifies the values in those columns by removing square brackets
    and single quotes, and splits the modified string values into lists.
    '''
    data[extracted_list_ver] = data[orig_columns].apply(lambda x:
						x.strip('[]').replace("'", "").split(', '))
    return data

def explode_column(data, column_filter, column, column_list, csv_name):
    '''
    Transform DataFrame by Exploding Actors Column
    '''
    filtered_df = data.loc[data[column_filter] == True]
    title_paragr = (filtered_df[['title', 'paragraph_num']].apply(list, axis=1))
    filtered_df['title_paragr'] = title_paragr
    target = filtered_df
    target.reset_index(inplace = True, drop = True)
    target = modify_and_split_columns(target, column, column_list)
    new_df = target.explode(column_list)
    new_df.to_csv(csv_name, index=False)
    return new_df


# to be put into main:
 # load input data from Pipeline notebook:
data = pd.read_csv('newDF_nneighbors15_ncomponents5_cluster_size120_unigram.csv')
df_actors_per_par = explode_column(data, 'one_or_more_actors',
'actors_in_paragraph', 'actors_list', 'bipart_actors_per_par.csv')
df_organiz_per_par = explode_column(data, 'one_or_more_organizations',
'organizations_in_paragraph', 'organizations_list', 'bipart_organizations_per_par.csv')
