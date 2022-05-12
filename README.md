# Senat-Scraping-Project
Welcome to repository of our webscraping project, dedicated to gathering Roll-Call data from Senat website.
Below we attach instructions on how to run each out of 3 prepared by us spiders (assuming that you use Visual Studio Code):

Selenium scraper:


Scrapy scraper:
Download entire uploaded project folder (you can put it on desktop)
Open cmd console in Visual Studio Code. Then you will need to change working directory to this folder containing spider.
For instance, on my desktop I would use
cd C:\Users\mj\Desktop\projects\scrapy
Then you are ready to go. You will probably want to save scraped data to some csv, if so, use command like this:
scrapy crawl senat_scraper -o filename.csv


Beatiful soup scraper:




Note that all scrapers have built-in page limiter. By default, it will scrap data from just 100 pages. If you would like to scrap all data available ( that is from 500+ pages) you will have to change value of boolean called "limit" to False.
