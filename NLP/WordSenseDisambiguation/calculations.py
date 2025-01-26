# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 22:16:21 2022

@author: khanh
"""
import re, pprint, string, nltk, os, random, logging, sys, math
from nltk.probability import ConditionalProbDist, ELEProbDist
from nltk.probability import ConditionalFreqDist
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import pandas as pd

# initializing the decision list to an empty list
decision_list = []

# Ambiguous word
ambiguous_word = "line"

# Use conditional frequency distribution
cfd = ConditionalFreqDist()

# Condition probability distribution with ELEProbDist and 10 bins
cpd = ConditionalProbDist(cfd, ELEProbDist, 10)

# Function to preprocess the textual content
def process_text(text):
    text = text.lower()

    # removing the standard stop word from the text
    stop_words = stopwords.words("english")
    stop_words.extend(string.punctuation)
    
    # treating "lines" and "line" as a single entity
    text = text.replace("lines", "line")
    corpus = [re.sub(r'[\.\,\?\!\'\"\-\_/]','',w) for w in text.split(" ")]
    corpus = [w for w in corpus if w not in stop_words and w != '']
    return corpus


# Calculate the logarithm of ratio of sense probabilities
def log_likelihood(cpd, rule):
    prob = cpd[rule].prob("phone")
    prob_star = cpd[rule].prob("product")
    div = prob / prob_star
    if div == 0:
        return 0
    else:
        return math.log(div, 2)
    
    
# Function to retrieve a word at a certain index
def retrieve_idx_word(n, context):
    root_index = context.index(ambiguous_word)
    n_word_index = root_index + n
    if len(context) > n_word_index and n_word_index >= 0:
        return context[n_word_index]
    else:
        return ""


# checking whether the rule is satisfied in a given context
def validate(context, rule):
    rule_scope, rule_type, rule_feature = rule.split("_")
    rule_scope = int(rule_scope)
    
    return retrieve_idx_word(rule_scope, context) == rule_feature
        
# Function to estimate the sense on test data
def estimate(context, predicted):
    for rule in decision_list:
        if validate(context, rule[0]):
            if rule[1] > 0:
                return ("phone", context, rule[0])
            elif rule[1] < 0:
                return ("product", context, rule[0])
    return (predicted, context, "default")




