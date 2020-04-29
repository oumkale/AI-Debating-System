#!/usr/bin/env python
# coding: utf-8



import nltk
import pickle
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_sentence_polarity(sentence_tokens):
    sent = SentimentIntensityAnalyzer()
    sentiment_score = []
    for sentence in sentence_tokens:
        sentiment_score.append(sent.polarity_scores(sentence))
    return sentiment_score

def find_sentences(target,inp_sentences,similar=True, top_n=10):
    sentiment_score = get_sentence_polarity(inp_sentences)
    sentiment_score = [sentence['compound'] for sentence in sentiment_score]
    if top_n > len(sentiment_score): top_n = len(sentiment_score)
    sent = SentimentIntensityAnalyzer()
    target_pol = np.array([sent.polarity_scores(target)['compound']])
    dist = abs(target_pol - np.array(sentiment_score))
    dist = np.vstack([dist,np.arange(len(inp_sentences))]).T
    dist = dist[np.argsort(dist[:,0])]
    sentences = [inp_sentences[int(i)] for i in list(dist[:,1])]
    if similar:
        return sentences[:top_n]
    else :
        sentences.reverse()
        return sentences[:top_n]





