# Copyright (C) 2026 Warren Usui, MIT License
"""
BBO hand analysis
"""
import json
import io
import pandas as pd
from bbo_bad_hand_reviewer import bbo_bad_hand_reviewer

def under_avg(a_row):
    """
    Return true is Score is less than 50%
    """
    return int(a_row['Score'].values[0].split('.')[0]) < 50

def get_tops(hand_df, iam):
    """
    Get top results for a hand. Returns a dict with the following keys:
        top -- Top board
        most_pop -- list of results that beat iam.  Sorted by Frequency. Lower
                    scores are only added if their Frequency is greater than
                    the top previous Frequency value.
    """
    ret_val =  {}
    for presult in range(len(hand_df)):
        if int(hand_df.iloc[presult]['Score'].split('.')[0]) < 50:
            break
        if presult == 0:
            ret_val['top'] = hand_df.iloc[presult]
            ret_val['most_pop'] = [hand_df.iloc[presult]]
        else:
            if hand_df.iloc[presult]['Frequency'] > ret_val[
                        'most_pop'][0]['Frequency']:
                ret_val['most_pop'].insert(0, hand_df.iloc[presult])
    return ret_val

def bbo_analyze_hand(hand_info):
    """
    Do analysis of the hand specified
    """
    def vulnerability(number):
        basen = number % 4
        offset = number // 4 
        return (basen + offset) % 4
    string_io_object = io.StringIO(hand_info[1])
    hand_df = pd.read_csv(string_io_object)
    hand_df['Score'] = hand_df['Score'].astype(str)
    hand_df['Frequency'] = hand_df['Frequency'].astype(int)
    iam = list(filter(lambda a: isinstance(a, str), hand_df['Your Result']))
    myrow = hand_df[hand_df['Your Result'] == iam[0]]
    if under_avg(myrow):
        edata = get_tops(hand_df, iam[0])
        edata['dealer'] = "NESW"[hand_info[0] % 4]
        edata['vulnerability'] = ['None', 'N-S', 'E-W', 'Both'][
                                    vulnerability(hand_info[0])]
        edata['plyr_row'] = myrow
        edata['raw_data'] = hand_df
        return edata
    return {'raw_data': hand_df}

def bbo_analyze_game(json_input):
    """
    Open hand record, pass each hand to bbo_analyze_hand
    """
    with open('/'.join(['saved_hands', json_input]), 'r',
                            encoding='utf-8') as in_file:
        hands = json.load(in_file)
        results = list(map(bbo_analyze_hand, enumerate(hands)))
        bbo_bad_hand_reviewer(json_input.split('.')[0], results)

if __name__ == "__main__":
    #bbo_analyze_game('ACBL_Daylong_with_GIBBO_xMPx_1_-_Mar_02.json')
    bbo_analyze_game('ACBL_Daylong_with_GIBBO_xMPx_1_-_Feb_11.json')
