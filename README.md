# bbo
Bridge Base Online Analysis

This set of python scripts scrapes data from my recent Bridgebase online tournaments, finds hands
that have scores under 50%, and analyzes the traveller results to figure out what errors I made and
computes improved scores possible

## Installation
- Download the python files in this repo to a directory/folder of your choice
- Set PYTHONPATH to include this directory/folder
- cd to this directory
- mkdir saved_records, saved_hands, saved_analysis
- create a file named local.ini containing the following fields:
```
user = <my bbo username>
pass = <my bbo password>
http = https://www.bridgebase.com/v3
```

## Scripts
- bbo_get_filenames.py: Scrapes your recent bbo history for MP tournament results. Saves the results for each tournament in a unique file in saved_records
- bbo_read_files.py: For each new file added to saved_records, extract the data for each board in that tournament and save the extracted information for that traveller in saved_hands as a correspondingly named json file consisting of a list of csv records.
- bbo_analyze_game.py: For each file in saved_hands, parse the contents and pass that information to bbo_evaluator.  Save the evaluated code as a text file in saved_analysis
- bbo_evaluator: Do heavy-lifting analysis of what went wrong for each hand below 50%
- bbo_report: Consolodate all of the results in bbo_evaluator into one reportk

## Execution
- Every once in a while (say once a week) run bbo_get_filenames.py followed by bbo_read_files.py
- Whenever you want to update your analysis, run bbo_analyze_game.py
- Whenever you want to produce a report, run bbo_report.py

## Evaluation of hands
Right now, this section consists of me spitballing a bunch of ideas as to how hands are evaluated.

## Other Info

- Written by Warren Usui (warrenusui@gmail.com)
- Licensed using the MIT license
