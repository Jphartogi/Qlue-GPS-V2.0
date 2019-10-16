#!/usr/bin/python
# -*- coding:utf-8 -*-
from math import sin, cos, sqrt, atan2, radians
import math
lat_arr = []
longt_arr = []
waktu_arr = []



def UTC_converter(data):
    UTC = str(int(data))
    UTC = UTC[2:len(UTC)-2]

    return UTC

def UTC_time_converter(waktu):
    UTC = str(int(waktu))
    UTC = UTC[len(UTC)-6:len(UTC)]
    UTC = UTC + '.000'

    return UTC


def degree_converter(dec_lat,dec_long):

	a,b = math.modf(dec_lat)
	a = a*60
	nmea_lat = str(int(b)) + str(a)

	c,d = math.modf(dec_long)
	c = c*60
	nmea_long = str(int(d)) + str(c)

	return nmea_lat,nmea_long

def calculate_distance(lat,longt):
    # approximate radius of earth in km

    R = 6373.0
    lat = radians(lat)
    longt = radians(longt)


    lat_arr.append(lat)
    longt_arr.append(longt)


    if len(lat_arr) and len(longt_arr) > 1:
    	long2 = longt_arr[1]
    	long1 = longt_arr[0]
    	lat2 = lat_arr[1]
    	lat1 = lat_arr[0]

    	dlon = long2 - long1
    	dlat = lat2 - lat1

    	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    	c = 2 * atan2(sqrt(a), sqrt(1 - a))

    	distance = R * c *1000 # so it will be in m

    	#print("Result:", distance)

    	del longt_arr[0]
    	del lat_arr[0]

    	return distance
    else:
    	pass
    	return 0
