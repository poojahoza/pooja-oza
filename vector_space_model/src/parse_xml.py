# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 17:24:44 2017

@author: anaconda
"""
import xml.etree.ElementTree as ET

class ParseWikipediaContent(object):
    def __init__(self, query):
        self.query = query
        
    def read_xml_files(self):
        namespace = {'wiki_ns': 'http://www.mediawiki.org/xml/export-0.10/'}
        tree = ET.parse("Wikipedia-20170326142104.xml")
        root = tree.getroot()
        for page in root.findall('wiki_ns:page[wiki_ns:ns="0"]', namespace):
            print(page.find('wiki_ns:title', namespace).text)
            print(page.find('wiki_ns:revision/wiki_ns:text', namespace))
            
        
        
if __name__ == '__main__':
    parse_xml_obj = ParseWikipediaContent('Computer Science')
    parse_xml_obj.read_xml_files()