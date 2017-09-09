# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 11:12:22 2017

@author: pooja_oza
"""

import sys
from create_index import CreateIndex
from query_index import QueryIndex

if __name__ == '__main__':
	user_input = ' '.join(sys.argv[1:])
	print 'Given Query: %s' % user_input
	create_index_obj = CreateIndex(user_input)
	create_index_obj.create_inverted_index()
	query_index_obj = QueryIndex(user_input)
	query_index_obj.query_inverted_index()
