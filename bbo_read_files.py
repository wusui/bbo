# Copyright (C) 2026 Warren Usui, MIT License
"""
Create files in saved_hands directory
"""
import os.path
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd

def mk_driver():
    """
    Make an invisible driver
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def bbo_read_first(filename):
    """
    Get list of travellers
    """
    with open(f"saved_records/{filename}", 'r', encoding='utf-8') as ifd:
        ofilename = ifd.read().strip()
    driver = mk_driver()
    driver.get(ofilename)
    WebDriverWait(driver, 10)
    trows = driver.find_elements(By.TAG_NAME, 'tr')
    travellers = []
    for line in enumerate(trows):
        if line[0] == 0:
            continue
        linkv = line[1].find_elements(By.TAG_NAME, 'a')
        travellers.append(linkv[-1].get_attribute('href'))
    driver.quit()
    return travellers

def bbo_traveller(hand):
    """
    Save scoring data for one hand
    """
    driver = mk_driver()
    driver.get(hand)
    WebDriverWait(driver, 10)
    table = driver.find_element(By.TAG_NAME, 'table')
    tdata = table.get_attribute('outerHTML')
    data_frames = pd.read_html(tdata)
    bbo_df = data_frames[0]
    csv_str = bbo_df.to_csv()
    driver.quit()
    return csv_str

def bbo_save_trav_data(tourney):
    """
    Save all the scoring data
    """
    outfile = f"saved_hands/{tourney}.json"
    if os.path.isfile(outfile):
        return
    travellers = bbo_read_first(tourney)
    hlist = []
    for hand in travellers:
        hlist.append(bbo_traveller(hand))
    with open(outfile, 'w', encoding='utf-8') as json_file:
        json.dump(hlist, json_file, indent=4)

def bbo_mk_hand_recs():
    """
    Get hand records for each tournament
    """
    for tname in os.listdir('saved_records'):
        bbo_save_trav_data(tname)

if __name__ == "__main__":
    bbo_mk_hand_recs()
