#!/bin/bash

user="YourUsername"
path="/home/$user/workspace/ZRHSpotterTool"
path_tables="$path/timetables"
telegram_user="@dxmekch"

# Move to directory $path
cd $path

# Delete the last downloads except the sorted files
rm "$path_tables/timetable.arrival.spotter.json" > /dev/null 2>&1
rm "$path_tables/timetable.arrival.standard.json" > /dev/null 2>&1
rm "$path_tables/timetable.arrival.tom.spotter.json" > /dev/null 2>&1
rm "$path_tables/timetable.arrival.tom.standard.json" > /dev/null 2>&1
rm "$path_tables/timetable.departure.spotter.json" > /dev/null 2>&1
rm "$path_tables/timetable.departure.standard.json" > /dev/null 2>&1
rm "$path_tables/timetable.departure.tom.spotter.json" > /dev/null 2>&1
rm "$path_tables/timetable.departure.tom.standard.json" > /dev/null 2>&1

# Download the newest flights
python3 get-zrh.py -d $path_tables

# Delete old sorted files
rm "$path_tables/timetable.zrh.arrival.json" > /dev/null 2>&1
rm "$path_tables/timetable.zrh.departure.json" > /dev/null 2>&1
rm "$path_tables/timetable.zrh.tom.arrival.json" > /dev/null 2>&1
rm "$path_tables/timetable.zrh.tom.departure.json" > /dev/null 2>&1

# Sort the new files
python3 sort-flights.py -a "$path_tables/timetable.arrival.standard.json" -b "$path_tables/timetable.arrival.spotter.json" -o "$path_tables/timetable.zrh.arrival.json"
python3 sort-flights.py -a "$path_tables/timetable.departure.standard.json" -b "$path_tables/timetable.departure.spotter.json" -o "$path_tables/timetable.zrh.departure.json"
python3 sort-flights.py -a "$path_tables/timetable.arrival.tom.standard.json" -b "$path_tables/timetable.arrival.tom.spotter.json" -o "$path_tables/timetable.zrh.tom.arrival.json"
python3 sort-flights.py -a "$path_tables/timetable.departure.tom.standard.json" -b "$path_tables/timetable.departure.tom.spotter.json" -o "$path_tables/timetable.zrh.tom.departure.json"


# send via custom telegram script - OPT IN for use
# python3 print-table.py -i "$path_tables/timetable.zrh.arrival.json" -t "Zurich Airport ZRH - Arrivals (specials)" | telegram-bot -u $telegram_user --stdin
# python3 print-table.py -i "$path_tables/timetable.zrh.departure.json" -t "Zurich Airport ZRH - Departure (specials)" | telegram-bot -u $telegram_user --stdin


