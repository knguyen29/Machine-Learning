'''

Run the DecisionList_KN.py program in the command prompt as follows:
$ python DecisionList_KN.py line-train.xml line-test.xml

The script predict the meaning of the word by using  ConditionalFreqDist 
and Condition probability distribution with ELEProbDist with 10 bins.
The script then return my_untrained_answers.txt and my-trained-answers.txt as results.

'''

import re, pprint, string, nltk, os, random, logging, sys, math
from nltk.probability import ConditionalProbDist, ELEProbDist
from nltk.probability import ConditionalFreqDist
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from calculations import retrieve_idx_word, process_text, validate, log_likelihood


# Input for training data, testing data
training_data = sys.argv[1]
testing_data = sys.argv[2]


ambiguous_word = "line"

decision_list = []


# XML parsing for textual content from training data through 
with open(training_data, 'r') as data:
    soup = BeautifulSoup(data, 'html.parser')
train_data = []
for instance in soup.find_all('instance'):
    tags = dict()
    tags['id'] = instance['id']
    tags['sense'] = instance.answer['senseid']
    text = ""
    for s in instance.find_all('s'):
        text = text+ " "+ s.get_text()
    tags['text'] = process_text(text)
    train_data.append(tags)
    
    
# extracting the test data through XML parsing
with open(testing_data, 'r') as data:
    test_soup = BeautifulSoup(data, 'html.parser')

test_data = []
for instance in test_soup('instance'):
    tags = dict()
    tags['id'] = instance['id']
    text = ""
    for s in instance.find_all('s'):
        text = text+ " "+ s.get_text()
    tags['text'] = process_text(text)
    test_data.append(tags)
    
    

       
# Function to predict the sense on test data
def predict(context, majority_label):
    for rule in decision_list:
        if validate(context, rule[0]):
            if rule[1] > 0:
                return ("phone", context, rule[0])
            elif rule[1] < 0:
                return ("product", context, rule[0])
    return (majority_label, context, "default")


cfdist = ConditionalFreqDist()
# Add learned conditions from the training data to the decision list
def append_trained_rule(cfdist, data, n):
    for element in data:
        sense, context = element['sense'], element['text']
        n_word = retrieve_idx_word(n, context)
        if n_word != '':
            condition = str(n) + "_word_" + re.sub(r'\_', '', n_word)
            cfdist[condition][sense] += 1
    return cfdist


# Use conditional frequency distribution to add learned rules to the decision list

cfdist = append_trained_rule(cfdist, train_data, 1)
cfdist = append_trained_rule(cfdist, train_data, -1)
cfdist = append_trained_rule(cfdist, train_data, 2)
cfdist = append_trained_rule(cfdist, train_data, -2)
cfdist = append_trained_rule(cfdist, train_data, 3)
cfdist = append_trained_rule(cfdist, train_data, -3)
cfdist = append_trained_rule(cfdist, train_data, 4)
cfdist = append_trained_rule(cfdist, train_data, -4)
cfdist = append_trained_rule(cfdist, train_data, 5)
cfdist = append_trained_rule(cfdist, train_data, -5)
cfdist = append_trained_rule(cfdist, train_data, 6)
cfdist = append_trained_rule(cfdist, train_data, -6)
cfdist = append_trained_rule(cfdist, train_data, 7)
cfdist = append_trained_rule(cfdist, train_data, -7)
cfdist = append_trained_rule(cfdist, train_data, 8)
cfdist = append_trained_rule(cfdist, train_data, -8)


# Condition probability distribution with ELEProbDist and 10 bins 
# to calculate the probabilities of the frequencies recorded above
cpdist = ConditionalProbDist(cfdist, ELEProbDist, 10)

# Calculate the logarithm of ratio of sense probabilities
def calculate_log_likelihood(cpdist, rule):
    prob = cpdist[rule].prob("phone")
    prob_star = cpdist[rule].prob("product")
    div = prob / prob_star
    if div == 0:
        return 0
    else:
        return math.log(div, 2)
    
# from calculations import calculate_log_likelihood
# storing the learned rules into the decision list
for rule in cpdist.conditions():
    likelihood = calculate_log_likelihood(cpdist, rule)
    decision_list.append([rule, likelihood, "phone" if likelihood > 0 else "product"])
    
    decision_list.sort(key=lambda rule: math.fabs(rule[1]), reverse=True)


# Calculating the frequencies of each senses
senseA, senseB = 0.0, 0.0
for element in train_data:
    if element['sense'] == "phone":
        senseA += 1.0
    elif element['sense'] == 'product':
        senseB += 1.0
    else:
        print("warning no match")



# Calculating the predicted sense
predicted_sense = "phone" if senseA > senseB else "product"

# Performing the predictions
predictions = []
# from calculations import predict
for element in test_data:
    pred, _, r = predict(element['text'], predicted_sense)
    id1 = element['id']
    predictions.append(f'<answer instance="{id1}" senseid="{pred}"/>')


with open('my_trained_answers.txt', 'w') as f:      
    for item in predictions:
        f.write(item)
        f.write('\n')


# Create file without adding learning-rules
untrained_list = []
cfd = ConditionalFreqDist()
cpd = ConditionalProbDist(cfd, ELEProbDist, 10)
    
    
# calculate the likelihood of the untrained list
for rule in cpd.conditions():

    likelihood1 = log_likelihood(cpd, rule)
    untrained_list.append([rule, likelihood1, "phone" if likelihood1 > 0 else "product"])
    
    untrained_list.sort(key=lambda rule: math.fabs(rule[1]), reverse=True)


def predict1(context, predicted_label):
    for rule in untrained_list:
        if validate(context, rule[0]):
            if rule[1] > 0:
                return ("phone", context, rule[0])
            elif rule[1] < 0:
                return ("product", context, rule[0])
    return (predicted_label, context, "default")

predictions1 = []
# from calculations import predict
for element in test_data:
    pred1, _, r = predict1(element['text'], predicted_sense)
    id2 = element['id']
    predictions1.append(f'<answer instance="{id2}" senseid="{pred1}"/>')
    # print(f'<answer instance="{id2}" senseid="{pred1}"/>')
    
with open('my_untrained_answers.txt', 'w') as f:      
    for item in predictions1:
        f.write(item)
        f.write('\n')
