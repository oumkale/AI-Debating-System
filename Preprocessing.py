#!/usr/bin/env python
# coding: utf-8



import nltk
import re
import pickle
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import numpy as np



def data_preprocessing(data):
    #Creating Corpus
    data = [i for i in data if type(i) is not int]
    corpus = ''.join(data)
#     for i in data:
#         if type(i) is not int:
#             corpus += i
    #Lowercasing the data
    corpus = corpus.lower()
    #Removing Numbers
    corpus = re.sub(r'\d+', '', corpus)
    #Removing Punctuations
    corpus = corpus.translate(str.maketrans("","", '!"#$%&\'()*+,-/:;<=>?@[\\]^_`{|}~'))
    #Remoivng unnecessory spaces
    corpus = corpus.strip()
    #Lemmatizing and removing stop words
    lemmatizer= WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    stop_words.add('.')
    sentence_tokens = nltk.sent_tokenize(corpus)
    #Method 1(Works better)
    word_tokens = []
    for sentence in sentence_tokens:
        sent = word_tokenize(sentence)
        if '.' in sent:
            sent.remove('.')
        word_tokens.append(sent)
#     #Method 2
#     word_tokens = []
#     for i in sentence_tokens:
#         sentence = word_tokenize(i)
#         out_sent = []
#         for word in sentence :
#             if word not in stop_words:
#                 w = lemmatizer.lemmatize(word)
#                 if w not in stop_words:
#                     out_sent.append(w)
#         word_tokens.append(out_sent)
#     end_time = time.time()
#     print("Time: {}".format(end_time-start_time))
    return corpus, sentence_tokens, word_tokens

