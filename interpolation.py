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

inv_c = defaultdict(list)
for k, v in unigramsC.iteritems():
    inv_c[v].append(k)


def MLE(w):
	#choose three values l1, l2 and l3
	

def assignProb(tokens):
	LEN_TOK = len(tokens)
	PROB = 1.0;
	for i in range(0,LEN_TOK-1):
		PROB  = PROB * MLE(tokens[i])
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
