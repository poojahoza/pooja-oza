# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 12:15:13 2017

@author: pooja_oza
"""

import re
from porter_stemmer import PorterStemmer
from settings import STOP_WORDS

stemmer = PorterStemmer()

def get_tokens(content):
    content = content.lower()
    content = re.sub(r'[^a-z0-9 ]',' ',content)
    content = content.split()
    content = [stemmer.stem(token, 0, len(token)-1) for token in content if token not in STOP_WORDS]
    return content

def get_cosine_similarity(vector1, vector2):
    if len(vector1) != len(vector2):
        return 0
    return(sum([vector1[ind]*vector2[ind] for ind in range(len(vector1))]))

