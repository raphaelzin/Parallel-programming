#!/usr/bin/python3
from datetime import datetime
import threading
import random
import time

class Aircraft (threading.Thread):
	totalPlanes = 1
	airControl = 10
	groundControl = 10

	def __init__(self,name, onAir):
		threading.Thread.__init__(self)
		self.name = name
		self.onAir = onAir
		print ("\nNew plane: ", self.name, "in the air" if onAir else "on the ground ", datetime.now().strftime("%H:%M:%S"))
		if onAir:
			threading.Timer(30*timeSpeed, self.crash).start()
			self.crashProne = True
			Aircraft.airControl -= 1
		else:
			self.crashProne = False
			Aircraft.groundControl -= 1
		Aircraft.totalPlanes += 1

	def run(self):
		dispatchPlane(self)

	def crash(self):
		if self.crashProne:
			print ("CRASH (" + self.name + ") " +  datetime.now().strftime("%H:%M:%S"))


def createAircraftsOnAir():
	plane = Aircraft("AirForce %d" % Aircraft.totalPlanes,True)
	planesOnAir.append(plane)
	airportDetails()
	plane.start()

def createAircraftsOnGround():
	plane = Aircraft("AirForce %d" % Aircraft.totalPlanes,False)
	planesOnGround.append(plane)
	plane.start()
	airportDetails()

def airportDetails():
	print ("Planes in the air = [" + ", ".join( str(x.name) for x in planesOnAir) + "]")
	print ("Planes on the ground = [" + ", ".join( str(x.name) for x in planesOnGround) + "]")
	print ("\n")

def createPlane():
	createOnGround = bool(random.getrandbits(1))
	# print("### Ground? "  + str(createOnGround) + " ### Airs: " + str(len(planesOnAir)) + "/" + str(Aircraft.airControl) + " ### Grounds: " + str(len(planesOnGround)) + "/" + str(Aircraft.groundControl)) 

	if (createOnGround or (Aircraft.groundControl > 0 and Aircraft.airControl == 0)) :
		createAircraftsOnGround()
		if len(planesOnGround) > queueSize:
			print("GROUND CRASH")
	elif Aircraft.airControl > 0:
		createAircraftsOnAir()

	if (Aircraft.groundControl + Aircraft.airControl) == 0:
		print("\nAll planes were created\n")
	else:
		threading.Timer(8*timeSpeed, createPlane,[]).start()


def createFromFile():
	print(str(abs(Aircraft.airControl + Aircraft.groundControl-20)) + " : " + fileQueue[(abs(Aircraft.airControl + Aircraft.groundControl-20))])
	print("### Airs: " + str(len(planesOnAir)) + "/" + str(Aircraft.airControl) + " ### Grounds: " + str(len(planesOnGround)) + "/" + str(Aircraft.groundControl)) 

	if fileQueue[(abs(Aircraft.airControl + Aircraft.groundControl-20))] == "G":
		createAircraftsOnGround()
	else:
		createAircraftsOnAir()

	if (Aircraft.groundControl + Aircraft.airControl) == 0:
		print("\nAll planes were created\n")
	else:
		threading.Timer(8*timeSpeed, createFromFile,[]).start()


def dispatchPlane(plane):
	if not plane.onAir:
		groundLock.acquire()

	if plane.onAir:
		airLock.acquire()

	if not runway.locked:
		if ( len(planesOnAir) == 0 or len(planesOnGround) >= queueSize )and groundLock.locked():
			groundLock.release()
		if not len(planesOnGround) >= queueSize and airLock.locked():
			airLock.release()

	runway.acquire()

	if not airLock.locked():
		airLock.acquire()
	if not groundLock.locked():
		groundLock.acquire()

	if plane.onAir:
		plane.crashProne = False

		print ("------ %s Landing ------ (%s) \n" % (plane.name, datetime.now().strftime("%H:%M:%S")))

		planesOnAir.remove(plane)
		time.sleep(10*timeSpeed)

		print ("------ %s Arrived ------ (%s) \n" % (plane.name, datetime.now().strftime("%H:%M:%S")))

	else:
		planesOnGround.remove(plane)

		# Se não for o primeiro avião, espera
		if Aircraft.groundControl + Aircraft.airControl != 19:
			print ("------ %s Will take off ------ (%s) \n" % (plane.name, datetime.now().strftime("%H:%M:%S")))
			time.sleep(5*timeSpeed)

		print ("------ %s Taking off ------ (%s) \n" % (plane.name, datetime.now().strftime("%H:%M:%S")))

		time.sleep(5*timeSpeed)

		print ("------ %s took off ------ (%s) \n" % (plane.name, datetime.now().strftime("%H:%M:%S")))

	if ( len(planesOnAir) == 0 or len(planesOnGround) >= queueSize )and groundLock.locked():
		groundLock.release()
	if not len(planesOnGround) >= queueSize and airLock.locked():
		airLock.release()

	runway.release()

countAir = 10
countGround = 10

total = 30
queueSize = 4

# 1 - normal speed
# 0.5 - 2x fast
timeSpeed = 1

planesOnAir = []
planesOnGround = []
runway = threading.Lock()


airLock = threading.Lock()
groundLock = threading.Lock()

# FROM FILE

# file = open('queue.txt', "r")
# fileQueue = list(file.readline())
# createFromFile()

# FROM FILE END

createPlane()