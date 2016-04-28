# data1 
# address price rental latitude longtitude supermarkets laundary subway

# data2
# address city complaint_type descriptor latitude longtitude

# data3 addresses within 1 miles
# houseaddress complaintaddress complaint_type

# join data3 and data1

# address city rental rooms latitude longtitude supermarkets laundary subway complaints1 complaints2 complaints3 

# price
# create a multivaiate model

import googlemaps
import os
from datetime import datetime
import math
def rad(value):
	return (math.pi/180)*value
def distance(lat1,lng1,lat2,lng2):
    radlat1=rad(lat1)
    radlat2=rad(lat2)
    a=radlat1-radlat2
    b=rad(lng1)-rad(lng2)
    s=2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))
    earth_radius=6378.137
    s=s*earth_radius
    if s<0:
        return -s
    else:
        return s	

# -*- coding: utf-8 -*-
keys = []
keyFile = open('keyFile','r')
for line in keyFile.readlines():
	key = line.split('\t')[0]
	keys.append(key)
zillowData = open('zillowData','r')
neighborData = open('neighborData','a')
facility = ['laundry','supermarket','train station']
for key in keys:
	print "use key "+key
	gmaps = googlemaps.Client(key=key)
	r = 1.5
	# Geocoding an address
	count = 0
	for line in zillowData.readlines():
		address = line.split('\t')[1]
		zid = line.split('\t')[0]
		print "deal with no"+str(count+1),zid
		count+=1
		geocode_result = gmaps.geocode(address)
		try:
			lat = geocode_result[0].items()[0][1]['location']['lat']
			lng = geocode_result[0].items()[0][1]['location']['lng']
			# search for nearby
			neighbor = address+"\t"+str(lat)+"\t"+str(lng)
			maximumDis = 50
			for key in facility:
				nearby=gmaps.places_nearby(str(lat)+","+str(lng),keyword=key,rank_by='distance')
				c = 0
				try:
					for place in nearby['results']:
						lt = place['geometry']['location']['lat']
						lg = place['geometry']['location']['lng']
						d = distance(lat,lng,lt,lg)
						if d > r:
							break;
						else:
							c+=1
					lat2 = nearby['results'][0]['geometry']['location']['lat']
					lng2 = nearby['results'][0]['geometry']['location']['lng']
					dist = distance(lat,lng,lat2,lng2)
					neighbor = neighbor + "\t"+str(dist)+"\t"+str(c)
				except Exception,e:
					print e
					neighbor = neighbor + "\t"+str(maximumDis)
			neighborData.write(zid+"\t"+neighbor+"\n")
		except Exception,e:
			print e
			neighborData.write(zid+"\t"+address+"\tnull\tnull\tnull\tnull\tnull\n")
	zillowData.close()
	zillowData = open('zillowData','r')
	zillowData_new = open('zillowData_new','w')
	# drop the 2500 entries that have been used
	for entry in zillowData.readlines()[count:]:
		zillowData_new.write(entry)
	zillowData_new.close()
    ## change shx to your name
	os.remove('zillowData')
	os.rename('zillowData_new','zillowData')
x = distance(40.7307161,-73.727365,40.723879, -73.716336)
print x

