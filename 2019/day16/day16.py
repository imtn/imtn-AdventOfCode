import sys

def part1():
	with open("input.txt") as f:
		signalString = f.readline().strip()
	signal = list(signalString)
	for index, elem in enumerate(signal):
		signal[index] = int(elem)

	basePattern = [0,1,0,-1]
	phase = 1
	while phase <= 100:
		# loop through each element and calculate it
		newSignal = []
		for index, element in enumerate(signal):
			# first, calculate the pattern for this index
			patternForIndex = []
			for number in basePattern:
				patternForIndex.extend([number] * (index+1))

			indexForPattern = 1 # problem asks to start on the second element
			sumForIndex = 0
			# in order to get the value for this element
			# we loop through all elements in signal again
			# multiply by the pattern at the pattern's index
			# then add to running sum
			# after finish looping
			# get the one's digit from the sum and add that to the array
			for number in signal:
				sumForIndex += (number * patternForIndex[indexForPattern])
				indexForPattern = (indexForPattern + 1) % len(patternForIndex)
			digit = abs(sumForIndex) % 10
			newSignal.append(digit)
		signal = newSignal

		phase += 1
	print(signal)

def part2():
	with open("input.txt") as f:
		signalString = f.readline().strip()
		offset = int(signalString[:7])
	signal = list(signalString)
	for index, elem in enumerate(signal):
		signal[index] = int(elem)

	# extend signal by 10,000
	signal.extend(signal*9999)

	# What's different in part 2 is that:
	# 	the signal is much longer
	# 	the result is not the first 8 numbers, but the 8 numbers at the offset
	# 		for the input, the offset is 5,973,847
	# One thing I know is that
	# 	the value at position x is only affected by the values at position >= x
	# 	so I can skip calculating the values for positions < x
	# Thankfully, the offset is after half of the array
	# Which means the pattern for everything at and after the offset is 1
	# which means all I need to do is sum everything from position to 0
	# where position goes from last index backwards to the offset

	basePattern = [0,1,0,-1]
	phase = 1
	while phase <= 100:
		print("On phase " + str(phase))

		# every phase
		# loop through signal from end of array to offset
		# have a running sum
		# and for each phase
		# 	add current digit to sum
		# 	set current digit as last digit of sum
		runningSum = 0
		for i in range(len(signal) - 1, offset - 1, -1):
			runningSum += signal[i]
			signal[i] = runningSum % 10

		phase += 1
		
	print("Message is: ")
	print(str(signal[offset:offset+8]))

def main():
	#part1()
	part2()

main()