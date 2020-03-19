# Pick a Random To Do from your Remember the Milk list(s)

Do you have way too many things to do and don't know where to start? Use this script to randomly pick an item from your RTM account!

## Prerequisites

* Python 2.7.x
* Python modules:
	* rtmapi
	* httplib2
	* colorama

## Installing

Clone this repo to your local computer.

## Usage

Run `rtmr.py`. e.g.:

```./rtmr.py```

or perhaps:

```python2.7 rtmr.py```

### Options

* `-l` / `--list` - specify an RTM list to search within. Note that if your list has spaces in it, you must quote it. i.e. "Home Tasks" or 'Grocery List'
* `-t` / `--tag` - specify an RTM tag to search within or add to your search filter. 
* `-p` / `--priority` - specify an RTM priority to search within or add to your search filter. 

### Examples

Find a random task in _all_ of your RTM tasks:

`./rtmr.py`

Find a random task in your _Home Stuff_ list:

`./rtmr.py -l 'House Stuff'`

Find a random task in your _financial_ list:

`./rtmr.py -t financial`

Find a random task in your _Home Stuff_ list that is also tagged with the _financial_ tag:

`./rtmr.py -l 'House Stuff' -t financial`

Find all priority 1 tasks that are tagged as _financial_:

`./rtmr.py -p 1 -t financial`

*Note* that specifying multiple search filter flags `AND`s them together (not `OR`).

## Contributing

Please add your suggestions, bugs you've found or send us pull requests via this GitHub repo!

## Authors

* **Khalid J Hosein**

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0)  - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This utility uses the [Remember The Milk API](https://www.rememberthemilk.com/services/api/) but is not endorsed or certified by Remember The Milk.
