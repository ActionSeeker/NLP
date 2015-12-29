import nltk
from nltk import word_tokenize
SRULES = []

class POSTags:
	def __init__(self):
		self.tags = set()
		self.rules = {}
		f = open('tags','r')
		for line in f:
			line = line.strip()
			line = line.rstrip('\n')
			line = line.split('->')
			self.tags.add(line[0].strip())
			line[1] = line[1].strip()
			if line[1] in self.rules.keys():
				#already there, just append
				self.rules[line[1]].append(line[0])
			else:
				self.rules[line[1]] = []
				self.rules[line[1]].append(line[0])
		#print(self.rules)

	def checkTag(self,STRING):
		if STRING in self.tags:
			return True
		return False

	def printTags(self):
		print(self.tags)

	def returnRules(self,key):
		l = []
		for x in self.rules[key]:
			l.append(x+'->'+key)
		return l

tagset = POSTags()

class Rule:
	def __init__(self,STRING,i,j,dot):
		self.i = i
		self.j = j
		self.dot = dot
		self.STRING = STRING.split('->')
		self.lhs = self.STRING[0].strip()
		self.rhs1 = self.STRING[1].strip()
		self.rhs = []
		self.rhs1 = self.rhs1.split(' ')
		for word in self.rhs1:
			if word.strip()!= '':
				self.rhs.append(word)
		self.STRING = ' '.join(self.rhs)
		self.STRING = self.lhs+'->'+self.STRING

	def __eq__(self, other):
		if self.i == other.i:
			if self.j == other.j:
				if self.dot == other.dot:
					if self.lhs == other.lhs:
						if self.rhs == other.rhs:
							return True
		return False


class grammarClass:
		def __init__(self):
			f = open('grammar','r')
			self.g = []
			for line in f:
				line = line.strip()
				line = line.rstrip('\n')
				r = Rule(line,0,0,0)
				self.g.append(r)
				if r.lhs == 'S':
					SRULES.append(r)

grammar = grammarClass()

class EarleyParser:
	def __init__(self,words):
		self.chart = [[] for i in range(len(words)+1)]
		self.LEN = 0
		self.parser(words)

	def parser(self,words):
		begin = Rule('GAMMA -> S',0,0,0)
		self.enqueue(0,begin)
		self.LEN = len(words)
		LENW = len(words)+1
		for i in range(0,LENW):
			if i > 0:
				rList = tagset.returnRules(words[i-1])
				for state in rList:
					self.enqueue(i,Rule(state,i-1,i,1))
			for state in self.chart[i]:
				rule = state
				if self.incomplete(state) and rule.dot < len(rule.rhs) and tagset.checkTag(rule.rhs[rule.dot]) == False:
					self.predictor(rule)
				elif self.incomplete(state)and rule.dot < len(rule.rhs) and tagset.checkTag(rule.rhs[rule.dot]) == True:
					self.scanner(rule)
				else:
					self.completer(rule)
		'''ctr = 0
		for i in range(0,LENW):
			for rule in self.chart[i]:
				print(rule.STRING+' ['+str(rule.i)+','+str(rule.j)+']'+' .'+str(rule.dot))
				ctr = ctr+1
		print(ctr)'''
		for rules in self.chart[LENW-1]:
			if rules.lhs == 'S':
				print("Parsed")


	def enqueue(self,entry,state):
		if state in self.chart[entry] :
			return None
		else:
			self.chart[entry].append(state)

	def incomplete(self,rule):
		LENRHS = len(rule.rhs)
		if rule.dot != LENRHS+1:
			return True
		return False

	def predictor(self,rule):
		#print("Predictor")
		for rules in grammar.g:
			if rules.lhs == rule.rhs[rule.dot]:
				#rule is of form A -> alpha (DOT)B beta [i,j]
				#rules is of form B -> (DOT) gamma
				self.enqueue(rule.j,Rule(rules.STRING,rule.j,rule.j,0))

	def scanner(self,rule):
		for r in grammar.g:
			if r.lhs == rule.rhs[rule.dot]:
				#r is of form B -> word[j]
				self.enqueue(rule.j+1,Rule(r.STRING,rule.j,rule.j+1,rule.dot+1))

	def completer(self,rule):
		#print("Completer")
		lhs = rule.lhs
		# this rule is of form B -> gamma (DOT) [j,k]
		k = rule.j
		j = rule.i
		for rules in self.chart[j]:
			if rules.dot < len(rules.rhs) and rules.rhs[rules.dot] == lhs:
				#this rule is of form A -> alpha (DOT) B beta [i,j] in chart[j]
				i = rules.i
				self.enqueue(k,Rule(rules.STRING,i,k,rules.dot+1))

parser = EarleyParser(word_tokenize("they are flying planes"))
