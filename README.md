# ASCO site grabber

## Description
Simple data grabber application for http://iplanner.asco.org/am2017/#/ web-site.
Since this site uses Angular framework, it was pretty easy to reverse-engineer the underlying API and implement a grabber for this site. 

## Requirements
python 3

### Installation
`pip install -r requirements.txt`

## Usage

### Basics
```
$ python console.py

Usage: console.py [OPTIONS] COMMAND [ARGS]...

  ASCO Grabber command line interface

Options:
  --storage-file PATH  Where to store grabbed data, JSON file path. Default
                       value - storage.json in current directory.
  --help               Show this message and exit.

Commands:
  generate_csv       Make a CSV string from the data that is currently stored
                     in the local storage and echo it to the stdout.
  grab_data          Fill the local storage with the data from the API.
  print_stored_data  Display the data currently stored in local storage.
```

Sub-commands support the `--help` option too:
```
$ python console.py grab_data --help

Usage: console.py grab_data [OPTIONS]

Options:
  --base-api-url TEXT  Base URL of the API to grab the data from.
  --help               Show this message and exit.
```

### Typical workflow
`python console.py grab_data` pulls the data from the site and saves it in a JSON file.
`python console.py generate_csv --as-file=my.csv` generates a CSV file using this JSON file as a data source.

## Implementation details

Everything is wrapped by [Click](http://click.pocoo.org/) CLI framework.

There are separate steps for grabbing the actual data (which is then stored locally, in json file) and making a CSV file from it.
