'''

Instructions to Run the scorer.py program in the command prompt as follows:
$ python scoreKN.py my_untrained_answers.txt my_trained_answers.txt line-answers.txt

'''


import pandas as pd
import re
import sys
import numpy as np

# command line arguments for the file sources of results obtained from decision-list and available gold standard
untrained_key = sys.argv[1]
trained_key = sys.argv[2]
line_answers = sys.argv[3]


#function to search the strings and get keys, sense
def get_senses(mylist):
    sense = {}
    keys = []
    for string in mylist:
        search = re.search('<answer instance="(.*)" senseid="(.*)"/>', string, re.IGNORECASE)
        key = search.group(1)
        keys.append(key)
        value = search.group(2)
        sense[key] = value
    return sense, keys



#open the two files taken as input from command line and strip out '\n'
with open(line_answers, 'r') as data:
    mylist1 = [line.rstrip('\n') for line in data]
answers, keys = get_senses(mylist1)

with open(trained_key, 'r') as data:
    mylist2 = [line.rstrip('\n') for line in data]
trained, keys = get_senses(mylist2)

with open(untrained_key, 'r') as data:
    mylist3 = [line.rstrip('\n') for line in data]
untrained, keys = get_senses(mylist3)

scores = 0
total = len(keys)
for key in keys:
    if(answers[key] == untrained[key]):
        scores += 1
scores

print('\nWe compare the Accuracy score for each untrained and trained model')

# calucalate the accuracy before learning features
untrained_accuracy = (float(scores)/float(total))*100
print("\n   my_untrained_answers Accuracy score: "+str(untrained_accuracy)+"%")


# Check if the values matches
correct = 0
total = len(keys)
for key in keys:
    if(answers[key] == trained[key]):
        correct += 1
correct

# #calculated the most frequent sense baseline
# baseline_count = 0
# for key in keys:
#     if(answers[key] == 'phone'):
#         baseline_count += 1
# baseline_acc = (float(baseline_count)/float(total))*100
# print("\nBaseline accuracy is "+str(baseline_acc)+"%")


# calucalate the accuracy after learning features
accuracy = (float(correct)/float(total))*100
print("\n   my_trained_answers Accuracy score: "+str(accuracy)+"%")

#creating array and append the values to the answers list
answers_list = []
for v in answers:
    answers_list.append(answers[v])
    
#creating array for our output and append the values to list
trained_list = []
for v in trained:
    trained_list.append(trained[v])
    

# creating dataframes for both the files
df1 = pd.Series( (v for v in trained_list) )
df2 = pd.Series( (v for v in answers_list) )

#generating confusion matrix
conf_matr = pd.crosstab(df1, df2)
print('\nThen we inspect further the trained mode to retrieve some metrics')
print("    Confusion matrix for my_trained_answers is\n"  +str(conf_matr))

cm = pd.DataFrame(conf_matr)


cm1 = pd.DataFrame()
cm['Phone'] = cm['phone'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
cm['Product'] = cm['product'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
cm1 = cm[['Phone', 'Product']].copy()


TP = np.diag(cm1)
FP = np.sum(cm1, axis=0) - TP
FN = np.sum(cm1, axis=1) - TP
precision = TP/(TP+FP)
recall = TP/(TP+FN)


print("\n    Precision score for each entity in the trained answers: " , precision, "\n\n    Recall score for each entity in the trained answers: ", recall)