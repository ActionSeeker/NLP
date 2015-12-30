from __future__ import division

import nltk

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import math
from math import log

import numpy
import cython
import scipy

from collections import defaultdict

from nltk.util import ngrams
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize

class authors:
    def __init__(self,author):
        self.unigrams = []
        self.words = []
        self.unknownUnigrams = []
        self.unknownUnigramsC = []
        self.array = ['story1','story2','story3','story4','story5']
        if author == 'EAP':
            self.authorName = 'Edger Allan Poe'
            self.prefix = 'EAP/'
        elif author == 'GDM':
            self.authorName = 'Guy De Maussapant'
            self.prefix = 'GDM/'
        #gather lines
        for word in self.array:
            f = open(self.prefix+word,'r')
            for line in f:
                line = line.rstrip('\n')
                tokens = word_tokenize(line)
                self.words = self.words + tokens
            f.close()
        self.unigrams = ngrams(self.words,1)
        self.unigramsC = Counter(self.unigrams)

    def readFile(self,fileName):
        self.unknownUnigrams =[]
        f = open(fileName,'r')
        for line in f:
            line = line.rstrip('\n')
            tokens = word_tokenize(line)
            self.unknownUnigrams = self.unknownUnigrams + tokens
        f.close()
        self.N = len(self.unknownUnigrams)
        self.BOUNDARY = self.N
        self.unknownUnigrams = ngrams(self.unknownUnigrams,1)
        self.unknownUnigramsC = Counter(self.unknownUnigrams)
        self.logP = 0.0
        self.counter = 0
        self.mathWork()
        for (x,) in self.unknownUnigramsC:
            if self.unknownUnigramsC[(x,)] == 1:
                self.logP = self.logP + log(self.probability(x))
                self.counter = self.counter + 1;
        self.logAns = self.logP/self.counter
        print(math.exp(self.logAns))

    def probability(self,word):
        self.numerator = 1.0;
        self.numerator = self.unigramsC[(word,)]
        if self.numerator == 0.0:
            return 1
        self.denominator = len(self.words)
        return self.numerator/self.denominator

EAP = authors('EAP')
GDM = authors('GDM')

EAP.readFile('SAMPLE/sample2')
GDM.readFile('SAMPLE/sample2')
