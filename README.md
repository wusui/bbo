# bbo
Bridge Base Online Analysis

This set of python scripts scrapes data from my recent Bridgebase online tournaments, finds hands
that have scores under 50%, and analyzes the traveller results to figure out what errors I made and
computes improved scores possible

## Installation
- pip install selenium and pandas
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
- bbo_bad_hand_reviewer: Do heavy-lifting analysis of what went wrong for each hand below 50%
- bbo_report: Consolodate all of the results in bbo_evaluator into one reportk

## Execution
- Every once in a while (say once a week) run bbo_get_filenames.py followed by bbo_read_files.py
- Whenever you want to update your analysis, run bbo_analyze_game.py
- Whenever you want to produce a report, run bbo_report.py

## Evaluation of hands
Right now, this section consists of me spitballing a bunch of ideas as to how hands are evaluated.

Tournaments are named by the text name on the bbo page with underscores replacing blanks and x's replacing parentheses and '-' replacing '/' so that the text name of any file produced by this set of programs will be Posix compliant.

bbo_bad_hand_reviewer input parameters are a tournament name corresponding to a json file in the saved hands directory, and a dict containg the following fields for every hand scoring less than 50%.  For a hand scoring over 50%, this dict will only contain the raw_data field.
- raw_data: pandas dataframe containing all the sorted scores on the traveller
-  top: dataframe row for the top score on this board
-  most_pop: list of dataframe rows for scores in the top 50% that have high frequencies.  This list starts with the top score and lower entries are only added to the front of the list whenever their frequency exceeds the frequency of the top entry on thi list
-  dealer: N, E, S, W
-  vulnerability: 'None', 'N-S', 'E-W', 'Both'
-  plyr_row: the dataframe row for the player being tracked.

bbo_bad_hand_reviewer will try to track two potential values for each hand.  BPO (best possible hand) will be in most cases the top hand (exceptions may be made if it can be determined that a single anomalous bonkers result occurred which cannot be replicated). MLO (most likely outcome) will be what the code figures out will be the
most likely outcome if we tried to improve our scores (in most cases, this would be the first entry in the most_pop list if the contract is reasonably aligned with the contract that the player bid).  These values will cummulatively be tracked separately.  For any individual hand, these values are not mutually exclusive (it is quite possible for the MLO value to be the same as the BPO).

### Specific Cases
Capitalized text below are conclusions reached.
* Hand passed out [PASS OUT IS BAD]
    * MLO is BPO probably the same
    * Track Vulnerability and seat positon (especially 4th seat)
* We play hand
    * BPO and MLO are established.
    * Case 1: BPO contract and player contract are equivalent [BAD PLAY DURING HAND]
      * Track NT vs Suit contract
    * Case 2: BPO contract and player contract have same suit but BPO bid more [UNDERBID]
      * MLO is bidding level one greater than player
    * Case 3: BPO contract and player contract have the same suit but BPO bid less [OVERBID]
      * Track wrong suit combinations (NT vs maj, NT vs min, min vs maj, min vs NT, maj vs min, maj vs NT, other maj, other min)
    * Case 4: We bid but BPO defended
      * If opponent contract higher than where we played (we played for less) not much we can do (probably not likely)
        * Use better failed opponent contract under our bid if that exists -- for both MLO and BPO
      * All other cases [BAD SACRIFICE].
    * Case 5: BPO contract and player contract have different suits [WRONG SUIT CONTRACT]
      * Determine success of other players in this suit.  If bad or non-existent, definitely wrong suit
      * If decent results made by other players in this suit but with more tricks [BAD PLAY DURING HAND]
      
* We defend
  * Case 1: BPO plays [NOT COMPETITIVE ENOUGH]
    * BPO and MLO values similar to normal underbid case
    * Note that if BPO contract less than what we defended against, not much we can do.
  * Case 2: BPO defends different bid
    * Not much we can do if bid is not made / can't be made in our hand
    * Try to figure out if we could defend contract lower than us and get a better score.
  * Case 3: BPO defends same bid [BAD CARD PLAY DEFENSE]
    * Similar to how we handle hand, Case 1
  * Case 4: We miss double [MISSED DOUBLE]
    * MLO is our score with double
  * Case 5: Doubled when we should not [BAD DOUBLE]
    * MLO is our score without double

## Current Issues
My recent behavior on bbo has been to play strictly MP tournaments.  Potential bugs exist if IMP results are in the history file.
In the future, I should pla y at least one IMP tournament and test to see what changes need to be made to skip IMP tournaments.  Maybe I should
also provide an IMP version of this code.

## Other Info
- Written by Warren Usui (warrenusui@gmail.com)
- Licensed using the MIT license
