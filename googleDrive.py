import os
import json
from investingScrape import writeToJSONFile
from getLinks import upload_link_database
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client import service_account


# folder_id of /cvs in Google Drive
csv_folder_id = '16WshNWjALslELADrap9hs30NsYljQW0x'
other_indicators_folder_id = '1RiB1pPpOwkzgSINhMWd8DNFdL5MMY4de'
exogenous_file_id = '1Xq-EsVmNxrKEBLxXOFLzrKOIJmYGIgiL9hjPJyfWN30'
link_database_data = {}
other_indicators_link_database_data = {}


def main(drive):
    print("Uploading to drive... ")

    upload_other_indicators(drive)
    upload_investing(drive)


def upload_other_indicators(drive):
    print("• Uploading other indicators links...")
    # Upload other-indicators files to Google Drive
    for file in os.listdir('other-indicators'):
        if 'json' in file:
            continue

        if(os.path.isdir('other-indicators/' + file)):
            for item in os.listdir('other-indicators/' + file):
                path = 'other-indicators/%s/%s' % (file, item)
                if (os.path.isdir(path)):
                    for item1 in os.listdir(path):
                        print(file, '\n', item, '\n', item1)
                        path1 = path + '/' + item1
                        if "Icon" in path1:
                            print('This file is not valid: ', item1)
                            os.remove(path1)
                            continue
                        elif ".DS_Store" in path1:
                            print('This file is not valid: ', item1)
                            os.remove(path1)
                            continue
                        else:
                            file_title = file + ' - ' + item1
                            print("Now uploading... ", file_title)

                            check_if_in_drive(
                                drive, item1, other_indicators_folder_id)
                            upload = upload_to_google_drive(
                                drive, path1, other_indicators_folder_id, file_title)
                            f = upload

                            other_indicators_link_database_data.update(
                                {file_title: f['id']})
                            writeToJSONFile('other-indicators/', 'link-database',
                                            other_indicators_link_database_data)

                            update_spreadsheet("spreadsheets-data.json", file, file.split(' -')
                                               [0], "other indicators", file.split('.')[0], f['id'])
                            print("Uploaded: ", file, f['id'])
                else:
                    if "Icon" in item:
                        print('This file is not valid: ', item)
                        os.remove(path)
                        continue
                    file_title = file
                    print("Now uploading... ", file_title)

                    check_if_in_drive(
                        drive, item, other_indicators_folder_id)
                    upload = upload_to_google_drive(
                        drive, path, other_indicators_folder_id, file_title)
                    f = upload

                    other_indicators_link_database_data.update(
                        {file: f['id']})
                    writeToJSONFile('other-indicators/', 'link-database',
                                    other_indicators_link_database_data)

                    update_spreadsheet("spreadsheets-data.json", file, file.split(' -')
                                       [0], "other indicators", file.split('.')[0], f['id'])
                    print("Uploaded: ", file, f['id'])
        else:
            path = 'other-indicators/%s' % (file)
            print("Now uploading... ", file)

            check_if_in_drive(drive, file, other_indicators_folder_id)
            upload = upload_to_google_drive(
                drive, path, other_indicators_folder_id, file)
            f = upload

            other_indicators_link_database_data.update(
                {f['title']: f['id']})
            writeToJSONFile('other-indicators/', 'link-database',
                            other_indicators_link_database_data)

            update_spreadsheet("spreadsheets-data.json", file,
                               file.split(' -')[0], "other indicators", file.split('.')[0], f['id'])
            print("Uploaded: ", file, f['id'])

    check_if_in_drive(drive, 'link-database.json', other_indicators_folder_id)
    upload_to_google_drive(
        drive, 'other-indicators/link-database.json', other_indicators_folder_id, 'link-database.json')


def upload_investing(drive):
    print("• Uploading investing links...")

    # Upload investing files to Google Drive
    for file in os.listdir('csv'):
        if 'Icon' in file:
            continue
        elif 'DS_Store' in file:
            continue
        elif 'json' in file:
            continue

        indicator_title = file.split('.')[0]
        path = 'csv/%s' % (file)
        currency = path.split('/')[1].split(' -')[0]

        print("Now uploading... ", file)

        check_if_in_drive(drive, file, csv_folder_id, False)
        upload = upload_to_google_drive(
            drive, path, csv_folder_id, indicator_title)
        f = upload

        # store ID to JSON database
        link_database_data.update({f['title']: f['id']})
        writeToJSONFile('csv/', 'link-database',
                        link_database_data)

        update_spreadsheet("spreadsheets-data.json", file, currency,
                           'indicators-investing', indicator_title, f['id'])
        print("Uploaded: ", file, f['id'])

    check_if_in_drive(drive, 'link-database.json', csv_folder_id)
    upload_to_google_drive(
        drive, 'csv/link-database.json', csv_folder_id, 'link-database.json')


def check_if_in_drive(drive, file, folder_id, hasExtention=True):
    file_list = drive.ListFile(
        {'q': "'%s' in parents and trashed=False" % folder_id}).GetList()
    try:
        for file1 in file_list:
            if (hasExtention == False):
                file = file.split('.')[0]
            if file1['title'] == file:
                file1.Delete()
                return
    except:
        pass


def upload_to_google_drive(drive, file, folder_id, title):
    f = drive.CreateFile(
        {"parents": [{"id": folder_id}],
         "title": title})
    f.SetContentFile(file)
    if 'json' in file:
        f.Upload({'convert': False})
        if folder_id == other_indicators_folder_id:
            cell = 'H5'
        else:
            cell = 'H4'
        upload_link_database(exogenous_file_id, cell, f['id'])
    else:
        f.Upload({'convert': True})
    return f


def googledrive_login():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    return GoogleDrive(gauth)


def update_spreadsheet(json_path, file, currency, indicators_entry, indicator_title, link_id):
    with open(json_path, "r+") as json_file:
        json_temp = json.load(json_file)
        if("Store" in file or "Icon" in file or "zip" in file):
            return
        else:
            currency = file.split(' -')[0]
            print(currency, indicators_entry,
                  indicator_title, 'link_id', link_id)
            json_temp[currency][indicators_entry][indicator_title]['link_id'] = link_id
            json_file.seek(0)
            json.dump(json_temp, json_file, indent=4,
                      sort_keys=True, separators=(',', ': '))
            json_file.truncate()


def download_spreadsheet_data(drive):
    spreadsheets_list = drive.ListFile(
        {'q': "'1xyegMN8XxfAy0tOxYFk4iFKaQTuwO_qf' in parents and trashed=false"}).GetList()
    for spreadsheet in spreadsheets_list:
        if ('Financial Analysis' in spreadsheet['title']):
            with open('spreadsheets-data.json', 'r+') as spreadsheets_json:
                json_file = json.load(spreadsheets_json)
                json_file[spreadsheet['title'].split(' ')[0]] = {
                    'link_id': spreadsheet['id'], 'indicators-investing': {}, 'other indicators': {}}
                writeToJSONFile('./', 'spreadsheets-data', json_file)
                spreadsheets_json.seek(0)
                json.dump(json_file, spreadsheets_json, indent=4,
                          sort_keys=True, separators=(',', ': '))
                spreadsheets_json.truncate()
