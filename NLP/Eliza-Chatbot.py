# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 12:07:27 2022

@author: Khanh Nguyen
AIT526-Team1-Eliza chatbot
"""
import re, pprint, string, nltk, os, random, logging, sys
from nltk import word_tokenize
from nltk.tag import pos_tag
# from nltk.chunk import RegexpParser
# from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.tokenize import wordpunct_tokenize
# from nltk.tokenize import RegexpTokenizer
# from nltk.probability import FreqDist


'''
This program is called Eliza Chatbot. It is designed to simulate a real conversation between the computer with human.
It takes inputs from the users and provide answers based on a selection of answer choices. 
The first part of the algorithm used is matching strings with conditional statements such as: if, elif, else.
The second part of the algorithm is to use Python nltk package to tokenize and tag the part of speech.
If a word form match the part of speech tag, it will produce an answer accordingly.
The goal is to generate a conversation as closed to human interaction as possible.
'''
PROMPT = '[Eliza:]'
INITIAL_PROMPT = 'My name is Eliza. I am a pyschotherapist. Use PERIOD at the end of your answer for more accurate response. To end conversation, say quit. \n... To begin, tell me  your name.'

#Use nltk package to tag the part of speech on the text after being tokenized.
#The tokens then are paired with the part of speech to form a dictionary.    
def tokenize_tag(text):
    #text = text.lower()
    #text = nltk.word_tokenize(text)
    #parts = nltk.pos_tag(text)
    parts = pos_tag(word_tokenize(text))
    dic = {}
    for work, part in parts:
        if part in dic:
            dic[part].append(work)
        else:
            dic[part] = [work]
    return dic

class Responses:
    #This coding block includes a selection of questions to generate a response to the user's inputs. 
    def response_stock(parts):
        return random.choice(["How are you feeling?", "How do you feel about your job?", "What do you like to do?", "What things do you want to have?", "What is your hobby?", "How many siblings do you have?", "What sport do you like?", "What is your favorite movie?"])

    #This block takes any word that represents numeric value and return an answer including a preset choice and the same value with the input.
    def number(parts):
        if 'CD' in parts:
            number = random.choice(parts['CD'])
            day = random.choice('five six'.split())
            return "Only %s? Did you want to have %s" % (number, day)
        
    #This block takes the 'single noun' from the input and provide a response by randomly choosing between saved choices. 
    def response_single_noun(parts):
        responses = ["Why did you choose %s?", "Tell me more about %s"]
        if 'NN' in parts:
            return random.choice(responses) % random.choice(parts['NN'])
        
    #This block recognize the 'adjective' from the input and provide a response by randomly choosing between saved choices. 
    def response_adjectives(parts):
        if 'JJ' in parts:
            adjective = random.choice(parts['JJ'])
            return "%s, %s! Certainly you can think that way! Anything else?" % ( adjective.title(), adjective.upper())

    #similarly for plural-nouns
    def response_plural_nouns(parts):
        responses = ["So you have %s, not one? How many?"]
        if 'NNS' in parts:
            return random.choice(responses) % random.choice(parts['NNS'])
    
    #for responses with base verb
    def response_verb1(parts):
        if 'VB' in parts:
            verb = random.choice(parts['VB'])
            time_of_day = random.choice('Day Night'.split())
            return "Some people like to %s too, especially at %s. When do you like to %s?" % (verb, time_of_day, verb)

    #for to BE verb
    def response_verb2(parts):
        if 'BEM' in parts:
            verb = random.choice(parts['BEM'])
            time_of_day = random.choice('are have'.split())
            return "I %s too. I like it when we %s friends." % (verb, time_of_day)

    #for adverb
    def response_adverb(parts):
        if 'RB' in parts:
            adverb = random.choice(parts['RB'])
            responses = random.choice("adverb answer".split())
            return " %s is an interesting measure. Is there another %s?" % (adverb, responses)

output = INITIAL_PROMPT
while True:
    #take the input from the user to analyze and generate responses accordingly.
    user_input = input(PROMPT + output + "\n")
    # hello = input("Hi " + names+ ", let's have a conversation.")
    # user_input = input()
    if len(user_input)==0: 
        print("You need to say something for me to response.")

    elif "mother"in user_input:print(PROMPT + "Tell me more about your mother ")
    elif "father" in user_input :print(PROMPT + "Tell me more about your father?")
    elif user_input[0]=='i' and user_input[1]=='feel': print(PROMPT + "Why do you feel that way? ")
    elif user_input[-1]=='?': print(PROMPT + "What do u want to know? ")
    elif user_input[0]=='i' and user_input[1]=='think': print(PROMPT + "Do you really think so? ")
    elif "question" in user_input:print(PROMPT + "What's the question? ")
    elif "love" in user_input:print(PROMPT +"Love is Very Complicated, Agree? ")
    elif "agree" in user_input:print(PROMPT + "Ok, some people with agree with you. ")
    elif "sad" in user_input: print(PROMPT + "Hope you feel better!")
    #elif any(word in "sad depressed broke poor ugly fat" for word in user_input): print("I'm sorry you feel that way. Hopefully, you get better.")
    elif "ok" in user_input: print(PROMPT + "Ok, that's fair.")
    elif "happy" in user_input: print(PROMPT + "Being happy is the main goal in life for most people.")
    elif "fine" in user_input: print(PROMPT + "Excellent.  Anything else?.")
    elif "bore" in user_input: print(PROMPT + "Ok, we should talk about something fun.")
    elif "good" in user_input: print(PROMPT + "that's good. We should continue.")
    else: print("")
    if user_input == "quit":
        print("Thanks for talking with me. I'll see you next time.  Goodbye!")
        sys.exit(0)
        
    parts = tokenize_tag(user_input)
    funcs = [f for (n, f) in Responses.__dict__.items() if callable(f)]
    while True:
        resp = random.choice(funcs)
        funcs.remove(resp)
        output = resp(parts)
        if output:
            break



if __name__ == '__main__':
    print(tokenize_tag(sys.argv[1]))