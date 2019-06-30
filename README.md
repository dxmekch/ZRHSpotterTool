
# ZRHSpotterTool

---
(formerly: mnemocron/ZRHMovementsSpottertool)

> This Python script can fetch the full arrival / departure list of the Zürich airport (ZRH). The output format is 'json'. There are multiple lists available. Both the arrivals and depatrures of regular civil flights, as well as both the arrivals and departures of all available flights (including private and freight flights). Typically a regular list contains ~400 flights per day, while a spotter list contains ~450 flights.

Furthermore there is a `dict.json` that contains further information for given registration numbers. The dict.json also overrides the sorting of special flights.

### [dxmek.ch/zrharr](https://dxmek.ch/zrharr/)

currently work in progress: refactoring and porting to Python 3

---

## Usage

### Download Timetables

`python3 get-zrh.py` downloads all available tables

`python3 get-zrh.py --today --arrivals` only fetch arrivals of today

`python3 get-zrh.py --tomorrow --departures` only fetch departures of tomorrow

Set the output directory to a place other than `./timetables`

`python3 get-zrh.py -d ./folder`

### Filter the special flights

```bash
python3 sort-flights.py -a timetables/timetable.arrival.standard.json -b timetables/timetable.arrival.spotter.json -o timetables/timetable.arrival.special.json
```

```bash
python3 sort-flights.py -a timetables/timetable.departure.standard.json -b timetables/timetable.departure.spotter.json -o timetables/timetable.departure.special.json
```

### Pretty Print a table

`python3 print-table.py -i timetables/timetable.arrival.special.json -t "Zurich Airport ZRH - Arrivals (special)"`


### Example Cronjob

Todo

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

If the cookie headers are not set, the script will fail with `AttributeError: 'NoneType' object has no attribute 'tbody'`.

**Dependencies**

Python 3

```bash
sudo apt install python3-bs4
```


---

