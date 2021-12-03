import re

# passport should be a dictionary mapping each field to its value
# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# 	If cm, the number must be at least 150 and at most 193.
# 	If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.
def isValid(passport):
	eyeColors = {'amb','blu','brn','gry','grn','hzl','oth'}
	requiredFields = {"byr","iyr","eyr","hgt","ecl","hcl","pid"}

	# if passport missing any required fields, return False
	for rF in requiredFields:
		if rF not in passport:
			return False

	# check each field
	if int(passport['byr']) < 1920 or int(passport['byr']) > 2002:
		return False
	if int(passport['iyr']) < 2010 or int(passport['iyr']) > 2020:
		return False
	if int(passport['eyr']) < 2020 or int(passport['eyr']) > 2030:
		return False

	#validate height
	if re.search("[0-9]+(cm|in)", passport['hgt']) == None:
		return False
	val = int(passport['hgt'][:-2])
	unit = passport['hgt'][-2:]
	if unit == 'cm' and (val < 150 or val > 193):
		return False
	if unit == 'in' and (val < 59 or val > 76):
		return False
	if unit != "cm" and unit != "in":
		print("Height Validation Errored: " + passport['hgt'])
		return False

	if re.search("#[0-9a-f]{6}", passport['hcl']) == None:
		return False
	if passport['ecl'] not in eyeColors:
		return False
	if re.search("^[0-9]{9}$", passport['pid']) == None:
		return False

	return True


def part1():
	with open('input.txt') as f:
		fieldSet = set()
		requiredFields = {"byr","iyr","eyr","hgt","ecl","hcl","pid"}
		validNum = 0
		for line in f:
			# if line == "\n":
			# 	print("NEWLINE")
			# else:
			# 	print(line.strip())
			if line == "\n":
				# print('----')
				# print(fieldSet)
				# print(requiredFields <= fieldSet)
				if requiredFields <= fieldSet: # If requiredFields is a subset of fieldSet
					validNum += 1
				fieldSet = set()
			else:
				splitByColon = line.strip().split(':')[:-1] # splits by colon, then removes the last element, which doesn't contain any fields
				fieldList = [x[-3:] for x in splitByColon] # for every element in splitByColon, gets the last 3 letters, which are the field
				fieldSet.update(fieldList)

		# for end of file, where it doesn't end in \n
		if requiredFields <= fieldSet: # If requiredFields is a subset of fieldSet
					validNum += 1

		print(validNum)

def part2():
	with open('input.txt') as f:
		passportDict = dict()
		validNum = 0

		for line in f:
			if line == "\n":
				if isValid(passportDict): # If requiredFields is a subset of fieldSet
					validNum += 1
				passportDict = dict()
			else:
				splitLine = line.strip().split(' ') # splits by space to get list of key-value pairs like 'key:value'
				tempDict = {x.split(':')[0]: x.split(':')[1] for x in splitLine}
				passportDict.update(tempDict)
				
		# for end of file, where it doesn't end in \n
		if isValid(passportDict): # If requiredFields is a subset of fieldSet
			validNum += 1

		print(validNum)

def main():
	# part1()
	part2()
main()
	