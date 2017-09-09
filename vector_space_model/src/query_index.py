# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 11:11:53 2017

@author: pooja_oza
"""
import json
from collections import defaultdict
from utils import get_tokens, get_cosine_similarity
from settings import INVERTED_INDEX_FILE, TITLE_INDEX_FILE

class QueryIndex(object):
    """
    rank the documents of the collection using vector space model
    """
    def __init__(self, query):
        self.query = query
        self.inverted_index = dict()
        self.title_index = dict()
    
    def read_index_file(self):
        """
        read the inverted_index.json file
        inverted_index = 
        {'computer': ['docid', ['pos1', 'pos2'], 'tf', 'idf']}
        """
        read_index = open(INVERTED_INDEX_FILE, 'r')
        self.inverted_index = json.loads(read_index.read())
        read_index.close()
        del read_index

    def read_title_index_file(self):
        """
        read the title_index.json file
        title_index = {'pageid' : title}
        """
        read_title_index = open(TITLE_INDEX_FILE, 'r')
        self.title_index = json.loads(read_title_index.read())
        read_title_index.close()
        del read_title_index         
        
    def get_ranked_documents(self):
        """
        rank the documents for the given user query by calculating
        the cosine similarity between the term and the document
        """
        ranked_documents = list()
        for doc, tf_vec in self.tf_vector.iteritems():
            cos_sim = get_cosine_similarity(tf_vec, self.idf_vector)
            ranked_documents.append((doc, cos_sim))
        ranked_documents.sort(key=lambda x:x[1], reverse=True)
        if len(ranked_documents) > 0:
            print 'The top 10 ranking documents are:'
            for docs in ranked_documents[:10]:
                print self.title_index[docs[0]]
        else:
            print 'No ranking documents found for the given query'
        
    def create_tf_idf_vectors(self):
        """
        create the tf and idf vectors for the given query
        if length of user query is 3
        self.tf_vector = {'docid_1' : [tf_1, tf_2, tf_3]}
        self.idf_vector = {0: idf, 1: idf, 2: idf}
        """
        self.query = get_tokens(self.query)
        query_len = len(self.query)
        self.tf_vector = defaultdict(lambda: [0]*query_len)
        self.idf_vector = [0]*query_len
        for token_ind, token in enumerate(self.query):
            if token in self.inverted_index:
                postings = self.inverted_index[token]
                for doc_id in postings:
                    self.tf_vector[doc_id[0]][token_ind] = float(doc_id[2])
                    self.idf_vector[token_ind] = float(doc_id[3])
    
    def query_inverted_index(self):
        self.read_index_file()
        self.read_title_index_file()
        self.create_tf_idf_vectors()
        self.get_ranked_documents()
        
