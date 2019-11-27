import getLinks
import investingScrape
import download.downloadIndicators as download_indicators
import googleDrive


def main():
    drive = googleDrive.googledrive_login()
    googleDrive.download_spreadsheet_data(drive)
    getLinks.main()
    download_indicators.download_commodities_data()  # Download Commodities
    download_indicators.main()
    investingScrape.main()
    googleDrive.main(drive)


main()
