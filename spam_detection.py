import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.metrics import confusion_matrix

def make_Dictionary(train_dir):
    emails = [os.path.join(train_dir,f) for f in os.listdir(train_dir)]#path of each file in training dataset is added in emails
    all_words = []#empty list
    for mail in emails:#for traversing through every file using paths mentioned in the emails 
        with open(mail) as m:#opening each file storing in m
            for i,line in enumerate(m):#traversing the file using line numbers "i" and "line" contains the whole line
                if i == 2:  #Body of email is only 3rd line of text file
                    words = line.split()#spliting the line into words taking the delimeter as space
                    all_words += words#words from each file will be added into all_words
 
    dictionary = Counter(all_words)#dictionary contains freq of each word present in all words using Counter 
    list_to_remove = dictionary.keys()#extracting the words from dictionary
    for item in list_to_remove:
      if item.isalpha() == False:#delete word from dictionary if word is not an alphabet
          del dictionary[item]
      elif len(item) == 1:#delete word from dictionary if its length is 1
          del dictionary[item]
    dictionary = dictionary.most_common(3000)#top 3000 frequency elements will be stored in dictionary
    return dictionary

# Create a dictionary of words with its frequency
train_dir = 'train-mails'
dictionary = make_Dictionary(train_dir)
 
# Prepare feature vectors per training mail and its labels
def extract_features(mail_dir):
    files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files),3000))
    docID = 0;
    for fil in files:
      with open(fil) as fi:
        for i,line in enumerate(fi):
          if i == 2:
            words = line.split()
            for word in words:
              wordID = 0
              for i,d in enumerate(dictionary):
                if d[0] == word:
                  wordID = i
                  features_matrix[docID,wordID] = words.count(word)
        docID = docID + 1
    return features_matrix

train_labels = np.zeros(702)
train_labels[351:701] = 1
train_matrix = extract_features(train_dir)

# Training SVM and Naive bayes classifier
model1 = MultinomialNB()
model2 = LinearSVC()
model1.fit(train_matrix,train_labels)
model2.fit(train_matrix,train_labels)
 
# Test the unseen mails for Spam
test_dir = 'test-mails'
test_matrix = extract_features(test_dir)
test_labels = np.zeros(260)
test_labels[130:260] = 1
result1 = model1.predict(test_matrix)
result2 = model2.predict(test_matrix)
print confusion_matrix(test_labels,result1)
print confusion_matrix(test_labels,result2)