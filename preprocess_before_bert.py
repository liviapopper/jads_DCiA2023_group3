"""
This module provides functions for processing data before topic modeling and filtering.

Functions:
- add_date_of_doc:
    Get the date of each document and map it to the dataframe used for topic modeling.

- filter_min_number:
    Add a filter column to check whether we have at least one actor/organization.

- check_if_list_has_enough_nonempty_items:
    Check the length of a list and return True if it has enough non-empty items.

- filter_both:
    Add a filter column to check whether we have at least one actor and one organization.
"""

import json
import pandas as pd
import numpy as np


def add_date_of_doc(original_data, paragr_data):
    '''
    get the date of each document and map it
    to the dataframe we use for topic modelling
    '''
    with open(original_data) as function:
        data = json.load(function)
    df_orig_data = pd.DataFrame(data)
    dates_dict = dict(zip(df_orig_data.document_title, df_orig_data.published))
    # map the dict with dates per doc to the final dataframe
    paragr_data['date_published'] = paragr_data['title'].map(dates_dict)
    return paragr_data


def filter_min_number(data, orig_columns, extracted_list_ver,
					one_or_more_present, numb_unique):
    '''
    Add a filter column to chech whether we have at least 1 actor/org
    '''
    # Extract the lists of actors and organizations from string in columns
    data[extracted_list_ver] = data[orig_columns].apply(
		lambda x: x.strip('[]').replace("'", "").split(', '))
    data[one_or_more_present] = data[extracted_list_ver].apply(
		lambda x: check_if_list_has_enough_nonempty_items(x))
    data[numb_unique] = data[extracted_list_ver].apply(
		lambda x: len(set(x)))
    return data


def check_if_list_has_enough_nonempty_items(lst):
    '''
    check of list length
    '''
    if len(list(filter(None, lst))) >= 1:
        return True

def filter_both(data, both_options, organizations,actors):
    '''
    Add a filter column to chech whether we have at least 1 actor and org
    '''
    # create a list of our conditions
    conditions = [(data[organizations]==True) & (data[actors]==True)]
    values = [True]
    data[both_options] = np.select(conditions, values, False)
    return data


def process_data(actor_org_data, orig_data, final_data_name):
    '''
    main function that uses all previous ones
    '''
    # Read the initial CSV file
    df_act_org = pd.read_csv(actor_org_data)

    # Add the date of each document
    df_act_org = add_date_of_doc(orig_data, df_act_org)

    # Filter: At least 1 actor present in the paragraphs
    df_act_org = filter_min_number(df_act_org, "organizations_in_paragraph",
    "organizations_list",'one_or_more_organizations','numb_unique_organizations')

    # Filter: At least 1 organization present in the paragraphs
    df_act_org = filter_min_number(df_act_org, "actors_in_paragraph",
    "actors_list",'one_or_more_actors','numb_unique_actors')

    # Filter: Both at least 1 actor and organization present in the paragraphs
    df_act_org = filter_both(df_act_org, 'both_org_act', 'one_or_more_organizations',
    'one_or_more_actors')

    # Save the final DataFrame to a CSV file
    df_act_org.to_csv(final_data_name, index=False)

    # Return the final DataFrame
    return df_act_org


# to be put into main:
process_data('paragraphs_split_actors_organizations.csv', 'data.json',
			'actors_organizations_processed_data.csv')
