'''
Created on 15-Nov-2017

@author: Vishnu
'''

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from pymongo import MongoClient
import spacy
from datetime import datetime
 
db_client = MongoClient(connect=False, port=38128)
print ('nlpstart', str(datetime.now()))
nlp = spacy.load('en')
print ('nlpend', str(datetime.now()))
from .model import FinalAnswer
from .model import category

@permission_classes((permissions.AllowAny,))
class Answer(viewsets.ViewSet):
    def create(self, request):
        question = request.data
        if question['messageSource'] == 'userInitiatedReset':
            result = {}
            result['messageSource'] = 'filter'
            result['result'] = "Hi.., I am Your Virtual Assistant..Which Company's Information you would like to gather?"
#             result['categories'] = category()
            result['success'] = True
            return Response(result)
        if question['messageSource'] == 'filter':
            result = {}
            cat = category()
            cat = [i.lower() for i in cat]
            if question['messageText'].lower() in cat:
                result['messageSource'] = 'messageFromBot'
                result['result'] = 'What would you like to know about' + ' ' + question['messageText'].upper() + '..?'
                if question['messageText'].lower() == 'fdc':
                    result['keyword'] = '8ef540222301fce4013f5ba643af8e260625e025'
                elif question['messageText'].lower() == 'cancun resort':
                    result['keyword'] = 'a2698bc710d12ad51bae1ec0a9139c1db5c9c27a'
                elif question['messageText'].lower() == 'barc':
                    result['keyword'] = 'ed78f9827c49cad7cd2f9c63a19d06ad47721a29'
                result['success'] = True
            else:
                result['messageSource'] = 'filter'
                result['result'] = "Sorry..We don't have documents related to" + ' ' + question['messageText'].upper() + '.' + 'Please select from below.'
                result['categories'] = category()
                result['success'] = True
            return Response(result)
        result = {}
        print ('Answerstart', str(datetime.now()))
        result['result'] = FinalAnswer(question['messageText'], question['keyword'], question['token'])
        print ('end', str(datetime.now()))
        result['messageSource'] = 'messageFromBot'
        if len(result['result'].split()) > 1:
            result['success'] = True
            reply = result
            return Response(reply)
        else:
            result['success'] = False
            reply = result
            return Response(reply, status=401)
