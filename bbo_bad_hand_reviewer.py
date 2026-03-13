def bbo_bad_hand_reviewer(tourney, hand_data):
    for hand in hand_data:
        if len(hand.keys()) == 1:
            continue
        my_row = hand['plyr_row'].squeeze(axis=0)
        my_result = my_row['Result']
        if my_result == "P":
            import pdb; pdb.set_trace()
        else:
            pass
