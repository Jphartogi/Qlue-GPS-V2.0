import GPS as GPS

import RPi.GPIO as GPIO


import serial



ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

def main():
	while True:
		try:
			GPS.powerUp()
			GPS.multiprocess()
			GPS.powerDown()
		except:
			if ser != None:
				ser.close()
			GPS.powerDown()
			GPIO.cleanup()
		if ser != None:
			ser.close()
			GPIO.cleanup()

if __name__ == '__main__':
	main()
