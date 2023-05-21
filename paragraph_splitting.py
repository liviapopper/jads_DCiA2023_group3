"""
This module provides functions to load data from a JSON file,
split document content into paragraphs,
and convert documents into paragraphs.

Module functions:
- load_data(file, item, title, column):
	Loads data from a JSON file and returns a DataFrame with documents.
- split_into_paragraphs(text):
	Splits a document's content into paragraphs.
- convert_docs_to_paragraphs(data):
	Converts a DataFrame of documents into a DataFrame of paragraphs.

Example usage:
    original_data = load_data("data.json", "item", 'document_title', 'content')
    paragraphs_data = convert_docs_to_paragraphs(original_data)
"""

import warnings
import ijson
import pandas as pd
import spacy
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)


def load_data(file, item, title, column):
    '''
    input: json file with documents
    output: dataframe with documents
    '''
    documents = []
    doc_titles = []
    doc_content = []
    with open(file, "rb") as j:
        for record in ijson.items(j, item):
            documents.append(record)
    for doc in documents:
        doc_titles.append(doc[title])
    for doc in documents:
        doc_content.append(doc[column])
    data = {'title': doc_titles, 'content': doc_content}
    return pd.DataFrame(data)

def split_into_paragraphs(text):
    '''
    input: document content
    output: document split into paragraphs
    '''
    nlp = spacy.load('nl_core_news_lg')
    doc = nlp(text)
    paragraphs = []
    current_paragraph = ''

    for sentence in doc.sents:
        if len(current_paragraph) == 0:
            current_paragraph = str(sentence)
        else:
            similarity = sentence.similarity(nlp(current_paragraph))
            if similarity < 0.6:  # threshold for new paragraph
                paragraphs.append(current_paragraph)
                current_paragraph = str(sentence)
            else:
                current_paragraph += '\n' + str(sentence)

    paragraphs.append(current_paragraph)  # add last paragraph
    return paragraphs

def convert_docs_to_paragraphs(data):
    '''
    input: dataframe of documents
    output: dataframe of document split into paragraphs
    '''
    paragraphs_data = pd.DataFrame(columns=['title', 'paragraph_num', 'paragraph_text'])

    for i, row in data.iterrows():
        title = row['title']
        content = row['content']
        paragraphs = split_into_paragraphs(content)

        for j, paragraph in enumerate(paragraphs):
            paragraphs_data = paragraphs_data.append({
		'title': title,
		'paragraph_num': j+1,
		'paragraph_text': paragraph
		},ignore_index=True)
    paragraphs_data.to_csv('documents_split_into_paragraphs.csv', index=False)
    return paragraphs_data


# to be put into main:
original_data = load_data("data.json", "item", 'document_title', 'content')
paragraphs_data = convert_docs_to_paragraphs(original_data)
