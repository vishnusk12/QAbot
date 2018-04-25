# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:48:07 2017

@author: Vishnu
"""

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemma = WordNetLemmatizer()
stopword_set = set(stopwords.words("english"))
stopword_set.update(['tell', 'define', 'explain', 'describe'])
exclude = {'?'}

def preprocess(raw_text):
    lemmatized = [lemma.lemmatize(i) for i in raw_text.split()]
    raw_text = ' '.join(lemmatized)
    raw_text = raw_text.lower()
    words = raw_text.split()
    meaningful_words = [w for w in words if w not in stopword_set]
    cleaned_word_list = " ".join(meaningful_words)
    cleaned_query = ''.join(ch for ch in cleaned_word_list if ch not in exclude)
    return cleaned_query