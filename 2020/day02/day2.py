def part1():
	passingPWCount = 0
	with open("input.txt") as f:
		for line in f:
			least = int(line.split('-')[0])
			most = int(line.split('-')[1].split(' ')[0])
			letter = line.split(':')[0].split(' ')[1]
			password = line.split(':')[1].strip()
			# print(least)
			# print(most)
			# print(letter)
			# print(password)
			# print('--------')

			letterCount = password.count(letter)
			if least <= letterCount and letterCount <= most:
				passingPWCount += 1
	print(passingPWCount)

def part2():
	passingPWCount = 0
	with open("input.txt") as f:
		for line in f:
			num1 = int(line.split('-')[0])
			num2 = int(line.split('-')[1].split(' ')[0])
			letter = line.split(':')[0].split(' ')[1]
			password = line.split(':')[1].strip()
			# print(num1)
			# print(num2)
			# print(letter)
			# print(password)
			# print('--------')

			pos1 = num1-1
			pos2 = num2-1
			if password[pos1] == letter or password[pos2] == letter:
				if password[pos1] == letter and password[pos2] == letter:
					continue
				passingPWCount += 1
	print(passingPWCount)

def main():
	part1()
	part2()
main()