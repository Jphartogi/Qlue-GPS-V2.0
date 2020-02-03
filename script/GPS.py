#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import sendData as sd
import webcam as webcam
import serial
import time
import re
import yaml
from multiprocessing import Process,Queue,Value


ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

## obtain data from the config.yaml file
with open("/app/script/config.yaml", 'r') as stream:
    try:
        data = yaml.safe_load(stream)
        GPS_data = data['GPS']
    except yaml.YAMLError as exc:
        print(exc)


## define the fixed parameter
GPS_power_key = 4
SIM_power_key = 6
rec_buff = ''
rec_buff2 = ''
time_count = 0
status = False



#define the non-fixed variable
time_delay = GPS_data['time_to_update'] # update GPS position every x seconds


# initialize class send data
sd_data = sd.sendData()


def power_on():
	print('SIM7600X is starting:')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	GPIO.setup(GPS_power_key,GPIO.OUT)
	GPIO.setup(SIM_power_key,GPIO.OUT)
	time.sleep(0.1)
	GPIO.output(GPS_power_key,GPIO.HIGH)
	GPIO.output(SIM_power_key,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(GPS_power_key,GPIO.LOW)
	GPIO.output(SIM_power_key,GPIO.LOW)
	time.sleep(2)
	ser.flushInput()
	print('SIM7600X is ready')

def power_down():
	print('SIM7600X is loging off:')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	GPIO.setup(GPS_power_key,GPIO.OUT)
	GPIO.setup(SIM_power_key,GPIO.OUT)
	GPIO.output(GPS_power_key,GPIO.HIGH)
	GPIO.output(SIM_power_key,GPIO.HIGH)
	time.sleep(3)
	GPIO.output(GPS_power_key,GPIO.LOW)
	GPIO.output(SIM_power_key,GPIO.LOW)
	time.sleep(2)
	print('Good bye')


def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(0.5)
	counter = 0
	#time.sleep(timeout)
	while ser.inWaiting() == 0 and counter < timeout * 100:
	       counter = counter + 1
	       
		   #print('value in waiting : ',ser.inWaiting())

	time.sleep(0.01)

	rec_buff = ser.read(ser.inWaiting())


	result = rec_buff.decode('utf-8')

	


	if rec_buff != '':
		if back not in rec_buff.decode():
			print(command + ' ERROR')
			print(command + ' back:\t' + rec_buff.decode())
			return 0
		else:
			print(result)
			status = decode_pos(result)

			if status == True:
				return 2
			elif status == False:
				return 99
			return 1

	else:
		print('GPS is not ready')
		return 0

def decode_pos(result):

        #string_int =re.findall('[-+]?\d*\.\d+|\d+',result)
        #string_int =re.findall('[-+]?\d+\.\d+',result) for searching the negative value
        string_int =re.findall('\d+\.\d+',result) # for searching only the number
        
        if len(string_int) < 6:
            #list is empty gps has not still worked
            print('NO GPS SIGNAL!')
            print('  ')
            return False
            
        else:
            msg =  string_int[1] + '; ' + string_int[2] + ';' + string_int[0] + ';' + string_int[3] + ';' + string_int[4] + ';' + string_int[5]
            print(' ')
            print('GET GPS SIGNAL!')
            #msg = 'http://maps.google.com/?q=' + string_int[1] + ',' + string_int[2]
            status = sd_data.send_message(msg)

            return status

def start_gps():
	print('Start GPS session...')
	answer_gps = 0
	while answer_gps < 1:
		answer_gps = send_at('AT+CGNSPWR=1','OK',1)
	print('GPS READY!')
	sd_data.logOn()
	print('Connection 4G LTE ready!')




def heart_beat(q,msg_sent):
	sd_data.send_heartbeat(msg_sent)
	pass

def takePic(q,status):
    webcam.takePicture(status)

def get_gps_position(q,msg_sent):
	rec_null = True
	answer = 0

	rec_buff = ''


	while rec_null:

		answer = send_at('AT+CGNSINF','+CGNSINF: ',1)


		if 1 == answer:
			answer = 0
			if ',,,,,,' in rec_buff:
				print('GPS is not ready')
				rec_null = False
				time.sleep(1)
		elif answer == 2:
			msg_sent.value = 1
		elif answer == 99:
			msg_sent.value = 0


		else:
			print('error %d'%answer)
			rec_buff = ''
			send_at('AT+CGPS=0','OK',2)
			answer_gps = 0
			while answer_gps < 1:
				answer_gps = send_at('AT+CGNSPWR=1','OK',1)
			print('GPS READY!')
			
			time.sleep(time_delay)
		
def powerUp():
	power_on()

	start_gps()

def powerDown():
	power_down()


def multiprocess():
    q = Queue()
    msg_sent = Value('i')

    p1 = Process(target=get_gps_position,args=(q,msg_sent))
    p2 = Process(target=heart_beat,args=(q,msg_sent))
    #p3 = Process(target=takePic,args=(q,status))
    p1.start()
    p2.start()
    #p3.start()

    p1.join()
    p2.join()
    #p3.join()

