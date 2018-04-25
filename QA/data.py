# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:44:16 2017

@author: Vishnu
"""

from .Cleaning import clean
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import PyPDF2
from pymongo import MongoClient
import os
import glob

# os.chdir('C:/Users/hp/eclipse-workspace/QA/QA/Data')
os.chdir('/home/dev/QAbot/Data')

path = glob.glob("*.pdf")

db_client = MongoClient('52.221.4.121', 38128)

def Data(path):
    for paths in path:
        pdf = PyPDF2.PdfFileReader(open(paths, "rb"))
        file = open(paths, 'rb')
        num_of_pages = pdf.getNumPages()
        for i in range(num_of_pages):
            pages = [i]
            page_no = set(pages)
            manager = PDFResourceManager()
            io = StringIO()
            encoder = 'utf-8'
            params = LAParams()
            converter = TextConverter(manager, io, codec=encoder, 
                                      laparams=params)
            interpreter = PDFPageInterpreter(manager, converter)
            password = ""
            maxpages = 0
            caching = True
            text = ""
            for page in PDFPage.get_pages(file, page_no, maxpages=maxpages, 
                                          password=password, caching=caching, 
                                          check_extractable=True):
                interpreter.process_page(page)
                text = io.getvalue()
                text = clean(text)
                if text != '' and len(text.split()) > 10:
                    db_client.local.PDFData.insert_one({'data': text, 'keyword': paths.split('_')[0].lower()})
        
Data(path)
