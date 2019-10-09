#!/usr/bin/python

import sys
import os
import xml.etree.ElementTree
import urllib
import urllib.request
import json
import socket
import time
import math
import yaml

import CALCULATION as calc


## obtain data from the config.yaml file
with open("config.yaml", 'r') as stream:
    try:
        data = yaml.safe_load(stream)
        sim_data = data['SIM']
    except yaml.YAMLError as exc:
        print(exc)


### define parameter from the yaml file

ServerIP = sim_data['ServerIP']
Port = sim_data['Port']
PhoneNum = sim_data['PhoneNum']
imei = sim_data['IMEI']
distance_threshold = sim_data['distance_to_update'] # update GPS position every 20 m
heartbeat_duration = sim_data['heartbeat_duration']


#####3

send_error_counter = 0
rec_buff = ''
hb_counter = 0
new_distance = 0
#####

class sendData:
    
    def __init__(self):

        self.user = { 'email' : 'admin', 'password' : 'admin' }
        self.baseUrl = 'http://traccar.qlue.id:8082'
        
        self.debug = '-v' in sys.argv
        
        self.URL = 'traccar.qlue.id'
        self.port = 5001
        self.so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        
    def connect(self):

        self.so.connect((self.URL, self.port))
        return self.so


    def login(self):
        request = urllib.request.Request(self.baseUrl + '/api/session')
        response = urllib.request.urlopen(request, urllib.parse.urlencode(self.user).encode("utf-8"))
        if self.debug:
            print('\nlogin: %s\n' % repr(json.load(response)))
        return response.headers.get('Set-Cookie')

    def send_heartbeat(self,msg_sent):
         # nmea_lat,nmea_long = self.degree_converter(dec_lat,dec_long)
        # UTC = self.UTC_converter(waktu)

        while True:
            #messages = 'imei:'+imei+';'
            messages = 'imei:'+imei+',A;'

            global hb_counter
            global send_error_counter
            print('hb counter value now',hb_counter)
            
            if hb_counter > heartbeat_duration:
                hb_counter = 0
                
        
                self.so.send(messages.encode('utf-8'))
                print('messagenya:',messages)

                print('heartbeat sent!')
               
            
              
                
            if msg_sent.value == 1:
                hb_counter = 0
            hb_counter = hb_counter + 1
            time.sleep(1)


    def send_message(self,msgs):
        
        global new_distance
        global distance_threshold
        global hb_counter
        split = msgs.split(';')

        #### parameter for the message
        lat = float(split[0])
        longt = float(split[1])
        waktu = float(split[2])
        orientation = split[3]
        altitude = split[4]
        speed = split[5]
        #####

        distance = calc.calculate_distance(lat,longt)
        nmea_lat,nmea_long = calc.degree_converter(lat,longt)
        UTC_date = calc.UTC_converter(waktu)
        UTC_time = calc.UTC_time_converter(waktu)
        messages = 'imei:'+imei+',help me,'+ UTC_date +',,F,'+UTC_time+',A,' + nmea_lat + ',S,' + nmea_long + ',E,'+altitude+','+speed+','+orientation+',1,1,99.9%,1.1%,27;'
        new_distance = new_distance + distance
        print('message is:',messages)
        if new_distance > distance_threshold or distance > distance_threshold:
            print("now sending message")
            new_distance = 0 # reseting the distance counter
            self.so.send(messages.encode('utf-8'))
            
            return True
        else:
            
            return False


        # # nmea_lat,nmea_long = self.degree_converter(dec_lat,dec_long)
        # # UTC = self.UTC_converter(waktu)
        # messages ='imei:1234567890,001,0809231929,13554900601,F,055403.000,A,2244.1870,N,11354.3067,E,0.00,30.1,65.43,1,0,10.5%,0.0%,28;'
        
        # self.so.send(messages.encode('utf-8'))
        # print('messagenya:',messages)

        # print('message sent!')
        # # time.sleep(0.2)
        


  
