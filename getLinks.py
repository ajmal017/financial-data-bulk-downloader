import ssl
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

CREDENTIALS = []


def create_credentials():
    ssl._create_default_https_context = ssl._create_unverified_context

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
              'https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive.readonly',
              'https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive'
              ]

    # gspread connect to Google API
    CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
        'update-macro-indicators-3a86604dce58.json', SCOPES)

    return CREDENTIALS


def main():
    print("Getting links from spreadsheets... ")
    # gspread connect to Google API
    CREDENTIALS = create_credentials()

    client = gspread.authorize(CREDENTIALS)

    # write to JSON file
    with open("spreadsheets-data.json", "r+") as spreadsheets_json:
        spreadsheets = json.load(spreadsheets_json)
        index = 0
        for currency in spreadsheets:
            ws = client.open_by_key(
                spreadsheets[currency]['link_id']).worksheet('SOURCES')

            column_links = [item for item in ws.col_values(12)][2:]

            if (len(column_links) > 0):
                i = 3
                for link in column_links:
                    if ('investing' not in link and link != ''):
                        print(link)
                        indicator_title = str(
                            list(spreadsheets)[index] + ' - ' + ws.cell(i, 4).value)
                        spreadsheets[currency]['other indicators'].update({
                            indicator_title: {'link': link, 'row': i, 'title': indicator_title}})
                    elif ('investing' in link and link != ''):
                        print(link)
                        indicator_title = str(
                            list(spreadsheets)[index] + ' - ' + ws.cell(i, 4).value)
                        spreadsheets[currency]['indicators-investing'].update({
                            indicator_title: {'link': link, 'row': i, 'title': indicator_title}})

                    i = i+1
            index = index+1

        spreadsheets_json.seek(0)
        json.dump(spreadsheets, spreadsheets_json, indent=4,
                  sort_keys=True, separators=(',', ': '))
        spreadsheets_json.truncate()


def upload_link_database(file_id, cell, link):
    CREDENTIALS = create_credentials()  # to delete when working
    client = gspread.authorize(CREDENTIALS)
    ws = client.open_by_key(
        file_id).worksheet('SOURCES')
    ws.update_acell(cell, link)
    print("Updated Cell %s with link-database id: %s" % (cell, link))
