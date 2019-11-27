import pprint as pp
import csv
import json
import time
from urllib import request
import requests
import glob
import os
from os.path import basename
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


login_investing = False


def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp, indent=4,
                  sort_keys=True, separators=(',', ': '))


def create_row(browser_element):
    l = [item.text for item in browser_element]
    if (len(l) > 6):
        l = [l[i:i + 6] for i in range(0, len(l), 6)]
    return l


def main():
    print("...Scraping from investing.com... ")

    # example option: add 'incognito' command line arg to options
    option = webdriver.ChromeOptions()
    preferences = {"download.default_directory": os.path.dirname(os.path.abspath(__file__)) + '/csv/',
                   "directory_upgrade": True,
                   "safebrowsing.enabled": True,
                   "user-data-dir": "Users/luca/Library/Application Support/Google/Chrome"}
    option.add_experimental_option("prefs", preferences)
    option.add_argument("--incognito")
    option.add_argument("--start-maximized")

    # create new instance of chrome in incognito mode
    browser = webdriver.Chrome(
        '/Library/Application Support/Google/chromedriver/chromedriver', options=option)

    login_investing = False
    investing_scrape(browser)


def historical_data(link, browser, path):
    print('Downloading from historical data...')

    data_interval = browser.find_elements_by_xpath(
        "//select[@id='data_interval']")[0]
    widget_field = browser.find_elements_by_xpath(
        "//div[@id='widgetFieldDateRange']")[0]
    cookie_bar = browser.find_elements_by_xpath(
        "//span[@class='closer']")

    if (len(cookie_bar) > 0 and cookie_bar[0].is_displayed()):
        cookie_bar[0].click()

    actions = ActionChains(browser)
    actions.move_to_element_with_offset(
        data_interval, 0, -200).perform()
    data_interval.click()
    time.sleep(1)
    data_interval.send_keys("m")
    data_interval.send_keys(u'\ue007')
    time.sleep(1)
    widget_field.click()
    start_date = browser.find_elements_by_xpath(
        "//div[@id='ui-datepicker-div']//input[@class='newInput']")[0]
    start_date.clear()
    start_date.send_keys("01/01/1985")
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='ui-datepicker-div']//a[@id='applyBtn']")))
    apply_button = browser.find_elements_by_xpath(
        "//div[@id='ui-datepicker-div']//a[@id='applyBtn']")[0]
    apply_button.send_keys(u'\ue007')
    time.sleep(1)
    download_data = browser.find_elements_by_xpath(
        "//a[@title='Download Data']")[0]
    download_data.send_keys(u'\ue007')

    print("Historical data has been downloaded: ", path.split('/')[1])

    return


def investing_scrape(browser):

    with open('spreadsheets-data.json', "r") as read_file:
        json_data = json.load(read_file)

        for currency in json_data:

            print("---", currency, "---")
            index = 0
            for link in json_data[currency]['indicators-investing']:

                link_address = json_data[currency]['indicators-investing'][link]['link']
                link_name = list(
                    json_data[currency]['indicators-investing'])[index]
                csv_path = 'csv/' + link_name + '.csv'
                index += 1
                print(link_address, csv_path)

                browser.get(link_address)

                global login_investing
                if login_investing == False:
                    login_button = browser.find_elements_by_xpath(
                        "//a[@class='login bold']")[0]
                    login_button.click()
                    email_login = browser.find_elements_by_xpath(
                        "//input[@id='loginFormUser_email']")[0]
                    password_login = browser.find_elements_by_xpath(
                        "//input[@id='loginForm_password']")[0]
                    email_login.send_keys("somigliluca@gmail.com")
                    password_login.send_keys("Cliveden93")
                    password_login.send_keys(u'\ue007')
                    login_investing = True

                # Historical data download
                if 'historical-data' in link_address:
                    historical_data(link_address, browser,
                                    csv_path)
                    time.sleep(5)
                    latest_file = max(
                        glob.glob('csv/*.csv'), key=os.path.getctime)
                    os.rename(latest_file, csv_path)
                    continue
                else:
                    # Investing scrolling links
                    print('...Scraping from table...')

                    # click radio button
                    button_element = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//div[@class="showMoreReplies block"]')))
                    button = browser.find_elements_by_xpath(
                        "//div[@class='showMoreReplies block']")[0]

                    while (button.is_displayed()):
                        cookie_bar = browser.find_elements_by_xpath(
                            "//span[@class='closer']")
                        pop_up = browser.find_elements_by_xpath(
                            "//div[@id='PromoteSignUpPopUp']")

                        try:
                            if (len(cookie_bar) > 0 and cookie_bar[0].is_displayed()):
                                cookie_bar[0].click()
                            if(len(browser.window_handles) > 1):
                                browser.switch_to.window(
                                    browser.window_handles[-1])
                                browser.close()
                                browser.switch_to.window(
                                    browser.window_handles[0])
                            if (len(pop_up) > 0 and pop_up[0].is_displayed()):
                                pop_up[0].click()

                            actions = ActionChains(browser)
                            actions.move_to_element_with_offset(
                                button, 0, -200).perform()
                            button.click()
                            time.sleep(1)
                        except ValueError as e:
                            ValueError(e)

                    # find table data
                    th = browser.find_elements_by_xpath(
                        "//table[@class='genTbl openTbl ecHistoryTbl']//th")
                    tr = browser.find_elements_by_xpath(
                        "//table[@class='genTbl openTbl ecHistoryTbl']//td")

                    # Create csv file
                    with open(csv_path, 'w') as csvFile:
                        h = create_row(th)
                        r = create_row(tr)

                        header = csv.DictWriter(csvFile, h)
                        header.writeheader()
                        writer = csv.writer(csvFile)
                        for item in r:
                            writer.writerow(item)
                        csvFile.close()
                    print("Link has been scraped: ", link_name)

    browser.quit()
