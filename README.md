# Data Consultancy in Action - Group 3 project

### In collaboration with JoinSeven

Authors:
* Diana Spahieva
* Ege Özol
* Jannes Hollander
* Kyriakos Koukiadakis
* Livia Popper
* Niels Gaastra



Scripts order:

1. paragraph_splitting.py
Here, we split the content of the documents, based on their semantic meaning. In order to lemmatize the words, we used Spacy's "nl_core_news_lg" dutch, extensive ("lg", meaning large) POS tags, in order to tokenize the words for better results.

	1.1 input - "data.json"

	1.2 output - "documents_split_into_paragraphs.csv"

2. actror_mapping_to_paragraphs.py
For this module, we used the NER tags provided by Spacy's implementation by JoinSeven in order to map the actors and organizations in each paragraph. We also used the Abbreviations list provided by JoinSeven, in order to map discrete actors that had been mentioned with slightly different names.

	2.1 input:
	- "org_abbreviations.json",
	- "data.json",
	- "family_names_in_the_netherlands_with_natural_name.csv",
	- "documents_split_into_paragraphs.csv"

	2.2 output - "paragraphs_split_actors_organizations.csv"

3. preprocess_before_bert.py
In this module we combine the dates of each document and paragraph, the actors and organizations and the initial data from JoinSeven. Afterwards, we filter the paragraphs based on having at least on actor, so that the paragraphs are meaningful for our network.

	3.1 input:
	- "paragraphs_split_actors_organizations.csv"
	- "data.json"

	3.2 output - "actors_organizations_processed_data.csv"

4. Bertopic_modelling.ipynb
This is our main Topic modelling notebook. We use this to train our BERTopic models, using Spacy's "nl_core_news_lg" dutch, and extensive ("lg", meaning large) POS tags, in order to apply lemmatization in the paragraphs and tokenize the words for better results. Furthermore, for our embedding models we fine-tuned the light pre-trained sentence transformer model "all-MiniLM-L6-v2" and the 5 times bigger and best performing "all-mpnet-base-v2" model of Huggingface https://huggingface.co/sentence-transformers. There 
is also available a topic reduction algorithm, that can reduce the topics according to the likings of the user.

	4.1 input:
	- "actors_organizations_processed_data.csv"

	4.2 output:
	- bertopic model : model_nneighbors15_ncomponents5_cluster_size120_unigram
	- "newDF_nneighbors15_ncomponents5_cluster_size120_unigram.csv"

5. bipartite_data_powerbi.py
This module contains functions for preparing output data of the topic modelling notebook for our bipartite visualization in the PowerBI dashboard

	5.1 input - "newDF_nneighbors15_ncomponents5_cluster_size120_unigram.csv"

	5.2 output:
	- "bipart_actors_per_par.csv"
	- "bipart_organizations_per_par.csv"
