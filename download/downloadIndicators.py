import pybea
import pandas as pd
import ssl
from urllib import request
import os
import re
import glob
from os.path import basename
from zipfile import ZipFile
from download.post import post_request
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def download_commodities_data():

    ssl._create_default_https_context = ssl._create_unverified_context
    print(os.curdir)
    csv_list = 'download/commodities/commodities.txt'

    with open(csv_list, 'r') as csv_file:
        line = csv_file.readline()
        while line:
            print(line[:-3])
            r = requests.get(line[:-1])
            out_path = 'download/commodities/' + str(basename(r.url)) + '.csv'
            line = csv_file.readline()
            with open(out_path, 'wb') as outfile:
                outfile.write(r.content)
                print(out_path, str(outfile))


def get_BEA_data(path):

    USER_ID = "8766E2A1-3059-4FB9-9CCF-CE8BE40CE9A9"

    indicators = [
        'ExpGdsServIncRec', 'ImpGdsServIncPay', 'ImpGdsServ', 'SecIncPay', 'FinAssetsExclFinDeriv', 'FinLiabsExclFinDeriv', 'StatDisc', 'BalCurrAcct', 'NetLendBorrFinAcct']

    dataframes = []
    for item in indicators:
        dataframes.append(pybea.get_data(USER_ID, DataSetName='ITA', Indicator=item,
                                         AreaOrCountry='All', Frequency='QSA', ResultFormat='JSON'))

    table = pd.concat([item for item in dataframes], axis=1)

    table.to_csv(path)


def main():
    print("Downloading Indicators... ")
    l = []

    ssl._create_default_https_context = ssl._create_unverified_context

    with open('spreadsheets-data.json', 'r+') as json_file:
        json_read = json.load(json_file)

        for currency in json_read:
            index = 0
            print("--- ", currency, " ---")
            for indicator in json_read[currency]['other indicators']:

                url = json_read[currency]['other indicators'][indicator]['link']
                title = json_read[currency]['other indicators'][indicator]['title']

                title = list(json_read[currency]['other indicators'])[index]
                path = "other-indicators/%s" % (title)

                print("Downloading... ", title)

                # Download Table from indicators
                if 'api' in url:
                    post_request(
                        url, "download/query.json", path + '.csv')
                    index = index+1

                    print("File downloaded: ", title)
                    continue

                # Scrape/Download USA BOP from BEA Page
                if 'bea.gov' in url:
                    get_BEA_data(path + '.csv')
                    index = index+1

                    print("File downloaded: ", title)
                    continue

                r = requests.get(url)

                file_extension = [el for el in re.split('[.?]', str(
                    basename(r.url))) if 2 <= len(el) <= 4]
                file_type = (
                    '.' + file_extension[-1]) if len(file_extension) > 0 else ''
                print(file_type, str(basename(r.url)))
                l.append(path + file_type)  # Appending to list.

                print("File downloaded: ", title)

                if ('zip' in file_type):
                    fullfilename = os.path.join(
                        "other-indicators/", basename(r.url))
                    with open(fullfilename, 'wb') as outfile:
                        outfile.write(r.content)
                    with ZipFile(fullfilename, 'r') as zipObj:
                        zipObj.extractall(path=path,
                                          members=[item for item in zipObj.namelist() if 'MetaData' not in item])
                        print(zipObj, [
                              item for item in zipObj.namelist() if 'MetaData' not in item])
                    os.remove(fullfilename)  # remove zip file after extraction
                else:
                    full_path = path + file_type
                    for el in l:  # print out elements
                        print(el)
                    with open(full_path, 'wb') as outfile:
                        outfile.write(r.content)

                index = index+1
