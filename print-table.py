#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 13:31:20 2019

@author: simon
"""

#%%
import json
import os
import optparse

parser = optparse.OptionParser('print-table.py')
parser.add_option('-i', '--table', dest='infile', type='string', help='input file to pretty print')
parser.add_option('-t', '--title', dest='title', type='string', help='title text before the print')
# parser.add_option('-d', '--dict', dest='dict', type='string', help='dict.json')
(opts, args) = parser.parse_args()

# default location
path_prefix = './timetables/'
path_table = path_prefix + 'timetable.arrival.special.json'

title = 'Zurich Airport ZRH - Arrivals (specials)'

if(opts.infile is not None):
    if(os.path.exists(opts.infile)):
        path_table = opts.infile
    else:
        raise FileNotFoundError('Input file not found: {}'.format(opts.infile))

if(opts.title is not None):
    title = str(opts.title)

def main():
    try:
        with open(path_table) as stdFile:
            table = json.load(stdFile)
        
        print(title)
        print('STA / Code / Reg / Type / City')
        for flight in table['timetable']:
            time_sched = flight['scheduled']
            code = flight['flightcode']
            reg = flight['masterflight']['registration']
            plane = flight['masterflight']['aircrafttype']
            city = flight['airportinformation']['airport_city']
            print(time_sched + ' ' + code + ' ' + reg + ' ' + plane + ' ' + city)
            
    # enables abortion of the program through CTRL + C
    except KeyboardInterrupt:
        print('')
        exit(0)

if __name__ == '__main__':
    main()
    