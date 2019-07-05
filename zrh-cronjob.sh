#!/bin/bash

path="/mnt/c/Users/simon/Downloads/workspace/SPYDER/ZRHSpotterTool"
path_tables="./timetables"

telegram_user = "@mnemocron"

# pwd

cd $path
rm "$path_tables/timetable.arrival.special.json"
rm "$path_tables/timetable.departure.special.json"
rm "$path_tables/timetable.arrival.spotter.json"
rm "$path_tables/timetable.arrival.standard.json"
rm "$path_tables/timetable.arrival.tom.spotter.json"
rm "$path_tables/timetable.arrival.tom.standard.json"
rm "$path_tables/timetable.departure.spotter.json"
rm "$path_tables/timetable.departure.standard.json"
rm "$path_tables/timetable.departure.tom.spotter.json"
rm "$path_tables/timetable.departure.tom.standard.json"

python3 get-zrh.py -d $path_tables
python3 sort-flights.py -a "$path_tables/timetable.arrival.standard.json" -b "$path_tables/timetable.arrival.spotter.json" -o "$path_tables/timetable.arrival.special.json"
python3 sort-flights.py -a "$path_tables/timetable.departure.standard.json" -b "$path_tables/timetable.departure.spotter.json" -o "$path_tables/timetable.departure.special.json"
python3 sort-flights.py -a "$path_tables/timetable.arrival.tom.standard.json" -b "$path_tables/timetable.arrival.tom.spotter.json" -o "$path_tables/timetable.arrival.tom.special.json"
python3 sort-flights.py -a "$path_tables/timetable.departure.tom.standard.json" -b "$path_tables/timetable.departure.tom.spotter.json" -o "$path_tables/timetable.departure.tom.special.json"

python3 print-table.py -i "$path_tables/timetable.arrival.special.json" -t "Zurich Airport ZRH - Arrivals (specials)" | telegram-bot -u $telegram_user --stdin
python3 print-table.py -i "$path_tables/timetable.departure.special.json" -t "Zurich Airport ZRH - Departure (specials)" | telegram-bot -u $telegram_user --stdin


