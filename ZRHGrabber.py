#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 10:47:03 2019

@author: simon
"""

from datetime import datetime, timedelta
import urllib
from bs4 import BeautifulSoup
import requests

# ToDo: Tested: headers seem to be not required
# Edit: Seems to be required sometimes
# Notice:
# I tried to use the most recent headers with a super long Cookie string and a
# few additional parameters. The request was rejected.
# These Headers seem to still work fine.
headers = { 'Host': 'www.zurich-airport.com',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.zurich-airport.com/passengers-and-visitors/arrivals-and-departures/',
                'Content-Length': '85',
                'Cookie': 'sc_expview=0; website#lang=en; ASP.NET_SessionId=tewblvuqsehbozbq5yakat2n; __RequestVerificationToken=vIUKElZhB4SVQfWDXu2DyJAYluqyOAecVSwB5sDOniFyFMTvSZJnrZNudEVMbrRzvtLS1v2GurbyFTCScCMOME-ybd81; TS01cd1ab8=018735b6f7dff7a3e09286a67ae052f4e2011617ee8846a666a6630182514b91ee5552f129831d7f6267e740d9595f99ca9149393dae9ac848ae68b61d427320fffd9b5eb9890ba550276dd5bd9c357f6c979b7a89d7ebac45ad4fe23564114c99cdab08f117858652ebe1195e659af262baa071e0bbd6fc395fb0b81a1ebd6bfe2799de00bde795de96bab4b0a8b52993ab0995a2',
                'DNT': '1',
                'Connection': 'keep-alive' }

url_base = 'https://www.zurich-airport.com/api/sitecore/FlightScheduleDetail/'

class ZRHGrabber:
    def __init__(self):
        self.hdr = headers
        self.url_base = url_base
        self.UTC_correction = 4.00

if(int(opts.timeoffs) == 0):
    opts.timeoffs = 0
elif(int(opts.timeoffs) == 1):
    opts.timeoffs = 1
elif(int(opts.timeoffs) == 2):
    opts.timeoffs = 2
elif(int(opts.timeoffs) == 3):
    opts.timeoffs = 3
elif(int(opts.timeoffs) == 4):
    opts.timeoffs = 4
elif(int(opts.timeoffs) == 5):
    opts.timeoffs = 5
        
    def parse_table(self, flighttable):
        dict_flighttable = []
        try:
            for flight in flighttable.tbody.findAll('tr') :
                try:
                    f_code = '' # clear
                    f_code = flight.find('a', attrs={'class', 'main-code'}).text # flight code
                    f_reg  = '' # clear
                    f_reg  = str( flight.find('a', attrs={'class', 'main-code'}).get('title') ) # registration number nested in 'title'
                    f_reg  = f_reg.split('number:')[1].split('<br')[0].strip()
                    f_loc  = flight.find('div', attrs={'class', 'airport'}).contents[0].strip() # location airport
                    f_time = flight.find('td', attrs={'class', 'plan'}).text.replace('\n', '') # scheduled time
                    f_texp = flight.find('td', attrs={'class', 'plan ext'}).text.replace('\n', '') # expected time
                    f_status = flight.find('td', attrs={'class', 'status'}).text.replace('\n', '') # status information
                    f_airc = str( flight.find('a', attrs={'class', 'main-code'}).get('title') )
                    f_airc = f_airc.split('Typ')[1].strip().replace(':', '').replace('e ', '')

                    entry = {}
                    entry['airportinformation'] = {}
                    entry['airportinformation']['airport_city'] = f_loc
                    entry['flightcode'] = f_code
                    entry['masterflight'] = {}
                    entry['masterflight']['registration'] = f_reg
                    entry['masterflight']['aircrafttype'] = f_airc
                    # entry['masterflight']['specialcs'] = {"\"specialcs\":"\"null\""} # unused ?
                    entry['scheduled'] = f_time
                    entry['expected'] = f_texp
                    entry['status'] = f_status

                    dict_flighttable.append({})
                    index = len(dict_flighttable)-1
                    dict_flighttable[index] = entry
                except AttributeError:
                    print('Parsing Error in flight')
                    print(flight)
        except AttributeError:
            # print(flighttable)
            print('Error')

        return dict_flighttable


    def fetch(self, fetch_type='arrival', spotter=False, tomorrow=False):
        if(fetch_type in ['arrival', 'arr', 'arrivals', 'Arrival']):
            fetch_type = 'Arrival'
        elif(fetch_type in ['departure', 'dep', 'departures', 'Departure']):
            fetch_type = 'Departure'
        else:
            raise ValueError('Unknown fetch type [arrival, departure]: {}'.format(fetch_type))

        # set time - 'HH:MM:SS'   ---   GMT/UTC format ! -> Swiss time 06:00:00 would be 04:00:00
        date_today = datetime.now().strftime('%Y-%m-%d')
        if(tomorrow==True):
            date_today = (datetime.now() + timedelta(days=str(opts.timeoffs)) + timedelta(hours=0) ).strftime('%Y-%m-%d')
        utc_time = (datetime.now() - timedelta(minutes = self.UTC_correction*60) ).strftime('%H:00:00')
        if(tomorrow==True):
            utc_time = datetime.now().strftime('00:00:05')
        page_n = 0
        search_term = ''
        if(spotter==True):
            search_term = 'spotter'

        dict_flighttable = {}
        dict_flighttable['timetable'] = []

        # fetch every flight by scrolling through pages
        last_flight_fetched = False
        while(not last_flight_fetched):
            # craft a request
            body = urllib.parse.urlencode({'startDateTime' : date_today + 'T' + utc_time + '.000Z', \
                                     'search' : search_term, \
                                     'page' : str(page_n), \
                                     '__RequestVerificationToken' : ''})
            url = self.url_base + fetch_type + 'DetailData'

            # send POST request and parse using LXML
            response = requests.post(url, data=body, headers=self.hdr)
            parsed_html = BeautifulSoup(response.text, 'lxml')

            # Chech if the website returns a "No Result Title" message when
            # the last page is reached.
            # this is an odd behaviour since in the webbrowser there is no such
            # Error message but the last available flight(s)
            # The Arrival page returns "No Result Title" ...
            # The Departure page returns "No flights found" ...
            end_of_table_error = parsed_html.find('div', attrs={'class', 'desktop-only'}).tbody.findAll('tr')[0].text
            if('No Result' in  end_of_table_error or 'No flights' in end_of_table_error):
                last_flight_fetched = True
            else:
                flighttable = parsed_html.find('div', attrs={'class', 'desktop-only'})

                if (page_n > 0):
                    if(dict_flighttable['timetable'][-1]['flightcode'] in flighttable):
                        last_flight_fetched = True
                        print('last page reached')
                        print(dict_flighttable['timetable'][-1]['flightcode'])

                # TODO: merging of tables not working
                table_to_add = self.parse_table(flighttable)
                dict_flighttable['timetable'].extend(table_to_add)


                page_n = page_n + 1

                if(page_n > 40):  # stop at 40+ requests
                    print('RunawayError: Too many pages requested. Aborting possible infinite loop')
                    last_flight_fetched = True

        return dict_flighttable





"""
<tr>
    <td class="plan">
        <div class="inactive">13:00</div>
    </td>
    <td class="plan ext">
        <div>12:58</div>
    </td>
    <td class="location">
        <div class="airport">OSLO
            <div>Gardermoen Intl.</div>
        </div>
    </td>
    <td class="flight-nr tooltip">
        <a class="main-code" href="/passengers-and-visitors/arrivals-and-departures/airlines-en/?id=SK" title="SAS Scandinavian Airlines &lt;br/&gt; Registration number: LNRGA  &lt;br/&gt; Typ: 737-800">SK 841</a>
        <div class="codeshare-wrap">
            <div class="shade"></div>
            <div class="codeshare">
                <div class="telop">
                    <strong>Codeshare:</strong>
                    <a href="/passengers-and-visitors/arrivals-and-departures/airlines-en/?id=LX" title="SWISS International Air Lines &lt;br/&gt; Operating airline: SAS Scandinavian Airlines &lt;br/&gt; Registration number: LNRGA &lt;br/&gt; Typ: 737-800">LX 4711</a>
                    <a href="/passengers-and-visitors/arrivals-and-departures/airlines-en/?id=OU" title="Croatia Airlines &lt;br/&gt; Operating airline: SAS Scandinavian Airlines &lt;br/&gt; Registration number: LNRGA &lt;br/&gt; Typ: 737-800">OU 5679</a>
                </div>
            </div>
        </div>
    </td>
    <td class="terminal">
        <a href="/~/media/flughafenzh/dokumente/uebersichtsplaene/check-in-12.pdf">1</a>
    </td>
    <td class="baggage">
        <div>15</div>
    </td>
    <td class="status">
        <div class="green">landed</div>
    </td>
</tr>
"""
