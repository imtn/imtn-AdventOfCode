function findHowMany1s(strArray, index)
	count1 = 0
	for str in strArray
		if str[index] == '1'
			count1 += 1
		end
	end
	return count1
end


function part1(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	bitCount1 = zeros(Int64, length(input[1])) # array that counts how many 1s for each position

	for bNum in input
		for bitPos in 1:length(bitCount1)
			if bNum[bitPos] == '1'
				bitCount1[bitPos] += 1
			end
		end
	end

	gammaRateArray = fill("0", length(bitCount1))
	epsilonRateArray = fill("1", length(bitCount1))
	for i in 1:length(gammaRateArray)
		# for each bit count in bitCount1, if the count is more than half the length of the input array (meaning it appears at least half the time),
		# set the same bit in gammaRateArray to 1 and in epsilonRateArray to 0
		gammaRateArray[i] = bitCount1[i] > length(input)/2 ? "1" : "0"
		epsilonRateArray[i] = bitCount1[i] > length(input)/2 ? "0" : "1"
	end

	gammaRate = parse(Int, join(gammaRateArray), base = 2)
	epsilonRate = parse(Int, join(epsilonRateArray), base = 2)


	println(gammaRate)
	println(epsilonRate)
	println(gammaRate * epsilonRate)
end

function part2(fileName::String)
	file = open(fileName)
	input = readlines(file)
	close(file)

	oxygenArray = copy(input)
	co2Array = copy(input)

	currIndex = 1
	#= Find Oxygen Generator Rating
		while the oxygen array is more than 1
		find how many 1s in current index, then determine if 0 or 1 is more common, tie-broken by 1.
		remove values that don't have that 0 or 1 in the current index
		increment current index
		loop again
	=#
	while length(oxygenArray) > 1
		mostCommonBit = findHowMany1s(oxygenArray, currIndex) >= length(oxygenArray)/2 ? 1 : 0
		filter!(e->parse(Int, e[currIndex]) == mostCommonBit, oxygenArray)
		currIndex += 1
	end

	currIndex = 1
	# Find CO2 Scrubber Rating
	while length(co2Array) > 1
		mostCommonBit = findHowMany1s(co2Array, currIndex) < length(co2Array)/2 ? 1 : 0
		filter!(e->parse(Int, e[currIndex]) == mostCommonBit, co2Array)
		currIndex += 1
	end

	println(oxygenArray)
	println(co2Array)
	println(parse(Int, join(oxygenArray), base = 2) * parse(Int, join(co2Array), base = 2))
end

part2("input.txt")