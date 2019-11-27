# financial-data-bulk-downloader
Automatic downloader for financial data files (BOP, Trades data) taken from various sources including UN Comtrade, US BEA, Bank Of Switzerland and more.

! Bear in mind, this project is currently under construction ! 
Most of financial data sources used are major (and reliable!) government APIs and either Quandl.com or db.nomics. Other sources include the use of web-scraping from Investing.com.

- https://www.quandl.com/
- https://db.nomics.world/

I was looking around for a way to integrate financial data around one sole app. Looking around, I found different ways to go do so, but most required a heavy monthly investmnent that usually is done by larger financial companies, like investment funds or banks. Also, most of the choices lack in data sources and grab one piece against the other. In trading the financial markets, the most important monitoring factors include country specific trade data together with major inflation and price indicators. Knowing the scope and direction of financial markets give the trader a broader understanding of direction and trend. That is when I decided to build my own web app. This way, me and other potential retail traders would be able to monitor recent economic activity and work around data published by accredited and official Governemt APIs in order to structure a better solution.

Again, bear in mind this is now still under development. Bulk-downloader is built by using Google Sheets functioning both as web server and as a tool to display data on a graph - in a excel type of way. I am currently working my way trough a Django based application, using Pandas, Matplotlib and Seaborn to visualise data corrently, with soon the possibility of running a correlation based analysis, comparing graphs and more.

At the moment, the app is running fine and original files are stored in a Google Drive folder. You can download all the files and potentially replace links in the code with your own spreadsheet files. The way it works is by running the buld-downloader.py file trough bash command. Just navigate to the root folder and type in on your terminal: # python3 bulk-downloader.py #

