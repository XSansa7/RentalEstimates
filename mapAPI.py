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
gmaps = googlemaps.Client(key='AIzaSyBAkUEqtlpkNaHJ1_FFQftIb-nsUByDe80')
zillowData = open('zillowData','r')
neighborData = open('neighborData','w')
facility = ['laundry','supermarket','train station']
r = 1.5
# Geocoding an address
count = 0
for line in zillowData.readlines():
	address = line.split('\t')[1]
	print "deal with no"+str(count+1)
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
		neighborData.write(neighbor+"\n")
	except Exception,e:
		print e
		neighborData.write(address+"\tnull\tnull\tnull\tnull\tnull\n")
x = distance(40.7307161,-73.727365,40.723879, -73.716336)
print x

