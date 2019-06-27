# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 10:33:29 2019

@file 			get-zrh.py
@brief 			download arrivals and departures from ZRH (Airport Zurich)
@author 		Simon Burkhardt - simonmartin.ch - github.com/mnemocron
@date 			2019-06
@description 	

@bug 			It seems like the last few flights appear twice in all the files.
				The problem is most likely at the determination of lastFlightFetched = True

"""


"""
JSON format kept from the old ZRH website's api

{
	"timetable":[{
	    "airportinformation": {
	        "airport_city": "DUBLIN"
	    },
	    "flightcode": "EI349",
	    "masterflight": {
	        "registration": "EIDEN"
	    }, 
	    "scheduled": "20:05", 
	    "expected" : "20:20"
	},{
		[...]
	}
}
"""

#%%


from ZRHGrabber import ZRHGrabber
import json
import os

# Writes a dict in json format to a file
def dump_to_json_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=4, sort_keys=True)

def main():
    try:
        zrh = ZRHGrabber()
        
        departures_standard = zrh.fetch('Departure', spotter=False, tomorrow=False)
        departures_spotter  = zrh.fetch('Departure', spotter=True, tomorrow=False)
        arrival_standard    = zrh.fetch('Arrival', spotter=False, tomorrow=False)
        arrival_spotter     = zrh.fetch('Arrival', spotter=True, tomorrow=False)
        
        departures_standard_tomorrow = zrh.fetch('Departure', spotter=False, tomorrow=False)
        departures_spotter_tomorrow  = zrh.fetch('Departure', spotter=True, tomorrow=False)
        arrival_standard_tomorrow    = zrh.fetch('Arrival', spotter=False, tomorrow=False)
        arrival_spotter_tomorrow     = zrh.fetch('Arrival', spotter=True, tomorrow=False)
        # pprint.pprint(table_departures_standard)
        
        dump_to_json_file(departures_standard, 'timetables/timetable.departures.standard.json')
        dump_to_json_file(departures_spotter, 'timetables/timetable.departures.spotter.json')
        dump_to_json_file(arrival_standard, 'timetables/timetable.arrival.standard.json')
        dump_to_json_file(arrival_spotter, 'timetables/timetable.arrival.spotter.json')
        dump_to_json_file(departures_standard_tomorrow, 'timetables/timetable.departures.tom.standard.json')
        dump_to_json_file(departures_spotter_tomorrow, 'timetables/timetable.departures.tom.spotter.json')
        dump_to_json_file(arrival_standard_tomorrow, 'timetables/timetable.arrival.tom.standard.json')
        dump_to_json_file(arrival_spotter_tomorrow, 'timetables/timetable.arrival.tom.spotter.json')
        dump_to_json_file(departures_standard, 'timetables/timetable.departures.spotter.json')
        
    # enables abortion of the program through CTRL + C
    except KeyboardInterrupt:
        print('')
        exit(0)

if __name__ == '__main__':
    main()








