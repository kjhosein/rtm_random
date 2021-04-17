# Pick a Random To Do from your Remember the Milk list(s)

Do you have way too many things to do and don't know where to start? Use this script to randomly pick an item from your RTM account!

## Prerequisites

* Python 2.7.x - primarily due to the RtmAPI module being built with this version.
* Python modules (`pip install` these):
	* rtmapi
	* httplib2
	* colorama
	* progress

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

## Bonus Script - Randomize a List of Ordered Numbers, 1 to N.

Many days, I have To Dos that crop up outside of what's in RTM. I tend to write these down. To fight the overwhelm, I number the items, then randomize the list using the `shuffle.py` script. 

For example, if I have 4 items (1, 2, 3, 4 ), after shuffling the list, it may become [3, 1, 4, 2].

## Contributing

Please add your suggestions, bugs you've found or send us pull requests via this GitHub repo!

The point of this tool is to make your life a little bit more manageable by removing one more decision - what to do/where to start? So that means it should *not* make it more complicated by having/adding so many features that you need to do/learn 1 more thing! As much as I like powerful software, I've fought the urge to add every single feature that has occurred to me. 

## Authors

* **Khalid J Hosein**

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0)  - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This utility uses the [Remember The Milk API](https://www.rememberthemilk.com/services/api/) but is not endorsed or certified by Remember The Milk.
