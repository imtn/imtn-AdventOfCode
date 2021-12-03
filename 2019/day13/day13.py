import sys
from threading import Thread, Lock, Event
import time
from PIL import Image

#Globals for sharing data between intcode and maincode
globalInput = []
globalOutput = []
inputMutex = Lock()
outputMutex = Lock()
inputFlag = Event() # Set when globalInput is populated
outputFlag = Event() # Set when globalOutput is populated 
waitForInput = Event()

def getInput():
	#userInput = input("getInput() >>> ")

	# wait for inputFlag to be true
	waitForInput.set()
	inputFlag.wait()
	inputMutex.acquire()
	try:
		userInput = globalInput.pop(0)
	finally:
		inputMutex.release()
		inputFlag.clear()
	return userInput

def setOutput(output):
	# there may be timing issues
	# if intcode program calls this function in succession
	# while somewhere else is waiting for the flag

	while outputFlag.is_set():
		pass # what's the right way to do this?
	outputMutex.acquire()
	try:
		globalOutput.append(output)
		# if len(globalOutput) == 3:
		# 	outputFlag.set()
	finally:
		outputMutex.release()

	#print("setOutput() >>> " + str(output))

def getAddrGivenParamMode(programDict, paramDigit, dictIndex, relativeBase):
	# programDict is the dictionary that represents the program. All memory outside program defaults to 0
	# paramDigit is a single positive digits that represents how to get the value
	# 	0 - position mode - return programDict[dictIndex] as the new index
	# 	1 - immediate mode - return dictIndex
	# 	2 - relative mode - take programDict[dictIndex] as baseModifier,
	#							and then return relativeBase + baseModifier as the new index
	# dictIndex is the index of programDict that this paramDigit decides how we get
	# relativeBase is the relative base for relative mode
	# returns the address and not the value that paramDigit, dictIndex, and relativeBase indicate
	paramDigit = int(paramDigit)

	if paramDigit == 0:
		# position mode

		return programDict.get(dictIndex, 0)

	elif paramDigit == 1:
		# immediate mode

		return dictIndex

	elif paramDigit == 2:
		# relative mode

		baseModifier = programDict.get(dictIndex, 0) # I don't see this happening, but just in case
		return baseModifier + relativeBase

	else:
		print("Got weird paramDigit: " + str(paramDigit) + str(type(paramDigit)))
		sys.exit()
		return

