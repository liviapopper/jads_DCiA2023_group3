# Data Consultancy in Action - Group 3 project

### In collaboration with JoinSeven

Authors:
- Diana Spahieva
- Ege Özol
- Jannes Hollander
- Kyriakos Koukiadakis
- Livia Popper
- Niels Gaastra

You can see our pipeline in this picture:
![Pipeline_flow](https://github.com/liviapopper/jads_DCiA2023_group3/blob/pipeline/Pipeline_flow.jpg)

### Scripts order:

1. [paragraph_splitting.py](https://github.com/liviapopper/jads_DCiA2023_group3/blob/pipeline/paragraph_splitting.py)
   - Here, we split the content of the documents, based on their semantic meaning. In order to lemmatize the words, we used Spacy's "nl_core_news_lg" Dutch, extensive ("lg", meaning large) POS tags, to tokenize the words for better results.
   - **Input**: "data.json"
   - **Output**: "documents_split_into_paragraphs.csv"

2. [actor_mapping_to_paragraphs.py](https://github.com/liviapopper/jads_DCiA2023_group3/blob/pipeline/actor_mapping_to_paragraphs.py)
   - For this module, we used the NER tags provided by Spacy's implementation by JoinSeven to map the actors and organizations in each paragraph. We also used the Abbreviations list provided by JoinSeven to map discrete actors that had been mentioned with slightly different names.
   - **Inputs**:
     - "org_abbreviations.json"
     - "data.json"
     - "family_names_in_the_netherlands_with_natural_name.csv"
     - "documents_split_into_paragraphs.csv"
   - **Output**: "paragraphs_split_actors_organizations.csv"

3. [preprocess_before_bert.py](https://github.com/liviapopper/jads_DCiA2023_group3/blob/pipeline/preprocess_before_bert.py)
   - In this module, we combine the dates of each document and paragraph, the actors and organizations, and the initial data from JoinSeven. Afterwards, we filter the paragraphs based on having at least one actor, so that the paragraphs are meaningful for our network.
   - **Inputs**:
     - "paragraphs_split_actors_organizations.csv"
     - "data.json"
   - **Output**: "actors_organizations_processed_data.csv"

4. [Bertopic_modelling.ipynb](https://github.com/liviapopper/jads_DCiA2023_group3/blob/pipeline/Bertopic_modelling.ipynb)
   - This is our main Topic modelling notebook. We use this to train our BERTopic models, using Spacy's "nl_core_news_lg" Dutch and extensive ("lg", meaning large) POS tags for lemmatization and tokenization. We also fine-tuned the light pre-trained sentence transformer model "all-MiniLM-L6-v2" and the 5 times bigger and best performing "all-mpnet-base-v2" model of Huggingface. There is also an available topic reduction algorithm that can reduce the topics according to the user's preferences.
   - **Input**: "actors_organizations_processed_data.csv"
   - **Outputs**:
     - BERTopic model: model_nneighbors15_ncomponents5_cluster_size120_unigram
     - "newDF_nneighbors15_ncomponents5_cluster_size120_unigram.csv"

5. [bipartite_data_powerbi.py](https://github.com/liviapopper/jads_DCiA2023_group3/blob/pipeline/bipartite_data_powerbi.py)
   - This module contains functions for preparing the output data of the topic modelling notebook for our bipartite visualization in the PowerBI dashboard.
   - **Input**: "newDF_nneighbors15_ncomponents5_cluster_size120_unigram.csv"
   - **Outputs**:
     - "bipart_actors_per_par.csv"
     - "bipart_organizations_per_par.csv"

Side note: The whole pipeline took us approximately six and a half hours to run on our setting, namely a laptop with a CPU i7-11800H and a GPU RTX 3050 Ti. If you want to drastically improve the running time, you might consider using a lighter version of Spacy's lemmatizer, such as "nl_core_news_sm", for both [paragraph_splitting.py](https://github.com/liviapopper/jads_DCiA2023_group3/blob/pipeline/paragraph_splitting.py), and  [Bertopic_modelling.ipynb](https://github.com/liviapopper/jads_DCiA2023_group3/blob/pipeline/Bertopic_modelling.ipynb). Furthermore, you might consider using an even lighter version of the pre-trained sentence transformer model "all-MiniLM-L6-v2" for [Bertopic_modelling.ipynb](https://github.com/liviapopper/jads_DCiA2023_group3/blob/pipeline/Bertopic_modelling.ipynb), such as "paraphrase-albert-small-v2", which are available at https://www.sbert.net/docs/pretrained_models.html?highlight=sentencetransformer%20korea. However, these tweeks, are going to change the performance of the Topic Models.
