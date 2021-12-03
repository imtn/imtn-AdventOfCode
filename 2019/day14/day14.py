import math

def part1():

	# store each line/reaction as an entry
	# with the mapping OUTPUT CHEMICAL => (amount, [(INPUT CHEMICAL, amount)])
	reactions = dict()

	with open("input.txt") as f:
		for line in f:
			reaction = line.split("=>")

			# we assume that the output is unique, and contains only one element
			output = reaction[1].strip().split()
			outputAmount = int(output[0])
			outputChemical = output[1]
			reactions[outputChemical] = (outputAmount, [])

			# we will loop through inputs and append them to the reactions dictionary
			# input is the name of a function, so Cinput is a chemical input
			Cinputs = reaction[0].strip().split(", ")
			for Cinput in Cinputs:
				inputAmount = int(Cinput.split(" ")[0])
				inputChemical = Cinput.split(" ")[1]
				reactions[outputChemical][1].append((inputChemical, inputAmount))

		# for output in reactions.keys():
		# 	print(str(output) + " <= " + str(reactions[output]))


	oreCount = 0
	queue = [("FUEL", 1)]
	excessChemicals = dict() # maps chemical=>excessAmount

	#this is where the magic happens
	while queue:
		currentItemTuple = queue.pop(0)
		(currItem, currNeededAmount) = currentItemTuple

		#if it's ore, increment oreCount
		if currItem == "ORE":
			oreCount += currNeededAmount
		else:
			# If there is any excess of currItem
			# then apply it
			if currItem in excessChemicals:
				minOfExcessAndCurrNeededAmount = min(excessChemicals[currItem], currNeededAmount)
				excessChemicals[currItem] -= minOfExcessAndCurrNeededAmount
				currNeededAmount -= minOfExcessAndCurrNeededAmount
				if excessChemicals[currItem] == 0:
					del excessChemicals[currItem]

			# Get number of times reaction producing currItem is run
			(rxnOutAmount, inputs) = reactions[currItem]
			rxnRunCount = math.ceil(currNeededAmount / rxnOutAmount)

			# if I still have to run the reaction
			if rxnRunCount != 0:
				# calculate excess of currItem
				excessCurrAmount = (rxnRunCount * rxnOutAmount) - currNeededAmount
				# if there is excess, store it
				if excessCurrAmount != 0:
					excessChemicals.setdefault(currItem, 0)
					excessChemicals[currItem] += excessCurrAmount

			# loop through inputs and add them to the queue
			for Cinput in inputs: # Cinput looks like (inputChemical, inputAmount)
				(inputChemical, inputAmount) = Cinput
				inputAmount *= rxnRunCount
				queue.append((inputChemical, inputAmount))



		# print("Excess is:")
		# print(excessChemicals)
		# print("\n~~~~~~~~\n")

	print("oreCount is " + str(oreCount))

def calculateOre(fuelAmount):
	# store each line/reaction as an entry
	# with the mapping OUTPUT CHEMICAL => (amount, [(INPUT CHEMICAL, amount)])
	reactions = dict()

	with open("input.txt") as f:
		for line in f:
			reaction = line.split("=>")

			# we assume that the output is unique, and contains only one element
			output = reaction[1].strip().split()
			outputAmount = int(output[0])
			outputChemical = output[1]
			reactions[outputChemical] = (outputAmount, [])

			# we will loop through inputs and append them to the reactions dictionary
			# input is the name of a function, so Cinput is a chemical input
			Cinputs = reaction[0].strip().split(", ")
			for Cinput in Cinputs:
				inputAmount = int(Cinput.split(" ")[0])
				inputChemical = Cinput.split(" ")[1]
				reactions[outputChemical][1].append((inputChemical, inputAmount))

		# for output in reactions.keys():
		# 	print(str(output) + " <= " + str(reactions[output]))


	oreCount = 0
	queue = [("FUEL", fuelAmount)]
	excessChemicals = dict() # maps chemical=>excessAmount

	#this is where the magic happens
	while queue:
		currentItemTuple = queue.pop(0)
		(currItem, currNeededAmount) = currentItemTuple

		#if it's ore, increment oreCount
		if currItem == "ORE":
			oreCount += currNeededAmount
		else:
			# If there is any excess of currItem
			# then apply it
			if currItem in excessChemicals:
				minOfExcessAndCurrNeededAmount = min(excessChemicals[currItem], currNeededAmount)
				excessChemicals[currItem] -= minOfExcessAndCurrNeededAmount
				currNeededAmount -= minOfExcessAndCurrNeededAmount
				if excessChemicals[currItem] == 0:
					del excessChemicals[currItem]

			# Get number of times reaction producing currItem is run
			(rxnOutAmount, inputs) = reactions[currItem]
			rxnRunCount = math.ceil(currNeededAmount / rxnOutAmount)

			# if I still have to run the reaction
			if rxnRunCount != 0:
				# calculate excess of currItem
				excessCurrAmount = (rxnRunCount * rxnOutAmount) - currNeededAmount
				# if there is excess, store it
				if excessCurrAmount != 0:
					excessChemicals.setdefault(currItem, 0)
					excessChemicals[currItem] += excessCurrAmount

			# loop through inputs and add them to the queue
			for Cinput in inputs: # Cinput looks like (inputChemical, inputAmount)
				(inputChemical, inputAmount) = Cinput
				inputAmount *= rxnRunCount
				queue.append((inputChemical, inputAmount))

	return oreCount

def part2():
	# one trillion is 1000000000000
	# one trillion ore creates 3343477 fuel
	# print(calculateOre(3290000))
	# return

	# continually run calculateOre until it runs the largest number below one trillion
	prevOreAmount = 0
	fuelAmount = 3290000
	while True:
		newOreAmount = calculateOre(fuelAmount)
		print("tried fuel amount " + str(fuelAmount))
		if newOreAmount >= 1000000000000:
			print("One trillion ore takes this much fuel: " + str(fuelAmount - 1))
			break
		fuelAmount += 1
		prevOreAmount = newOreAmount


def main():
	#part1()
	part2()

main()