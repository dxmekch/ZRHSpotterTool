#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 10:33:29 2019

@file                   get-zrh.py
@brief                  download arrivals and departures from ZRH (Airport Zurich)
@author                 Simon Burkhardt - simonmartin.ch - github.com/mnemocron
@date                   2019-06
@description

@bug                    It seems like the last few flights appear twice in all the files.
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
import optparse

parser = optparse.OptionParser('get-zrh')
parser.add_option('--today',    dest='today',    action='store_true', default=False, help='only fetch flights for today')
parser.add_option('--tomorrow', dest='tomorrow', action='store_true', default=False, help='only fetch flights for tomorrow')
parser.add_option('--standard', dest='std',      action='store_true', default=False, help='only fetch standard table')
parser.add_option('--spotter',  dest='spt',      action='store_true', default=False, help='only fetch spotter table')
parser.add_option('--arrivals',   dest='arr',    action='store_true', default=False, help='only fetch arrivals')
parser.add_option('--departures', dest='dep',    action='store_true', default=False, help='only fetch departures')
parser.add_option('--offset', dest='timeoffs', default=1, help='only fetch timeoffset')
parser.add_option('-d', '--out-dir', dest='out_dir', type='string',   default='./timetables/', help='output directory for json files')
(opts, args) = parser.parse_args()

# if none is selected, default to all
if(opts.today == False and opts.tomorrow == False):
    opts.today = True
    opts.tomorrow = True

if(opts.std == False and opts.spt == False):
    opts.std = True
    opts.spt = True

if(opts.arr == False and opts.dep == False):
    opts.arr = True
    opts.dep = True
    
if(opts.timeoffs >= 0):
  opts.timeoffs = int(opts.timeoffs)

# Writes a dict in json format to a file
def dump_to_json_file(data, filename):
    with open(filename, 'w+', encoding='utf-8') as fh:
        json.dump(data, fh, indent=4, sort_keys=True)

def main():
    try:
        if(os.path.exists(opts.out_dir)):
            outdir = opts.out_dir
        else:
            raise FileNotFoundError('Output directory not found')

        if(outdir[-1] not in ['/']):
            outdir = outdir + '/'

        zrh = ZRHGrabber()

        if(opts.today):
            if(opts.std):
                if(opts.arr):
                    print('[+] downloading (standard) (arrivals)  (today) ...')
                    arrival_standard    = zrh.fetch('Arrival', spotter=False, tomorrow=False)
                    dump_to_json_file(arrival_standard,             outdir + 'timetable.arrival.standard.json')
                if(opts.dep):
                    print('[+] downloading (standard) (depatures) (today) ...')
                    departures_standard = zrh.fetch('Departure', spotter=False, tomorrow=False)
                    dump_to_json_file(departures_standard,          outdir + 'timetable.departure.standard.json')
            if(opts.spt):
                if(opts.arr):
                    print('[+] downloading (spotter)  (arrivals)  (today) ...')
                    arrival_spotter     = zrh.fetch('Arrival', spotter=True, tomorrow=False)
                    dump_to_json_file(arrival_spotter,              outdir + 'timetable.arrival.spotter.json')
                if(opts.dep):
                    print('[+] downloading (spotter)  (depatures) (today) ...')
                    departures_spotter  = zrh.fetch('Departure', spotter=True, tomorrow=False)
                    dump_to_json_file(departures_spotter,           outdir + 'timetable.departure.spotter.json')

        if(opts.tomorrow):
            if(opts.std):
                if(opts.arr):
                    print('[+] downloading (standard) (arrivals)  (tomorrow) ...')
                    arrival_standard_tomorrow    = zrh.fetch('Arrival', spotter=False, tomorrow=True)
                    dump_to_json_file(arrival_standard_tomorrow,    outdir + 'timetable.arrival.tom.standard_' + str(opts.timeoffs) + '.json')
                if(opts.dep):
                    print('[+] downloading (standard) (departures) (tomorrow) ...')
                    departures_standard_tomorrow = zrh.fetch('Departure', spotter=False, tomorrow=True)
                    dump_to_json_file(departures_standard_tomorrow, outdir + 'timetable.departure.tom.standard_' + str(opts.timeoffs) + '.json')
            if(opts.spt):
                if(opts.arr):
                    print('[+] downloading (spotter)  (arrivals)  (tomorrow) ...')
                    arrival_spotter_tomorrow     = zrh.fetch('Arrival', spotter=True, tomorrow=True)
                    dump_to_json_file(arrival_spotter_tomorrow,     outdir + 'timetable.arrival.tom.spotter_' + str(opts.timeoffs) + '.json')
                if(opts.dep):
                    print('[+] downloading (spotter)  (departures) (tomorrow) ...')
                    departures_spotter_tomorrow  = zrh.fetch('Departure', spotter=True, tomorrow=True)
                    dump_to_json_file(departures_spotter_tomorrow,  outdir + 'timetable.departure.tom.spotter_' + str(opts.timeoffs) + '.json')

        print('[+] fetching done!')
    # enables abortion of the program through CTRL + C
    except KeyboardInterrupt:
        print('')
        exit(0)

if __name__ == '__main__':
    main()
