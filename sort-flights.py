#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 11:50:40 2019

@author: simon
"""

#%%

import json
import os
import optparse
from FlightEntry import FlightEntry

parser = optparse.OptionParser('filter-specials')
parser.add_option('-a', '--standard-flights', dest='flt_std', type='string', help='timetable.[arr,dep].standard.json')
parser.add_option('-b', '--spotter-flights',  dest='flt_spt', type='string', help='timetable.[arr,dep].spotter.json')
parser.add_option('-o', '--output-file',      dest='outfile', type='string', help='output file name and destination')
parser.add_option('-d', '--dict',             dest='dict',    type='string', help='dictionary file')
# parser.add_option('-d', '--dict', dest='dict', type='string', help='dict.json')
(opts, args) = parser.parse_args()

# default location
path_prefix = './timetables/'
path_standard = path_prefix + 'timetable.arrival.standard.json'
path_spotter  = path_prefix + 'timetable.arrival.spotter.json'
path_special  = path_prefix + 'timetable.zrh.arrival.json'  # for the special flights
path_dict     = './dict.json'

# check if input files is given and exists
if(opts.flt_std is not None):
    if(os.path.exists(opts.flt_std)):
        path_standard = opts.flt_std
    else:
        raise FileNotFoundError('Input file not found: {}'.format(opts.flt_std))
if(opts.flt_spt is not None):
    if(os.path.exists(opts.flt_spt)):
        path_spotter = opts.flt_spt
    else:
        raise FileNotFoundError('Input file not found: {}'.format(opts.flt_spt))
if(opts.outfile is not None):
    path_special = opts.outfile
if(opts.dict is not None):
    if(os.path.exists(opts.dict)):
        path_dict = opts.dict
    else:
        raise FileNotFoundError('Input file not found: {}'.format(opts.flt_spt))

# Writes a dict in json format to a file
def dump_to_json_file(data, filename):
    with open(filename, 'w+', encoding='utf-8') as fh:
        json.dump(data, fh, indent=4, sort_keys=True)

def main():
    try:
        # open the two files and parse them to a dict
        with open(path_standard) as stdFile:
            table_standard = json.load(stdFile)
        with open(path_spotter) as spotFile:
        	table_spotter = json.load(spotFile)
        with open(path_dict) as dictFile:
        	table_dict = json.load(dictFile)
        
        # convert the dicts to lists for easier comparison
        array_std = []
        array_spt = []
        array_dict = []
        for entry in table_standard['timetable']:
            flight = FlightEntry(entry)
            array_std.append(flight)
        for entry in table_spotter['timetable']:
            flight = FlightEntry(entry)
            array_spt.append(flight)
        for entry in table_dict['timetable']:
            flight = FlightEntry(entry)
            array_dict.append(flight)
        
        # single sided comparison
        # only look for special flights that are: 
        # in spotter but not in standard OR
        # in dict (dict overrides normal filtering)
        array_special = [x for x in array_spt if not x in array_std or x in array_dict]
        # double sided comparison
        # array_special = [*[x for x in array_spt if not x in array_std], *[x for x in array_std if not x in array_spt]]
        
        table_special = {}
        table_special['timetable'] = []
        for entry in array_special:
            table_special['timetable'].append(entry.raw)
        
        dump_to_json_file(table_special, path_special)
        print('[+] sorting done!')
        
    # enables abortion of the program through CTRL + C
    except KeyboardInterrupt:
        print('')
        exit(0)

if __name__ == '__main__':
    main()


