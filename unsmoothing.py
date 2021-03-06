from __future__ import division

import nltk
import time
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

def MLE(w1,w):
	numerator = bigramsC[(w1,w,)]
	denominator = unigramsC[(w1,)]
	ans = 0.0;
	if denominator >0 : return float(numerator)/float(denominator)
	return ans

def assignProb(tokens):
	LEN_TOK = len(tokens)
	PROB = 1.0;
	for i in range(1,LEN_TOK):
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
		tokens = word_tokenize(sentence)
		assignProb(tokens)

main()
