#!/bin/bash

path="/mnt/c/Users/simon/Downloads/workspace/SPYDER/ZRHSpotterTool"
path_tables="./timetables"
telegram_user="@mnemocron"

# pwd

cd $path

# rm "$path_tables/timetable.arrival.special.json" > /dev/null 2>&1
# rm "$path_tables/timetable.departure.special.json" > /dev/null 2>&1

rm "$path_tables/timetable.arrival.spotter.json" > /dev/null 2>&1
rm "$path_tables/timetable.arrival.standard.json" > /dev/null 2>&1
rm "$path_tables/timetable.arrival.tom.spotter.json" > /dev/null 2>&1
rm "$path_tables/timetable.arrival.tom.standard.json" > /dev/null 2>&1
rm "$path_tables/timetable.departure.spotter.json" > /dev/null 2>&1
rm "$path_tables/timetable.departure.standard.json" > /dev/null 2>&1
rm "$path_tables/timetable.departure.tom.spotter.json" > /dev/null 2>&1
rm "$path_tables/timetable.departure.tom.standard.json" > /dev/null 2>&1

rm "$path_tables/timetable.zrh.arrival.json" > /dev/null 2>&1
rm "$path_tables/timetable.zrh.departure.json" > /dev/null 2>&1
rm "$path_tables/timetable.zrh.tom.arrival.json" > /dev/null 2>&1
rm "$path_tables/timetable.zrh.tom.departure.json" > /dev/null 2>&1

python3 get-zrh.py -d $path_tables
python3 sort-flights.py -a "$path_tables/timetable.arrival.standard.json" -b "$path_tables/timetable.arrival.spotter.json" -o "$path_tables/timetable.arrival.special.json"
python3 sort-flights.py -a "$path_tables/timetable.departure.standard.json" -b "$path_tables/timetable.departure.spotter.json" -o "$path_tables/timetable.departure.special.json"

python3 sort-flights.py -a "$path_tables/timetable.arrival.spotter.json" -b "$path_tables/timetable.arrival.standard.json" -o "$path_tables/timetable.zrh.arrival.json"
python3 sort-flights.py -a "$path_tables/timetable.departure.spotter.json" -b "$path_tables/timetable.departure.standard.json" -o "$path_tables/timetable.zrh.departure.json"
python3 sort-flights.py -a "$path_tables/timetable.arrival.spotter.json" -b "$path_tables/timetable.arrival.tom.standard.json" -o "$path_tables/timetable.zrh.tom.arrival.json"
python3 sort-flights.py -a "$path_tables/timetable.departure.tom.spotter.json" -b "$path_tables/timetable.departure.tom.standard.json" -o "$path_tables/timetable.zrh.tom.departure.json"

# send via custom telegram script
# python3 print-table.py -i "$path_tables/timetable.arrival.special.json" -t "Zurich Airport ZRH - Arrivals (specials)" | telegram-bot -u $telegram_user --stdin
# python3 print-table.py -i "$path_tables/timetable.departure.special.json" -t "Zurich Airport ZRH - Departure (specials)" | telegram-bot -u $telegram_user --stdin


