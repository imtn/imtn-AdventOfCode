import hashlib

def part1():
	secretKey = 'yzbqklnj' # puzzle input

	for i in range(1000000):
		md5Value = hashlib.md5((secretKey + str(i)).encode()).hexdigest()
		# print(md5Value)
		if md5Value[0:5] == '00000':
			print(i)
			print(md5Value)
			break

def part2():
	secretKey = 'yzbqklnj' # puzzle input

	for i in range(999999999):
		md5Value = hashlib.md5((secretKey + str(i)).encode()).hexdigest()
		# print(md5Value)
		if md5Value[0:6] == '000000':
			print(i)
			print(md5Value)
			break

part1()
part2()