from nltk.sentiment.vader import SentimentIntensityAnalyzer

from nltk.sentiment.util import *
#
import pandas as pd
import os
from nltk.corpus import stopwords
import nltk.data
import logging
import numpy as np  # Make sure that numpy is imported
from gensim.models import Word2Vec
from sklearn.ensemble import RandomForestClassifier
from nltk import tokenize

from KaggleWord2VecUtility import KaggleWord2VecUtility
'''
VADER produces four sentiment metrics from these word ratings, which you can see below. 
The first three, positive, neutral and negative, represent the proportion of the text 
that falls into those categories.  
The final metric, the compound score, is the sum of all of the lexicon 
ratings  which have been standardised to range between -1 and 1. 
'''
def review_to_sentences( review, tokenizer, remove_stopwords=False ):
        # Function to split a review into parsed sentences. Returns a
        # list of sentences, where each sentence is a list of words
        #
        # 1. Use the NLTK tokenizer to split the paragraph into sentences
        raw_sentences = tokenizer.tokenize(review.decode('utf8').strip())
        #
        # 2. Loop over each sentence
        sentences = []
        for raw_sentence in raw_sentences:
            # If a sentence is empty, skip it
            if len(raw_sentence) > 0:
                # Otherwise, call review_to_wordlist to get a list of words
                sentences.append( KaggleWord2VecUtility.review_to_wordlist( raw_sentence, \
                  remove_stopwords ))
        #
        # Return the list of sentences (each sentence is a list of words,
        # so this returns a list of lists
        return sentences



data = pd.read_csv('../../data/comments.tsv', header=0, delimiter="\t",
                       quoting=3)

sentences = {} # Initialize an empty list of sentences


#print "Parsing sentences from unlabeled set"
for index, review in data.iterrows():
	sentences[review["id"]] = tokenize.sent_tokenize(review["review"]) 
	'''
	print "\n"
	print "\n"
	print "\n"
		
	print sentences[review["id"]]
	'''

reaction = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
counter = 0
sid = SentimentIntensityAnalyzer()
results = {}
for index, review in sentences.items():
	reaction = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
	counter = 0
	for sentence in review:
			
		ss = sid.polarity_scores(sentence)
		reaction["neg"] += ss["neg"]
		reaction["neu"] += ss["neu"]
		reaction["pos"] += ss["pos"]
		reaction["compound"] += ss["compound"]
		counter += 1
	
	reaction["neg"] /= counter
	reaction["neu"] /= counter
	reaction["pos"] /= counter
	reaction["compound"] /= counter
	results[index] = reaction	
	
	'''
	print "\n"
	for k in sorted(reaction):
		print('{0}: {1}, '.format(k, ss[k]))
	print "\n"	
	'''

# Write the test results
with open('../../data/comments_reaction.csv', 'w') as csvfile:
    fieldnames = ['Movie', 'Reaction']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for index, key  in results.items(): 
    	writer.writerow({'Movie': index, 'Reaction': key})
    