# Senat-Scraping-Project
Welcome to the repository of our webscraping project, dedicated to gathering Roll-Call data from the Senat website. Below we attach instructions on how to run each out of 3 prepared by us spiders (assuming that you use Visual Studio Code):


<b>Scrapy scraper:</b> </br>
Download the entire uploaded scrapy project folder (you can put it on the desktop) Open a cmd console in Visual Studio Code. Then you will need to change a working directory to this folder containing the spider. For instance, on my desktop, I would use cd C:\Users\mj\Desktop\projects\scrapy Then you are ready to go. You will probably want to save scraped data to some CSV, if so, use a command like this: scrapy crawl senat_scraper -o filename.csv
<br><br>
<b>Beautiful Soup scraper:</b><br>
Download a file "MSsenat - BS4" placed in a "soup" folder. You don't need anything else, location is not important. Open the file in the Visual Studio and run the code section by section. The code also generates XLSX file at the end with whole output.
<br>
<br>
<b>Selenium scraper:</b><br>
Download a file "Staniaszek.py" placed in a "selenium" folder. Open the file using your IDE or command prompt. THE MOST IMPORTANT IS SETTING YOUR GECKODRIVER PATH. Change GECKO_PATH variable  according to your computer. If you use geckodriver other than Chrome change DRIVER variable acordingly to your system.  
<br>
<br>

<b>Note:</b>
Note that all scrapers have a built-in page limiter. By default, it will scrap data from just 100 pages. If you would like to scrap all data available ( that is from 500+ pages) you will have to change the value of a boolean called "limit" to False.


