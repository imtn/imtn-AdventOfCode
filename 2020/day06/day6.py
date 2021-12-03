def part1():
	# groups is a list of group lists, each which represents one group (separated by a full blank line)
	# group is a list of answers, each of which represents the Yes answers provided by each person (separated by newline)
	groups = []
	group = []
	with open('input.txt') as f:
		for line in f:
			if line == "\n":
				groups.append(group)
				group = []
			else:
				group.append(line.strip())
		# input ends without newline so process one last time
		groups.append(group)
	
	runningSum = 0	
	for g in groups:
		# for each group, count the total amount of unique letters in the group
		letterSet = set()
		for answer in g:
			letterSet.update({letter for letter in answer})
		runningSum += len(letterSet)
	print(runningSum)

def part2():
	# groups is a list of group lists, each which represents one group (separated by a full blank line)
	# group is a list of answers, each of which represents the Yes answers provided by each person (separated by newline)
	groups = []
	group = []
	with open('input.txt') as f:
		for line in f:
			if line == "\n":
				groups.append(group)
				group = []
			else:
				group.append(line.strip())
		# input ends without newline so process one last time
		groups.append(group)
	
	runningSum = 0	
	for g in groups:
		# for each group, count the amount of letters that every person has
		# do this by populating the letter set, and then removing letters which are not in following answers
		letterSet = 0
		for answer in g:
			if letterSet == 0:
				letterSet = {letter for letter in answer}
			else:
				# for each letter in letterSet, add it to newLetterSet only if letter is in answer
				# then set letterSet to newLetterSet
				newLetterSet = set()
				for letter in letterSet:
					if letter in answer:
						newLetterSet.add(letter)
				letterSet = newLetterSet
		runningSum += len(letterSet)
	print(runningSum)

def main():
	part1()
	part2()
main()