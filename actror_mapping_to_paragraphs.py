"""
This module processes abbreviations, documents,
and paragraphs to extract actors and organizations.

Functions:
- get_name_by_abbreviation: Function to link names to abbreviations.
- process_abbreviations: Function to load and process abbreviations.
- load_documents: Function to load the documents.
- process_documents: Function to process the documents and extract actors and organizations.
- process_paragraphs: Function to process the paragraphs and find actors and organizations.
- main_process: Main function that orchestrates the entire process.

Usage:
- Call the main_process function with the appropriate arguments.
"""

import warnings
import ijson
import difflib
import re
import pandas as pd
#warnings.filterwarnings('ignore', category=FutureWarning)
#warnings.filterwarnings('ignore', category=UserWarning)


def get_name_by_abbreviation(org_abbreviation_dict, abbreviation):
    """
    Define functions for linking names to abbreviations, vice versa
    """
    for org_name, org_info in org_abbreviation_dict.items():
        if 'abbreviation' in org_info.keys():
            if org_info['abbreviation'] == abbreviation:
                return org_name
    return None


def process_abbreviations(filename):
    """
    Load abreviations from a json file and return the
    org_name_list, org_abbrev_list, org_cleaning_list
    """
    org_abbreviations_raw = []

    with open(filename, "rb") as j:
        for record in ijson.items(j, "item"):
            org_abbreviations_raw.append(record)

    org_abbreviation = {}
    for entity in org_abbreviations_raw:
        org_name = entity['attributes']['general']['name']
        org_info = entity['attributes']['general']
        org_abbreviation[org_name] = org_info

    org_name_list = [info['name'] for info in org_abbreviation.values() if 'name' in info.keys()]
    org_abbrev_list = [info['abbreviation'] for info in org_abbreviation.values()if 'abbreviation' in info.keys()]
    org_cleaning_list = org_name_list + org_abbrev_list

    return org_name_list, org_abbrev_list, org_cleaning_list, org_abbreviation


def load_documents(filename):
    """
    Load the documents and return a list with them
    """
    documents = [] 
    with open(filename, "rb") as j:
        for record in ijson.items(j, "item"):
            documents.append(record)   
    return documents


def process_documents(documents, org_name_list, org_abbrev_list, org_abbreviation, family_names):
    surnames = pd.read_csv(family_names)
    surname_list = list(surnames['natural name'])

    def extract_surname(name):
        split = name.split()
        if len(split) > 1:
            return ' '.join(split[1:])
        return name

    # Filter some erroneous values from the surnames dataset (optional)
    surname_filter_list = ['I', 'Minister', 'O', 'Ve', 'An', 'Commissaris']

    org_filter_list = []
    doc_org = {}
    doc_per = {}
    name_regex_query = '|'.join(org_name_list)
    abbrev_regex_query = '|'.join(org_abbrev_list)

    for doc in documents:
        per_list = []
        org_list = []
        sentences = doc['sentences']
        for sent in sentences:
            sentence_entries = sent['ner_tags']['flair/ner-dutch-large']
            for entry in sentence_entries:
                if entry['ner_label'] == 'PER':
                    surname = extract_surname(entry['text'])
                    if surname in surname_list and surname not in surname_filter_list:
                        per_list.append(surname)
                elif entry['ner_label'] == 'ORG':
                    raw_organization = entry['text']
                    if raw_organization not in org_filter_list:
                        name_match = re.search(raw_organization, name_regex_query)
                        if name_match:
                            name_match_string = name_match.group()
                            if name_match_string in org_name_list:
                                organization = name_match_string
                                org_list.append(organization)
                        else:
                            abbrev_match = re.search(raw_organization, abbrev_regex_query)
                            if abbrev_match:
                                abbrev_match_string = abbrev_match.group()
                                if abbrev_match_string in org_abbrev_list:
                                    organization = get_name_by_abbreviation(org_abbreviation, abbrev_match_string)
                                    org_list.append(organization)
        doc_per[doc['document_title']] = list(set(per_list))
        doc_org[doc['document_title']] = list(set(org_list))
    return doc_per, doc_org


def process_paragraphs(split_paragr, doc_per, doc_org):
    """
    Paragraph level extraction
    """
    paragraphsDF = pd.read_csv(split_paragr)
    # Find actors in paragraph based on all Actors present in document
    def find_actors_in_paragraph(doc_per, document_title, paragraph_text):
        document_actor_list = doc_per[document_title]
        regex = '|'.join(document_actor_list)
        actors_in_paragraph = re.findall(regex, paragraph_text)
        return actors_in_paragraph

    def find_organizations_in_paragraph(doc_org, document_title, paragraph_text):
        document_organization_list = doc_org[document_title]
        if len(document_organization_list) > 0:
            regex = '|'.join(document_organization_list)
            organizations_in_paragraph = re.findall(regex, paragraph_text)
            return organizations_in_paragraph
        return []
    
    # Apply find organizations in paragraph function to all paragraphs
    paragraphsDF['organizations_in_paragraph'] = paragraphsDF.apply(
        lambda row: find_organizations_in_paragraph(doc_org, row['title'], row['paragraph_text']), axis=1)
    # Apply find actors in paragraph function to all paragraphs
    paragraphsDF['actors_in_paragraph'] = paragraphsDF.apply(
        lambda row: find_actors_in_paragraph(doc_per, row['title'], row['paragraph_text']), axis=1)

    return paragraphsDF


def main_process(abbreviations_filename, documents_filename, surnames_filename, split_paragr, csv_name):
    # Load and process abbreviations
    org_name_list, org_abbrev_list, org_cleaning_list, org_abbreviation = process_abbreviations(abbreviations_filename)
    # Load documents
    documents = load_documents(documents_filename)
    # Process documents
    doc_per, doc_org = process_documents(documents, org_name_list, org_abbrev_list, org_abbreviation, surnames_filename)
    # Process paragraphs
    processed_paragraphsDF = process_paragraphs(split_paragr, doc_per, doc_org)
    processed_paragraphsDF.to_csv(csv_name, index=False)
    return processed_paragraphsDF


# to be put into main:
final_df = main_process("org_abbreviations.json",
					"data.json",
					"family_names_in_the_netherlands_with_natural_name.csv",
					'documents_split_into_paragraphs.csv',
					'paragraphs_split_actors_organizations.csv')
