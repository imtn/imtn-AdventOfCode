# Takes in a dictionary of rules and returns a set of all possible strings that fit ruleNum, recursively
def calcSet(rules, ruleNum):
	stringSet = set()
	rule = rules[ruleNum]
	if rule[0][0] == '\"':
		stringSet.add(rule[0][1])
	else:
		if '|' in rule: # rules with pipes
			if rule.count('|') > 1:
				print("More than one | in rule " + rule + ' for ruleNum ' + ruleNum)
				quit()

			cumulSet = set()
			for comp in rule[:rule.index('|')]: # for each component in rule before pipe
				if len(cumulSet) == 0:
					cumulSet = calcSet(rules, comp).copy()
				else:
					tempSet = set()
					for s in cumulSet:
						for c in calcSet(rules, comp):
							tempSet.add(s + c)
					cumulSet = tempSet.copy()
			stringSet |= cumulSet

			cumulSet = set()	
			for comp in rule[rule.index('|') + 1:]: # for each component in rule after pipe
				if len(cumulSet) == 0:
					cumulSet = calcSet(rules, comp).copy()
				else:
					tempSet = set()
					for s in cumulSet:
						for c in calcSet(rules, comp):
							tempSet.add(s + c)
					cumulSet = tempSet.copy()
			stringSet |= cumulSet

		else: # Rules with no pipes
			for comp in rule: # for each component in rule
				newSet = set()
				if len(stringSet) == 0:
					stringSet = calcSet(rules, comp).copy()
				else:
					for s in stringSet:
						for c in calcSet(rules, comp):
							newSet.add(s + c)
					stringSet = newSet.copy()
	return stringSet


# Matches any number of fourtwos, followed by any number of threeones that is less than the number of fourtwos
# String is a string to check if it matches
# fourtwos is a set of strings that match eight
# threeones is a set of strings that match threeones
# returns True if it matches the rule in the first line, and False otherwise.
def matchEightEleven(string, fourtwos, threeones):
	# assumes all strings in fourtwos and all strings in threeones have the same length
	sLen = len(list(fourtwos)[0])
	numOf42s = 0
	numOf31s = 0
	state = 0 # 0 is matching fourtwos, 1 is matching threeones

	i = 0
	while i < len(string):
		# print('evaluating ' + string[i:i+sLen] + ' in string ' + string)
		# print(str(state) + ' | ' + str(numOf42s) + ' | ' + str(numOf31s))
		if state == 0:
			if string[i:i+sLen] in fourtwos:
				numOf42s += 1
			else:
				state += 1
				continue
		elif state == 1:
			if string[i:i+sLen] in threeones:
				numOf31s += 1
			else:
				state += 1
				continue
		else:
			return False
		i += sLen
	# print("String, num42s, and num31s are " + string + ' | ' + str(numOf42s) + ' | ' + str(numOf31s))
	return numOf42s > numOf31s and numOf31s > 0


def part1():
	state = 0 # 0 means parsing rules, 1 means matching text
	rules = dict()
	zero = set() # set of all strings that match rule 0
	matchingMessages = 0

	with open('input.txt') as f:
		for line in f:
			if line == '\n':
				state += 1
				zero = calcSet(rules, '0')
				# print(zero)
				# return
			elif state == 0:
				ruleNum = line.split(':')[0].strip() # a string that represents a number
				rule = line.split(':')[1].strip().split(' ') # a list of numbers and pipes
				rules[ruleNum] = rule
			elif state == 1:
				if line.strip() in zero:
					matchingMessages += 1
			else:
				print("Weird state: " + state)
				print(line)
				quit()

	print(matchingMessages)

def part2():
	state = 0 # 0 means parsing rules, 1 means matching text
	rules = dict()
	zero = set() # set of all strings that match rule 0
	matchingMessages = 0


	eight = ['42','|','42','8'] # any number of 42s, followed by
	eleven = ['42','31','|','42','11','31'] # any number of 42s followed by a matching number of 31s
	# Meaning that 0: 8 11
	# Means any number of 42s, followed by a lesser number of 31s
	set42 = set()
	set31 = set()

	with open('input.txt') as f:
		for line in f:
			if line == '\n':
				state += 1
				rules['8'] = eight
				rules['11'] = eleven
				set42 = calcSet(rules, '42')
				set31 = calcSet(rules, '31')
				print(set42)
				print(set31)
				# print(matchEightEleven('bbbbbbbaaaabbbbaaabbabaaa', set42, set31))
				# return
			elif state == 0:
				ruleNum = line.split(':')[0].strip() # a string that represents a number
				rule = line.split(':')[1].strip().split(' ') # a list of numbers and pipes
				rules[ruleNum] = rule
			elif state == 1:
				if matchEightEleven(line.strip(), set42, set31):
					matchingMessages += 1
			else:
				print("Weird state: " + state)
				print(line)
				quit()

	print(matchingMessages)

def main():
	#part1() # This takes about 15 seconds
	part2()
main()