def intcode(filename):
	with open(filename) as f:
		program = dict() # store the program as a dictionary so we can access memory outside the program
		inputArray = f.readlines()[0].split(',')
		for index, value in enumerate(inputArray):
			program[index] = int(value) # Make each value an integer, not a string

		# Run the opcode program, stop on 99
		index = 0 # this is the pointer
		relativeBase = 0 # this is the relative base
		while True:
			num = program[index]
			param = str(num // 100).zfill(3)
			op = num % 100
			# print("index is " + str(index))
			# print("four numbers are " + str(num) + " " + str(program[index+1]) + " " + str(program[index+2]) + " " + str(program[index+3]))

			if op == 99:
				# End Processing, and do whatever needs to happen before exiting
				print("Finished processing.")
				return

			elif op == 1:
				# Take val1 at pos1, add it to val2 at pos2, and store it in pos3

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				pos3 = getAddrGivenParamMode(program, param[0], index + 3, relativeBase)
				program[pos3] = val1 + val2

				index += 4

			elif op == 2:
				# Take val1 at pos1, multiply it to val2 at pos2, and store it in pos3

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				pos3 = getAddrGivenParamMode(program, param[0], index + 3, relativeBase)
				program[pos3] = val1 * val2

				index += 4

			elif op == 3:
				# Get input and store in pos1

				pos1 = getAddrGivenParamMode(program, param, index + 1, relativeBase)
				program[pos1] = int(getInput())

				index += 2

			elif op == 4:
				# Output value in pos1

				val1 = program.get(getAddrGivenParamMode(program, int(param), index + 1, relativeBase), 0)
				setOutput(val1)

				index += 2

			elif op == 5:
				# jump if true
				# if val1 is non-zero, set index to val2
				# otherwise, advance index normally

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				if val1 != 0:
					index = val2
				else:
					index += 3

			elif op == 6:
				# jump if not true
				# if val1 is zero, set index to val2
				# otherwise, advance index normally

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				if val1 == 0:
					index = val2
				else:
					index += 3

			elif op == 7:
				# less than
				# if val1 < val2 then store ONE in pos3
				# else store 0 in pos3

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				pos3 = getAddrGivenParamMode(program, param[0], index + 3, relativeBase)
				program[pos3] = 1 if val1 < val2 else 0

				index += 4

			elif op == 8:
				# equal to
				# if val1 == val2 then store ONE in pos3
				# else store 0 in pos3

				val1 = program.get(getAddrGivenParamMode(program, param[2], index + 1, relativeBase), 0)
				val2 = program.get(getAddrGivenParamMode(program, param[1], index + 2, relativeBase), 0)
				pos3 = getAddrGivenParamMode(program, param[0], index + 3, relativeBase)
				program[pos3] = 1 if val1 == val2 else 0

				index += 4

			elif op == 9:
				# adjust relative base
				# relative base += val1
				# val1 may be negative

				val1 = program.get(getAddrGivenParamMode(program, int(param), index + 1, relativeBase), 0)
				relativeBase += val1

				index += 2

			else:
				print("Found a different opcode: " + str(op))
				print("Exiting...")
				sys.exit()

def part1():
	intcodeProgram = Thread(target = intcode, args = ("inputpart1.txt", ))
	intcodeProgram.start()
	imageArray = dict() # maps (x,y) to block
	brownCount = 0
	# Hardcoded max is (37,21)

	intcodeProgram.join()
	while globalOutput:
		x = globalOutput.pop(0)
		y = globalOutput.pop(0)
		block = globalOutput.pop(0)
		imageArray[(x, y)] = block
		# print("Added " + str((x, y)) + " with block " + str(block))

	im = Image.new("RGB", (40,25))
	for pixel in imageArray.keys():
		color = 0
		if imageArray[pixel] == 0:
			#Empty tile, draw white
			color = (255,255,255)
		elif imageArray[pixel] == 1:
			#Wall tile, red
			color = (255,0,0)
		elif imageArray[pixel] == 2:
			#block tile, draw brown
			color = (150,75,0)
			brownCount += 1
		elif imageArray[pixel] == 3:
			#paddle tile, draw blue:
			color = (0,0,255)
		elif imageArray[pixel] == 4:
			#ball tile, draw green
			color = (0,255,0)
		im.putpixel(pixel, color)
	print(brownCount)
	im.show()

def part2():
	# we need to "play" the game
	# we keep running, don't worry about output initially
	# wait until getInput called
	# call output, build board screen
	# then get user input
	# then repeat waiting for getInput to be called

	intcodeProgram = Thread(target = intcode, args = ("inputpart2.txt", ))
	intcodeProgram.start()
	imageArray = dict() # maps (x,y) to block
	score = 0
	# Hardcoded max is (37,21)
	frames = []


	while intcodeProgram.is_alive():

		if not waitForInput.wait(timeout = 3):
			alive = intcodeProgram.is_alive()
			print("waitForInput timed out, program thread is alive? " + str(alive))
			if not alive:
				print(globalOutput)
				break

		# first, get input and populate image array
		while globalOutput:
			x = globalOutput.pop(0)
			y = globalOutput.pop(0)
			block = globalOutput.pop(0)
			if x == -1 and y == 0:
				#set score
				score = block
				print("Score set to " + str(score))
			else:
				#add pixel to imageArray
				imageArray[(x,y)] = block
				# print("Added " + str((x, y)) + " with block " + str(block))

		# then, draw and display image
		# instead of displaying the image, let's save it to frames
		# to show as a gif later
		im = Image.new("RGB", (40,25))
		ballX = "default"
		paddleX = "another default"
		for pixel in imageArray.keys():
			color = 0
			if imageArray[pixel] == 0:
				#Empty tile, draw white
				color = (255,255,255)
			elif imageArray[pixel] == 1:
				#Wall tile, red
				color = (255,0,0)
			elif imageArray[pixel] == 2:
				#block tile, draw brown
				color = (150,75,0)
			elif imageArray[pixel] == 3:
				#paddle tile, draw blue:
				color = (0,0,255)
				paddleX = pixel[0]
			elif imageArray[pixel] == 4:
				#ball tile, draw green
				color = (0,255,0)
				ballX = pixel[0]
			else:
				print("We got a weird color here: " + str(imageArray[pixel]))
				sys.exit()
			im.putpixel(pixel, color)
		# im.show()
		frames.append(im)

		#Finally, ask for input
		# userJoystickInput = int(input("-1 for left, 0 for no movement, 1 for right >>> "))

		# instead of user input, we should move the paddle (blue, 3) to the ball (green, 4)
		if ballX > paddleX:
			# ball to right of paddle, move paddle right
			userJoystickInput = 1
		elif ballX < paddleX:
			# ball to left of paddle, move paddle left
			userJoystickInput = -1
		else:
			#ball above paddle, don't move
			userJoystickInput = 0
		# print("deriving input: " + str(userJoystickInput))
		globalInput.append(userJoystickInput)
		waitForInput.clear()
		inputFlag.set()

	# save frames as a gif
	frames[0].save("gameplay.gif", append_images = frames[1:], duration = 100, loop = 0, save_all = True)


def main():
	#part1()
	part2()

main()