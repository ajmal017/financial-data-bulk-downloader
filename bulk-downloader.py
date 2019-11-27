import getLinks
import investingScrape
import download.downloadIndicators as download_indicators
import googleDrive

# This is where the brain of the application is. This main function is directing
# all of the functions and processes needed for the app to work.
# In order:
# 1. Connect to google drive.
# 2. Download spreadsheets data.
# 3. Get download links data from specific cells and gather in json file.
# 4. Download indicators.
# 5. Web scrape linkes from Investing.com and store to csv.
# 6. Write new collected data to spreadsheets and finalize.


def main():
    drive = googleDrive.googledrive_login()
    googleDrive.download_spreadsheet_data(drive)
    getLinks.main()
    download_indicators.download_commodities_data()  # Download Commodities
    download_indicators.main()
    investingScrape.main()
    googleDrive.main(drive)


main()
