# Senat-Scraping-Project
Welcome to the repository of our webscraping project, dedicated to gathering Roll-Call data from the Senat website. Below we attach instructions on how to run each out of 3 prepared by us spiders (assuming that you use Visual Studio Code):

<b>Selenium scraper:</b> <br>

<br>
<br>
<b>Scrapy scraper:</b> </br>
Download the entire uploaded Senat project folder (you can put it on the desktop) Open a cmd console in Visual Studio Code. Then you will need to change a working directory to this folder containing the spider. For instance, on my desktop, I would use cd C:\Users\mj\Desktop\projects\scrapy Then you are ready to go. You will probably want to save scraped data to some CSV, if so, use a command like this: scrapy crawl senat_scraper -o filename.csv
<br><br>
<b>Beautiful Soup scraper:</b><br>
Download a file "MSsenat - BS4" placed in a "BeautifulSoup" folder. You don't need anything else, location is not important. Open the file in the Visual Studio and run the code section by section. It will scrap the data from all pages (500+). If you would like to scrap the data only from 100 pages, change the value of a "limit" boolean to 1. The code also generates XLSX file at the end with whole output.
<br>
<br>
Note that Scrapy and Selenium scrapers have a built-in page limiter. By default, it will scrap data from just 100 pages. If you would like to scrap all data available ( that is from 500+ pages) you will have to change the value of a boolean called "limit" to False.
