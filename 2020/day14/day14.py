# takes in an unmasked value and uses the bitmask to return a masked value
# bitmask is a string that represents a bitmask
# val is an int representing an unmasked integer
# Returns an integer representing the masked value
def maskValue(bitmask, val):
	# print("Mask called with: " + bitmask + ' ' + str(val))
	unmaskedBinaryString = '{:036b}'.format(val)

	if len(unmaskedBinaryString) != 36 or len(bitmask) != 36:
		print("Unmasked or bitmask not len 36: " + unmaskedBinaryString + ' ' + str(bitmask))
		quit()

	maskedBinaryString = ''
	for i, v in enumerate(unmaskedBinaryString):
		maskedBinaryString += v if bitmask[i] == 'X' else bitmask[i]

	return int(maskedBinaryString, 2)

# takes in an unmasked address and uses the bitmask to return a list of all possible addresses
# bitmask is a string that represents a bitmask
# addr is an int representing an unmasked integer
# Returns a list of strings, representing all possible addresses
def maskAddress(bitmask, addr):
	# print("Mask address")
	# print(bitmask)
	# print(addr)
	unmaskedBinaryAddr = '{:036b}'.format(addr)

	if len(unmaskedBinaryAddr) != 36 or len(bitmask) != 36:
		print("Unmasked or bitmask not len 36: " + unmaskedBinaryAddr + ' ' + str(bitmask))
		quit()

	maskedBinaryAddrStr = ''
	for i, v in enumerate(unmaskedBinaryAddr):
		if bitmask[i] == '0':
			maskedBinaryAddrStr += unmaskedBinaryAddr[i]
		elif bitmask[i] == '1':
			maskedBinaryAddrStr += '1'
		elif bitmask[i] == 'X':
			maskedBinaryAddrStr += 'X'
		else:
			print("Bad bitmask in maskAddress: " + bitmask + ' ' + str(i) + ' ' + bitmask[i])
			quit()

	intAddrs = []
	queueToUnmask = [maskedBinaryAddrStr]
	while len(queueToUnmask) > 0:
		addr = queueToUnmask.pop(0)
		if 'X' not in addr:
			intAddrs.append(int(addr, 2))
		else:
			xIndex = addr.index('X')
			addr0 = addr[:xIndex] + '0' + addr[xIndex+1:]
			addr1 = addr[:xIndex] + '1' + addr[xIndex+1:]
			queueToUnmask.append(addr0)
			queueToUnmask.append(addr1)
	return intAddrs

def part1():
	bitmask = ''
	memory = dict()
	with open('input.txt') as f:
		for line in f:
			if line[:3] == 'mas':
				bitmask = line.split('=')[1].strip()
			elif line[:3] == 'mem':
				address = int(line.split('=')[0].strip()[4:-1])
				unmaskedValue = int(line.split('=')[1].strip())
				maskedValue = maskValue(bitmask, unmaskedValue)
				memory[address] = maskedValue
			else:
				print("Bad line when reading line: " + line)
				quit()

	runningSum = 0
	for v in memory:
		runningSum += memory[v]
	print('Part 1 Sum == ' + str(runningSum))

def part2():
	bitmask = ''
	memory = dict()
	with open('input.txt') as f:
		for line in f:
			if line[:3] == 'mas':
				bitmask = line.split('=')[1].strip()
			elif line[:3] == 'mem':
				address = int(line.split('=')[0].strip()[4:-1])
				val = int(line.split('=')[1].strip())
				maskedAddrs = maskAddress(bitmask, address)
				for a in maskedAddrs:
					memory[a] = val

			else:
				print("Bad line when reading line: " + line)
				quit()

	runningSum = 0
	for v in memory:
		runningSum += memory[v]
	print('Part 2 Sum == ' + str(runningSum))

def main():
	part1()
	part2()
main()