# s is a string to evaluate
# returns True if s is a nice string, or False if s is a naughty string
def oldIsNiceOrNaughty(s):
	naughtyStrings = ['ab', 'cd', 'pq', 'xy']
	vowels = ['a', 'e', 'i', 'o', 'u']

	for nS in naughtyStrings:
		if nS in s:
			return False

	vowelCount = 0
	for c in s:
		if c in vowels:
			vowelCount += 1
	if vowelCount < 3:
		return False

	for i in range(len(s)-1):
		if s[i] == s[i+1]:
			return True

	return False

# s is a string to evaluate
# returns True if s is a nice string, or False if s is a naughty string
def newIsNiceOrNaughty(s):
	containsDoublePairs = False
	for i in range(len(s)-2):
		pair = s[i:i+2]
		for j in range(i+2,len(s)):
			if pair == s[j:j+2]:
				containsDoublePairs = True
	if not containsDoublePairs:
		return False

	for i in range(len(s)-2):
		if s[i] == s[i+2]:
			return True
	return False

def part1():
	niceCount = 0
	with open('input.txt') as f:
		for line in f:
			if oldIsNiceOrNaughty(line.strip()):
				niceCount += 1
	print(niceCount)

def part2():
	niceCount = 0
	print(newIsNiceOrNaughty('ieodomkazucvgmuy'))
	with open('input.txt') as f:
		for line in f:
			if newIsNiceOrNaughty(line.strip()):
				niceCount += 1
	print(niceCount)

part1()
part2()