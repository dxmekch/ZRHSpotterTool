
# ZRHSpotterTool

---

This Python script can fetch the full arrival / departure list of the Zürich airport (ZRH). The output format is 'json'. There are multiple lists available. Both the arrivals and depatrures of regular civil flights, as well as both the arrivals and departures of all available flights (including private and freight flights). Typically a regular list contains ~400 flights per day, while a spotter list contains ~450 flights.

Furthermore there is a `dict.json` that contains further information for given registration numbers.

### [dxmek.ch/zrharr](https://dxmek.ch/zrharr/)

---

## Usage

### Download Timetables

Get the arrival list (today / regular): `$ zrh-fix-working-beta.py -a`

Get the departure list (toady / regular): `$ zrh-fix-working-beta.py -d`

Get all four available lists of today: `$ zrh-fix-working-beta.py -dau`

Get all four available lists of tomorrow: `$ zrh-fix-working-beta.py -daut`

### Filter Timetables

Filter out the special flights:

`$ spotter-sort.py -r [regular] -s [spotter] [-o][dir] [-v]`

#### Example:

`$ spotter-sort.py -r timetable.arrival.regular.json -s timetable.arrival.spotter.json -o ./flighttables`

The option `-o [dir]` is used to set the output directory (not filename) of the filtered timetable.json - if there is already a timetable.[x].special.json, this file will be overwritten

The option `-v` enables verbos output for further use. You can pipe this output to a Telegram chat for example.

### Example Cronjob

```bash
#!/bin/bash
cd /home/pi/workspace/zrh
rm timetable.arrival.spotter.json
rm timetable.arrival.standard.json
rm timetable.departure.spotter.json
rm timetable.departure.standard.json
rm timetable.arrival.tom.spotter.json
rm timetable.arrival.tom.standard.json
rm timetable.departure.tom.spotter.json
rm timetable.departure.tom.standard.json

./zrh-fix-working-beta.py
./zrh-fix-2day.py

./spotter-sort.py timetable.arrival.standard.json timetable.arrival.spotter.json | awk '!x[$0]++' > temparrtod.txt
./spotter-sort-tom.py timetable.arrival.tom.standard.json timetable.arrival.tom.spotter.json | awk '!x[$0]++' > temparrtom.txt
cat temparrtod.txt temparrtom.txt > temparr.txt
./spotter-sort.py timetable.departure.standard.json timetable.departure.spotter.json | awk '!x[$0]++' > tempdeptod.txt
./spotter-sort-tom.py timetable.departure.tom.standard.json timetable.departure.tom.spotter.json | awk '!x[$0]++' > tempdeptom.txt
cat tempdeptod.txt tempdeptom.txt > tempdep.txt
```

---

## Output Format

The output format is a json file. The structure is taken from the old ZRH website API.

### Example:

```json
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
		"airportinformation": {
			"airport_city": ""
		},
		"flightcode": "",
		"masterflight": {
			"registration": ""
		}, 
		"scheduled": "", 
		"expected" : "0"
	}]
}
```

---

## Requirements

**Before you can use the `zrh-fix-working-beta.py` script you need to edit the headers.** The website requires the cookie parameters to be set. Open your browser and look inside the developer tools to find the cookie headers. Copy them into the `zrh-fix-working-beta.py` file.

If the cookie headers are not set, the script will fail with `AttributeError: 'NoneType' object has no attribute 'tbody'`.

**Dependencies**

Python 2.7

Packages used:
-   optparse
-   sys
-   os
-   datetime
-   httplib
-   urllib
-   requests
-   bs4 / BeautifulSoup
-   json

---

