# Given that the index points to a '(' in the string, this method looks for the matching ')' and returns the index for it
def getClosingParan(string, index):
	if string[index] != '(':
		print("Cannot get closing param for string: " + string + " at index: " + str(index))
		quit()
	level = 0

	i = index + 1
	while i < len(string):
		v = string[i]
		if v == ')':
			if level == 0:
				return i
			else:
				level -= 1
		elif v == '(':
			level += 1
		i += 1

	print('Did not find closing param for string: ' + string + " at index: " + str(index))
	quit()


# Evaluates a string that's a mathematical expressions like normal, except that multiplication and addition have same precendence, and so are evaluated right to left
# Only handles addition, multiplication, and parantheses
def oldEvaluate(line):
	eSum = 0
	op = '' # operator (+, *)

	i = 0
	while i < len(line):
		v = line[i]
		# If found digit, process according to op
		if v.isdigit():
			if op == '':
				eSum = int(v)
			elif op == '+':
				eSum += int(v)
			elif op == '*':
				eSum *= int(v)
			else:
				print("Weird operator while processing digit: " + op)
				quit()
		elif v == '+' or v == '*':
			op = v
		elif v == '(':
			# Recursively call evaluate on the string within the parantheses
			cPI = getClosingParan(line, i)
			if op == '+':
				eSum += oldEvaluate(line[i+1:cPI])
			elif op == '*':
				eSum *= oldEvaluate(line[i+1:cPI])
			elif op == '':
				eSum = oldEvaluate(line[i+1:cPI])
			else:
				print("Weird operator while recursive processing: " + op)
				quit()
			i = cPI + 1
		i += 1
	return eSum


# Returns the next non-space value in the string
# Returns 'EOF' if it reaches end of file before finding anything
def getNextValue(line, index):
	i = index + 1
	while i < len(line):
		v = line[i]
		if v != ' ':
			return v
		i += 1
	return 'EOF'


# Evaluates a string that's a mathematical expressions like normal, except that addition has precedence over multiplication
# Only handles addition, multiplication, and parantheses
def newEvaluate(line):
	# print('Enter newEvaluate with line ' + line)
	eSum = 0
	op = '' # operator (+, *)
	i = 0

	while i < len(line):
		v = line[i]
		# print("eSum = " + str(eSum) + ' | v = ' + v)
		# If found digit, process according to op
		if v.isdigit():
			if op == '':
				eSum = int(v)
			elif op == '+':
				eSum += int(v)
			elif op == '*':
				# look forward to see if we can multiply or not
				nV = getNextValue(line, i)
				if nV == '*' or nV == 'EOF':
					eSum *= int(v)
				elif nV == '+':
					# Evaluate the 'second half' of the expression, which is just everything starting with the addition sign
					rSum = newEvaluate(line[i:])
					# print("Returning " + str(eSum) + '*' + str(rSum))
					return eSum * rSum
				else:
					print("Weird next value " + nV + " when parsing line " + line + " from index " + str(i))
					quit()
			else:
				print("Weird operator while processing digit: " + op)
				quit()
		elif v == '+' or v == '*':
			op = v
		elif v == '(':
			# Recurse
			cPI = getClosingParan(line, i)
			parensValue = newEvaluate(line[i+1:cPI])

			if op == '':
				eSum = parensValue
			elif op == '+':
				eSum += parensValue
			elif op == '*':
				# look forward to see if we can multiply or not
				nV = getNextValue(line, cPI + 1)
				if nV == '*' or nV == 'EOF':
					eSum *= parensValue
				elif nV == '+':
					# Evaluate the 'second half' of the expression, which is just everything on the right side of the parantheses
					rSum = newEvaluate(line[i:])
					# print("Returning " + str(eSum) + '*' + str(rSum))
					return eSum * rSum
				else:
					print("Weird next value " + nV + " when parsing line " + line + " from index " + str(i))
					quit()
			else:
				print("Weird operator while processing digit: " + op)
				quit()

			i = cPI + 1
		i += 1
	# print("End Returning " + str(eSum))
	return eSum

def part1():
	runningSum = 0
	with open('input.txt') as f:
		for line in f:
			runningSum += oldEvaluate(line.strip())

	print(runningSum)

def part2():
	runningSum = 0
	with open('input.txt') as f:
		for line in f:
			runningSum += newEvaluate(line.strip())

	print(runningSum)

	# This code works! In retrospect, I should have converted the string into a char array (minus spaces) for easier visualization.

def main():
	part1()
	part2()
main()