# -*- coding: utf-8 -*-
"""
Created on Sun Sep 03 16:36:23 2017

@author: pooja_oza
"""
import json
import math
import xml.etree.ElementTree as ET
from collections import defaultdict
from utils import get_tokens
from settings import INVERTED_INDEX_FILE, TITLE_INDEX_FILE, INPUT_FILE

class ParseWikipediaContent(object):
    """
    Parse the input wikipedia XML file. The XML file is the collection of
    the documents
    """
    def __init__(self):
        self.total_documents = 0
    
    def read_xml_files(self):
        """
        Parse the collection of documents from the input XML file
        return: document content, id, title
        """
        namespace = {'wiki_ns': 'http://www.mediawiki.org/xml/export-0.10/'}
        tree = ET.parse(INPUT_FILE)
        root = tree.getroot()
        elements = root.findall('wiki_ns:page[wiki_ns:ns="0"]', namespace)
        self.total_documents = len(elements)
        for page in elements:
            yield(page.find('wiki_ns:revision/wiki_ns:text', namespace).text,
                  page.find('wiki_ns:id', namespace).text,
                  page.find('wiki_ns:title', namespace).text)

class CreateIndex(ParseWikipediaContent):
    """
    Create the inverted index file and title index file from the 
    collection of documents
    """
    def __init__(self, query):
        super(ParseWikipediaContent, self).__init__()
        self.query = query
        self.postings = defaultdict(list)
               
    def get_postings(self, content, pageid):
        """
        tokenize the contents of the document and prepare
        the postings for each token of the document
        For e.g. - {'computer': ['docid', ['pos1', 'pos2']]}
        return: the dictionary contains the tokens and postings
        """
        tokenized_content = get_tokens(content)
        postings_dict = dict()
        for position, tokens in enumerate(tokenized_content):
            if tokens not in postings_dict:
                postings_dict[tokens] = [pageid, [str(position)]]
            else:
                postings_dict[tokens][1].append(str(position))
        return postings_dict
          
    def merge_index(self, posting):
        """
        merge the tokens and postings in a single dictionary
        """
        for key, value in posting.iteritems():
            self.postings[key].append(value)
  
    def create_tf_idf(self):
        """
        calculate the tf - idf of the tokens and the documents
        tf = 1 + log(count of term in the document)
        idf = log(total documents/ documents having term)
        append the tf, idf in the postings dictionary
        {'computer': ['docid', ['pos1', 'pos2'], 'tf', 'idf']}
        """
        for token, values in self.postings.iteritems():
            df = len(values)
            for docs in values:
                tf = 1 + math.log(len(docs[1]))
                idf = math.log(self.total_documents/df)
                docs.extend([str(tf), str(idf)])
            self.postings[token] = values
            
    def write_index_to_file(self):
        """
        write the inverted index to the file - 
        inverted_index.json
        """
        output_file = open(INVERTED_INDEX_FILE, 'w')
        json.dump(self.postings, output_file)
        output_file.close()
        del output_file

    def write_title_index_to_file(self, title_index):
        """
        write the title index to the file - 
        title_index.json
        """
        output_title_file = open(TITLE_INDEX_FILE, 'w')
        json.dump(title_index, output_title_file)
        output_title_file.close()
        del output_title_file
        
    def create_inverted_index(self):
        """
        create title index and inverted index
        title index - {'pageid' : title}
        """
        title_index = dict()
        articles = self.read_xml_files()
        for content, pageid, title in articles:
            title_index[pageid] = title
            self.merge_index(self.get_postings(content, pageid))
        self.create_tf_idf()
        self.write_index_to_file()
        self.write_title_index_to_file(title_index)
        del self.postings