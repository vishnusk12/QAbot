# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:41:59 2017

@author: Vishnu
"""

import re

def clean(raw_data):
    raw_data = raw_data.replace('€', '')
    raw_data = raw_data.replace('Œ', '')
    raw_data = re.sub(r'https?:\/\/.*[\r\n]*', '', raw_data, flags=re.MULTILINE)
    raw_data = re.sub(r'\<a href', ' ', raw_data)
    raw_data = re.sub(r'&amp;', '', raw_data) 
    raw_data = re.sub(r'<br />', ' ', raw_data)
    raw_data = re.sub(r'\'', ' ', raw_data)
    raw_data = raw_data.replace("®", '')
    raw_data = re.sub(r'\bl\b', '', raw_data)
    raw_data = re.sub(r'(\n\s*)+\n+', '\n\n', raw_data)
    page_content = raw_data.replace(u"\u2122", '')
    page_content = page_content.split('References', 1)[0]
    page_content = page_content.split('Morrow', 1)[0]
    page_content = page_content.split('Wolff', 1)[0]
    page_content = page_content.split('Henry NL', 1)[0]
    page_content = page_content.split('Philadelphia', 1)[0]
    page_content = page_content.split('Ann Surg', 1)[0]
    page_content = page_content.split('Whelan T', 1)[0]
    page_content = page_content.split('receptor positive advanced breast cancer.N Engl J', 1)[0]
    page_content = page_content.split('National Comprehensive Cancer Network  NCCN .', 1)[0]
    page_content = page_content.split('DeVita VT, Lawrence TS, Rosenberg SA, eds.DeVita', 1)[0]
    page_content = page_content.split('Overmeyer B and Pierce LJ', 1)[0]
    page_content = page_content.split('10, 2017.Shannon KM and Chittenden A. Chapter 80', 1)[0]
    page_content = page_content.split('National Cancer Institute. SEER Cancer Stat Facts', 1)[0]
    page_content = page_content.split('King MC, Wieand S, Hale K, et al. Tamoxifen', 1)[0]
    page_content = page_content.split('Results from an international collaborative study.JClin Oncol.2013', 1)[0]
    return page_content
