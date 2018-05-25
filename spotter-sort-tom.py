#!/usr/bin/python

try:
	import json
	import sys
	import os
except:
	print ("error: library missing")
	exit()

if( len(sys.argv) < 3 ):
	print("error: no files provided")
	print("usage:")
	print("\tspotter-sort.py standard.json spotter.json")
	exit()

pathStd = sys.argv[1]
pathSpot = sys.argv[2]

try:
	with open(pathStd) as stdFile:
		jsonstd = json.load(stdFile)
	with open(pathSpot) as spotFile:
		jsonspot = json.load(spotFile)
			# open dictionary file and parse to json. Path to dict.json is hardcoded and should always be the same
	with open("dict.json") as dictFile:
		jsondict = json.load(dictFile)
	with open("mfgz.json") as mfgzFile:
		json_mfgz = json.load(mfgzFile)
		
except:
	print ("error: cannot parse json file: \"" + pathStd + "\" or \"" + pathSpot + "\"")
	exit()

# find out if it is arrival or departure
if ( "arr" in sys.argv[1] ):
	print ("Zurich Airport ZRH - Arrivals")			# start output
	if os.path.exists("timetable.zrh.tom.arrival.json"):
		os.remove("timetable.zrh.tom.arrival.json")		# delete the outdated file
	webfile = open("timetable.zrh.tom.arrival.json", "w")
elif ( "dep" in sys.argv[1] ):
	print ("Zurich Airport ZRH - Departures")
	if os.path.exists("timetable.zrh.tom.departure.json"):
		os.remove("timetable.zrh.tom.departure.json")
	webfile = open("timetable.zrh.tom.departure.json", "w")

webfile.write("{\"timetable\":[")	# begin the json file

for i in range( len(jsonspot["timetable"])-1 ) :	# check every spotter flight
	send = 1	# default: true until proved otherwise


	for k in range( len(jsonstd["timetable"])-1 ) :		# with every standard flight
		if ( jsonspot["timetable"][i]["flightcode"].lower() == jsonstd["timetable"][k]["flightcode"].lower() ) :
			# print (str(i) + " " + jsonspot["timetable"][i]["flightcode"] + " " + jsonspot["timetable"][i]["scheduled"] + " " + jsonspot["timetable"][i]["masterflight"]["registration"] + " " + jsonspot["timetable"][i]["airportinformation"]["airport_city"] + " - EQUALS - " + str(k) + " " + jsonstd["timetable"][k]["flightcode"] + " " + jsonstd["timetable"][k]["scheduled"] + " " + jsonstd["timetable"][k]["masterflight"]["registration"] + " " + jsonstd["timetable"][k]["airportinformation"]["airport_city"])
			send = 0
			break # same as: k = len(jsonstd["timetable"])		# abort second for loop
			
	# added below
	if (send == 0) :
		# duplicate entry -> before discarding definitely, search through special dictionary, if it contains, add it nonetheless
		
		# search matching registration number
		for k in range( len(jsondict["timetable"])-1 ) :
			if ( jsonspot["timetable"][i]["masterflight"]["registration"].lower() == jsondict["timetable"][k]["masterflight"]["registration"].lower() ) :
				send = 1 # add it since it's in special dictionary
				break
	# added above
	
	if (send == 1) :
		try:
			print ( jsonspot["timetable"][i]["scheduled"] + " " + jsonspot["timetable"][i]["flightcode"] + " " + jsonspot["timetable"][i]["masterflight"]["registration"] + " " + jsonspot["timetable"][i]["masterflight"]["aircrafttype"] + " " + jsonspot["timetable"][i]["airportinformation"]["airport_city"])
		except:	# if the "registration" element is missing, print a N/A
			try:
				print (jsonspot["timetable"][i]["scheduled"] + "\t" + "\t" + "N/A" + "\t" + "\t")
			except:
				print ("unhandled error with this flight")
		# dumps encodes the json string
		webfile.write( json.dumps(jsonspot["timetable"][i], indent=4, sort_keys=True) + ",")
# ugly way to terminate the json file, but it works anyways
webfile.write("{\"null\":\"null\"}]}")
