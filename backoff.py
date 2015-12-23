from __future__ import division

import nltk
import time
import collections
from collections import defaultdict

from nltk.corpus import brown
from nltk.util import ngrams
from nltk.tokenize import sent_tokenize, word_tokenize

from collections import Counter

BROWN_WORDS = brown.words()

#Let 70% of the words be used for training, and rest be a held out data

LEN = len(BROWN_WORDS)

BOUNDARY = int(7*LEN/10);

words = BROWN_WORDS[0:BOUNDARY]
held_out = BROWN_WORDS[BOUNDARY:]

print("Creating n-grams..")

unigrams = ngrams(words,1)
bigrams = ngrams(words,2)
trigrams = ngrams(words,3)

unigramsC = Counter(unigrams)
bigramsC = Counter(bigrams)
trigramsC = Counter(trigrams)

end = time.time()
print("Done with the n-grams")


discount = 0.5

setA = set()
setB = set()
setC = set()

#create a set of unigrams

for((x,),y) in unigramsC.items():
	setC.add(x)

def words_that_follow(w1):
	setA.clear()
	#bigram counts of type (w1,someOtherWord)
	count = 0
	for ((x,y),z) in bigramsC.items():
		if(x == w1):
			setA.add(y)
			count = count+1
	return count	

def alpha(w1):
	numerator = words_that_follow(w1)
	numerator = numerator * discount
	denominator = unigramsC[(w1,)]
	return numerator/denominator

def countStar(w1,w):
	return bigramsC[(w1,w,)] - discount

def UniMLE(w):
	numerator = unigramsC[(w,)]
	denominator = BOUNDARY
	return numerator/denominator

def summation(w):
	#for given w1 and w, we find those where w1,w don't exist together
	setB = setC - setA
	#unigrams
	ans = 0.0
	for x in setB:
		ans = ans + UniMLE(x)
	return ans

def MLE(w1,w):
	#there are two sets A and B, A is where count(w1,w)>0 and B is where count(w1,w) = 0
	if bigramsC[(w1,w,)]>0: #belongs to set A
		numerator = countStar(w1,w) 
		denominator = unigramsC[(w1,)]
		return numerator/denominator
	else:
		alphaMass = alpha(w1)
		unigramFreq = UniMLE(w)
		numerator = alphaMass * unigramFreq
		denominator = summation(w)
		return numerator/denominator

def assignProb(tokens):
	LEN_TOK = len(tokens)
	PROB = 1.0;
	for i in range(1,LEN_TOK-1):
		PROB  = PROB * MLE(tokens[i-1],tokens[i])
	print(PROB) 

def main():
	while 1 == 1:
		print("Enter a statement / Write exit to exit")
		statement = raw_input().strip()
		if statement == '':
			continue
		if statement == 'exit':
			break
		sentence = statement
		sentence+='.'
		tokens = word_tokenize(sentence)
		assignProb(tokens)

main()
