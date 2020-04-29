#!/usr/bin/env python
# coding: utf-8

# # Dependencies

import numpy as np
import pickle
import re
import nltk
import string
import time
import gensim
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize



import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



setting = {
            'embedding_size' : 100,
            'min_count' : 2,
            'epochs' : 100
        }



# data = load_data('Datasets/Articles/AI.p')




def data_preprocessing(data):
    #Creating Corpus
    corpus = ''.join(data)
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

# corpus, sentence_tokens, word_tokens = data_preprocessing(data)

# save_data('AI Sentence Tokens',sentence_tokens)


# # Model


def tag_documents(word_tokens,label=True):
    tagged_sentences = []
    for i in range(len(word_tokens)):
        tagged_sentences.append(gensim.models.doc2vec.TaggedDocument(word_tokens[i], [i]))
    return tagged_sentences
    


def get_ranks(tagged_sentences,model):
    ranks = []
    for doc_id in range(len(tagged_sentences)):
        print(doc_id)
        inferred_vector = model.infer_vector(tagged_sentences[doc_id].words)
        sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
        rank = [docid for docid, sim in sims].index(doc_id)
        ranks.append(rank)
    return ranks



def create_model(setting):
    return gensim.models.doc2vec.Doc2Vec(vector_size=setting['embedding_size'], min_count=setting['min_count'], epochs=setting['epochs'])


def get_dict(model, tagged_sentences):
    return model.build_vocab(tagged_sentences,progress_per=50000)



def train_model(model,tagged_sentences):
    return model.train(tagged_sentences, total_examples=model.corpus_count, epochs=model.epochs)



def get_similar_sentences(query,model,tagged_sentences,top_n=10):
    inferred_vector = model.infer_vector(word_tokenize(query))
    sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
    similar_docs=[]
    for index in range(len(sims)):
        similar_docs.append(' '.join(tagged_sentences[sims[index][0]].words))
    return similar_docs

