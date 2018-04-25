# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:44:51 2017

@author: Vishnu
"""
from datetime import datetime

print ('start', str(datetime.now()))

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# import spacy
from nltk.corpus import wordnet
from .Preprocess import preprocess
import random
# from pymongo import MongoClient
import collections
import aiml
import os
import glob
from .views import nlp
from .views import db_client
# from memory_profiler import profile

print ('package', str(datetime.now()))

os.chdir('/home/dev/QAbot/Data')
# os.chdir('C:/Users/hp/eclipse-workspace/QA/QA/Data')

brain_file = "/home/dev/QAbot/QA/QA.brn"
# brain_file = "C:/Users/hp/eclipse-workspace/QA/QA/QA.brn"

fallback = ['Sorry, could you say that again?', 'Sorry, can you say that again?', 
            'Can you say that again?', "Sorry, I didn't get that.", 
            'Sorry, what was that?', 'One more time?', 'What was that?', 'Say that again?',
            "I didn't get that.", "Please rephrase your question."]

# db_client = MongoClient('52.221.4.121', 38128)
 
# nlp = spacy.load('en')
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))

cat = {
    '8ef540222301fce4013f5ba643af8e260625e025': 'FDC', 
    'a2698bc710d12ad51bae1ec0a9139c1db5c9c27a': 'Cancun Resort',
    'ed78f9827c49cad7cd2f9c63a19d06ad47721a29': 'BARC'
    }

def category():
    path1 = glob.glob("*.csv")
    path2 = glob.glob("*.pdf")
    path = path1 + path2
    category = [i.split('_')[0] for i in path]
#     category = [i.split('.')[0] for i in category]
    category = list(set(category))
    category = [cat[i] for i in category]
    return category

def Data(keyword):
    PDFdata = list(db_client.local.PDFData.find({'keyword': str(keyword).lower()}))
    FAQdata = list(db_client.local.FAQ.find({'keyword': str(keyword).lower()}))
    PDFdata = [i['data'] for i in PDFdata]
    FAQdata = [i['Question'] for i in FAQdata]
    data = PDFdata + FAQdata
    return data

def index(doc):
    tfidf_matrix = tfidf_vectorizer.fit_transform(doc)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    sim = similarity[0].tolist()
    sim = sorted(((value, index) for index, value in enumerate(sim)), reverse=True)[:5]
    refined = [i[1] for i in sim if i[0] > 0.2]
    refined.remove(0)
    refined[:] = [i-1 for i in refined]
    return refined   

def searchindex(query, keyword):
    data = Data(keyword)
    cleaned_query = preprocess(query)
    cleaned_data = [''.join(preprocess(i) + i) for i in data]
    indices = [indx for indx, i in enumerate(cleaned_data) if cleaned_query in i]
    indices = indices[:5]
    return indices

def QueryProcess(query, keyword):
    print ('datastart', str(datetime.now()))
    data = Data(keyword)
    print ('dataend', str(datetime.now()))
    cleaned_query = preprocess(query)
    txtn = nlp(cleaned_query)
    txtp = nlp(query)
    np = [np.text for np in txtn.noun_chunks]
    ner = [ent.text for ent in txtp.ents]
    tokens = cleaned_query.split()
    keywords = [token.text for token in txtn if token.pos_ == 'VERB' or token.pos_ == 'ADJ']
    synonyms = list(set([l.name() for i in keywords for syn in wordnet.synsets(i) for l in syn.lemmas()]))
    synonyms = [i for i in synonyms if '_' not in i]
    if '?' in query:
        query = query
    else:
        query = query + '?'
    new_text = tokens + synonyms + np + [i.lower() for i in ner] + [query]
    final_query = ' '.join(new_text)
    cleaned_data = [''.join(preprocess(i) + i) for i in data]
    doc = [final_query] + cleaned_data
    print ('indstart', str(datetime.now()))
    indx = index(doc)
    print ('indend', str(datetime.now()))
    return final_query, indx, data

def FinalIndex(final_query, desc, query_list):
    print ('simstart', str(datetime.now()))
    desc = [preprocess(i) for i in desc if i != ''  and len(i.split()) > 5]
    list_indx = []
    for indx, i in enumerate(desc):
        dict_indx = {}
        dict_indx['index'] = indx
        for j in query_list:
            if j in i:
                dict_indx['similarity'] = nlp(final_query).similarity(nlp(i)) + 1
                list_indx.append(dict_indx)
    refined = []
    for k in list_indx:
        if k['similarity'] >= 1:
            refined.append(k['index'])
    print ('simend', str(datetime.now()))
    counter = collections.Counter(refined)
    refined = counter.most_common(10)
    refined = [l[0] for l in refined]
    return refined

def FinalAnswer(query, keyword, token):
    if token == 'CDyPJxneSxHWwCySZYruxynh5j2m6fAf':
        print ('QueryProcessstart', str(datetime.now()))
        final_query, indx, text_data = QueryProcess(query, keyword)
        print ('QueryProcessend', str(datetime.now()))
        desc_answer = [text_data[i] for i in indx]
        desc_answer = ' '.join(desc_answer)
        try:
            print ('aimlstart', str(datetime.now()))
            kern = aiml.Kernel()
            kern.bootstrap(brainFile = brain_file)
            kernel_reply = kern.respond(query)
            print ('aimlend', str(datetime.now()))
            if not "Sorry, I didn't get you.." in kernel_reply:
                return kernel_reply
            elif len(indx) == 0:
                indices = searchindex(query, keyword)
                description = [text_data[i] for i in indices]
                description_answer = ' '.join(description)
                if description_answer != '':
                    descri = re.split('[.]', description_answer)
                    descri = [i for i in descri if not ('?' in i or 'Get an overview' in i or 
                                                        'Questions to Ask' in i or 
                                                        'See' in i or 
                                                        'Learn about treatment' in i or 
                                                        'Last Medical Review' in i or 
                                                        'Last Revised' in i or 
                                                        'Chapter' in i or 
                                                        'For more information' in i or
                                                        'To learn more' in i)]
                    descri = [i for i in descri if i != '' and len(i.split()) > 5]
                    query_list = preprocess(query).split()
                    print ('final_indexstart', str(datetime.now()))
                    final_index = FinalIndex(final_query, descri, query_list)
                    print ('final_indexend', str(datetime.now()))
                    final_answer = '\n'.join(descri[i] + '.' for i in final_index)
                    if final_answer != '' or len(final_answer) > 10:
                        return final_answer
                    else:
                        return random.choice(fallback)
                else:
                    return random.choice(fallback)
            elif len(indx) > 0:
                ind = indx[0]
                question = text_data[ind]
                answer_data = list(db_client.local.FAQ.find({'Question': question}))
                if len(answer_data) > 0:
                    final_answer = answer_data[0]['Answer']
                    return final_answer
                elif desc_answer != '':
                    desc = re.split('[.]', desc_answer)
                    desc = [i for i in desc if not ('?' in i or 'Get an overview' in i or 
                                                    'Questions to Ask' in i or 
                                                    'See' in i or 
                                                    'Learn about treatment' in i or 
                                                    'Last Medical Review' in i or 
                                                    'Last Revised' in i or 
                                                    'Chapter' in i or 
                                                    'For more information' in i or
                                                    'To learn more' in i)]
                    desc = [i for i in desc if i != '' and len(i.split()) > 5]
                    query_list = preprocess(query).split()
                    print ('final_indexstart', str(datetime.now()))
                    final_index = FinalIndex(final_query, desc, query_list)
                    print ('final_indexstart', str(datetime.now()))
                    final_answer = '\n'.join(desc[i] + '.' for i in final_index)
                    if final_answer != '' or len(final_answer) > 10:
                        return final_answer
                    else:
                        return random.choice(fallback)
                else:
                    return random.choice(fallback)
        except:
            return random.choice(fallback)
    else:
        return 'Unauthorized'
