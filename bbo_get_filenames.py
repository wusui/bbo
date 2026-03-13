# Copyright (C) 2026 Warren Usui, MIT License
"""
Create files in saved_records directory
"""
import os
import configparser
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

def bbo_login():
    """
    Login and return driver on starting web page
    """
    config = configparser.ConfigParser()
    config.read('local.ini')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.bridgebase.com/v3/auth/login")
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.element_to_be_clickable((By.ID,
                                                    "username")))
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CLASS_NAME,
                                       "old-bbo-phx-btn-primary")
    username_field.send_keys(config['private']['user'])
    password_field.send_keys(config['private']['pass'])
    login_button.click()
    return driver

def posixize_text(itext):
    """
    Make sure returned text used for filenames is posix compliant
    """
    itext1 = itext.replace(' ', '_')
    itext2 = itext1.replace('(', 'x')
    itext3 = itext2.replace(')', 'x')
    itext4 = itext3.replace('/', '-')
    return itext4

def bbo_save_info(result_file, rdiv):
    """
    Catalog results_file html link
    """
    print(f'analyze {result_file}')
    maindiv = rdiv.find_element(By.ID, 'mainDiv')
    mdata = maindiv.find_elements(By.TAG_NAME, 'title-bar')
    fname = posixize_text(mdata[-1].text)
    print(fname)
    if fname in os.listdir('saved_records'):
        return f"Filename {fname} already saved"
    with open(f"saved_records/{fname}", 'w', encoding='utf-8') as ofd:
        ofd.write(result_file)
    return result_file

def bbo_find_one_value(rdiv, driver):
    """
    Find an individual tournament result
    """
    buttons = rdiv.find_elements(By.TAG_NAME, 'button')
    results_b = list(filter(lambda a: a.text == 'Results:', buttons))
    if not results_b:
        return "No results found for this entry"
    o_iframes_list = driver.find_elements(By.TAG_NAME, "iframe")
    results_b[0].click()
    sleep(5)
    iframes_list = driver.find_elements(By.TAG_NAME, "iframe")
    ofo = list(filter(lambda a: a not in o_iframes_list, iframes_list))
    ret_v  = 'No new tournament record found'
    if len(ofo) > 0:
        wait = WebDriverWait(driver, 30)
        wait.until(EC.frame_to_be_available_and_switch_to_it(ofo[0]))
        showb = driver.find_element(By.TAG_NAME, 'a')
        ret_i = showb.get_attribute('href')
        driver.switch_to.default_content()
        ret_v = bbo_save_info(ret_i, rdiv)
    return ret_v

def bbo_get_record(count):
    """
    Follow links to get a tournament record
    """
    driver = bbo_login()
    wait = WebDriverWait(driver, 10)
    rdiv = wait.until(EC.element_to_be_clickable((By.ID,
                                                  "rightDiv")))
    ftabs = rdiv.find_elements(By.CLASS_NAME, "area-label")
    if len(ftabs) < 3:
        return "History tab not available"
    ftabs[2].click()
    sleep(1)
    rectangles = rdiv.find_elements(By.TAG_NAME, "celled-rectangle")
    actions = ActionChains(driver)
    sleep(1)
    zcount = count + 2
    if zcount > len(rectangles):
        return "All tournament records have been found"
    tclk = actions.move_to_element_with_offset(rectangles[zcount], 1, 1)
    tclk.click()
    tclk.perform()
    sleep(1)
    ret_v = bbo_find_one_value(rdiv, driver)
    driver.quit()
    return ret_v

def get_all_we_can():
    """
    Loop through possible tournaments
    """
    ret_list = []
    for tournumb in range(1, 101):
        bbo_rec = bbo_get_record(tournumb)
        if bbo_rec.endswith('already saved'):
            break
        if bbo_rec.startswith('http'):
            ret_list.append(bbo_rec)
            continue
        break
    return ret_list

if __name__ == "__main__":
    get_all_we_can()
