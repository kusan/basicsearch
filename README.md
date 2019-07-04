# basicsearch

This program will should run on either windows OR linux, but has been tested only to work on linux. 


## Requirements

 - [ ] Python 2.4 + (Only Python 2 supported due to the use of raw_input function on Console.py.
 - [ ] simplejson module for python must be installed by running "pip install simplejson" on the command prompt before starting application.
 - [ ] if you are running the application with very large json files then please install the c library for simplejson as well.

## Methodology

The application implements a dictionary of dictionaries in order to provide O(1) time data retrival. This means that there will be an initial indexing process where by data is converted from the format on Json (i.e list of dictionaries) into a Dictionary of Dictionaries. The indexing process is a O(n) time opertaion. At the moment the application does not serialize the root dictionary to disk but instead re-indexes from source at startup, before showing the menu. 

## Running Application

After cloning from github, navigate to the directory and run

python Console.py

Run tests with

python DataIndexerTestCase.py
