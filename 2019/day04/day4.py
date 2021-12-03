#imports

def hasTwoAdjacentDigits(num):
	textnum = str(num)
	for i in range(len(textnum) - 1):
		if textnum[i] == textnum[i+1]:
			return True
	return False

def hasOneGroupOfTwoAdjacentDigits(num):
	textnum = str(num)
	for i in range(len(textnum) - 1):
		if i == 0:
			#if we are looking at beginning of word
			if textnum[i] == textnum[i+1] and textnum[i+1] != textnum[i+2]:
				return True
		elif i == len(textnum) - 2:
			#if we are looking at end of word
			if textnum[i-1] != textnum[i] and textnum[i] == textnum[i+1]:
				return True
		else:
			#we are in middle of word
			if textnum[i-1] != textnum[i] and textnum[i] == textnum[i+1] and textnum[i+1] != textnum[i+2]:
				return True

def digitsNeverDecrease(num):
	textnum = str(num)
	for i in range(len(textnum) - 1):
		if int(textnum[i]) > int(textnum[i+1]):
			return False
	return True

def part1():
	start = 165432
	end = 707912
	count = 0
	for i in range(start, end + 1):
		if hasTwoAdjacentDigits(i) and digitsNeverDecrease(i):
			count += 1
	print(count)



def part2():
	start = 165432
	end = 707912
	count = 0
	for i in range(start, end+1):
		if hasOneGroupOfTwoAdjacentDigits(i) and digitsNeverDecrease(i):
			#print(i)
			count += 1
	print(count)

def main():
	part1()
	part2()

main()