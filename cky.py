import nltk

from nltk import word_tokenize

table = {}
grammar = {}

class CKY:
	def __init__(self):
		CNF = []
		CNF_File = open('rules.txt','r')
		for line in CNF_File:
			line = line.rstrip('\n')
			CNF.append(line)
		SIZE = len(CNF)
		for i in range(0,SIZE):
			rule = CNF[i].split('->')
			LHS = rule[0].strip()
			RHS = rule[1].strip()
			RHS_Sub_Rules = RHS.split(' ')
			if len(RHS) > 1:
				RHS = RHS_Sub_Rules[0].strip()+' '+RHS_Sub_Rules[len(RHS_Sub_Rules)-1].strip()
			else:
				RHS = RHS_Sub_Rules[0].strip()
			grammar[RHS] = LHS

	
	def parse(self,word):
		word = list(word)
		word.insert(0,'')
		tags = []
		for i in range(1,len(word)):
			tags.append(grammar[word[i]])
		tags.insert(0,'')
		for j in range(1,len(tags)):
			table[(j-1,j)] = tags[j]
			for i in range(j-2,-1,-1):
				for k in range(i+1,j):
					if (i,k) in table and (k,j) in table:
						if table[(i,k)]+' '+table[(k,j)] in grammar:
							table[(i,j)] = grammar[table[(i,k)]+" "+table[(k,j)]]
		if (0,len(tags)-1) in table and table[(0,len(tags)-1)] == 'S':
			print("Parsed")
	

def main():
	sentence = raw_input().strip()
	tokens = word_tokenize(sentence)
	textToken = nltk.pos_tag(tokens,tagset='universal')
	tags = []
	for (word,tag) in textToken:
		tags.append(tag)
	tags.insert(0,'')
	print(tags)

parser = CKY()
word = raw_input().strip()
parser.parse(word)
	
