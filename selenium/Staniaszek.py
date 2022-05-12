###### Scraper made by MICHAŁ STANIASZEK ######

# Libraries declaring 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import getpass
import datetime
import pandas as pd 
import csv

#GeckoDriver path and setting google chrome browser (INIT)
gecko_path = 'C:/Users/micha/Desktop/Selenium/chromedriver.exe'
ser = Service(gecko_path)
driver = webdriver.Chrome(service=ser) 

#Declaring Boolean parameter limiting number of pages 
Limit = True 

# List declaring 
linki1 = []
linki2 = []
glosowanie1 =[]
nazwisko = []
glos = []
ustawa = []

#URL TO GOVERMENT SITE 
url = 'https://www.senat.gov.pl/prace/posiedzenia/tematy-posiedzen-senatu-ix-kadencji/'

#ACTUAL PROGRAM:

#GOVERMENT SITE OPEN  
driver.get(url)

#Command forcing a wait of up to 5 seconds before an object appears
driver.implicitly_wait(5)

#Gathering links for all deliberations held 
linki_do_spotkan = driver.find_elements(By.CSS_SELECTOR,("a[href*='/prace/posiedzenia/tematy,']"))

#Saving links to lists and delete duplicates
for element in linki_do_spotkan:
    href1 = element.get_attribute("href")
    href1 = href1.replace('https','http')
    if href1 is not None:
        if href1 not in linki1:
           linki1.append(href1)

#Changing URL to site with PDF links 
for element in linki1:
    element = element.replace('tematy','przebieg')
    element = element.replace(',1',',1,glosowania')
    linki2.append(element)


#### Gathering links with voting results
for page in linki2:
    # All pages from link list are open and direct link to voting tables is scraped  
    driver.get(page)
    driver.implicitly_wait(1) # time for object to appear 
    karty = driver.find_elements(By.CSS_SELECTOR,("a[href*='glosowanie-drukuj']")) #link to voting 
    
    ##### Saving links to lists and delete duplicates
    for element in karty:
        href2 = element.get_attribute("href")
        if href2 is not None:
            if href2 not in glosowanie1:
                glosowanie1.append(href2)
                
#### Part of the program for boolean variable = True meaning  program is cut after 100 pages 
while Limit == True:
    ### Limitation counter 
    limit = 0
    for link in glosowanie1:
        if limit == 100: # After scraping 100 tables exit the loop  
            break
        
        #Opening pages with table 
        driver.get(link)
        driver.implicitly_wait(3)

        ### Finding senator's surname and their vote bu CSS_SELECTOR by class distinction 
        senators = driver.find_elements(By.CSS_SELECTOR, ".col-sm-4")  #senator's surname 
        glosy = driver.find_elements(By.CSS_SELECTOR, ".col-sm-2")    #senator's vote 

       ### Creating list
        for i in range(len(senators)):
            nazwisko.append(senators[i].text)
            try:
                glos.append(glosy[i].text)
            except:
                glos.append(" ")
            ustawa.append(link)
        limit += 1 

    #### Lists are convert into one pandas table object inluding senators' surnames and votes 
    ###  as well as link to vote.Everyting is save into csv file called "Tabel.csv" separated by semicolon
    df = pd.DataFrame(list(zip(nazwisko, glos,ustawa)),
                columns =['Surname', 'Vote', 'Link'])
    df.to_csv('Tabel.csv', sep=';')


#### Part of the program for boolean variable = False meaning  program scrap on over 500 pages 
while Limit == False:

    #Opening pages with table
    driver.get(link)
    driver.implicitly_wait(3)

    ### Finding senator's surname and their vote bu CSS_SELECTOR by class distinction 
    senators = driver.find_elements(By.CSS_SELECTOR, ".col-sm-4")  #senator's surname 
    glosy = driver.find_elements(By.CSS_SELECTOR, ".col-sm-2")    #senator's vote 

    ### Creating list
    for i in range(len(senators)):
        nazwisko.append(senators[i].text)
        try:
            glos.append(glosy[i].text)
        except:
            glos.append(" ")
        ustawa.append(link)
    

#### Lists are convert into one pandas table object inluding senators' surnames and votes 
###  as well as link to vote.Everyting is save into csv file called "Tabel.csv" separated by semicolon
    df = pd.DataFrame(list(zip(nazwisko, glos,ustawa)),
                columns =['Surname', 'Vote', 'Link'])
    df.to_csv('Tabel.csv', sep=';')













        
        
        
        
        
        
        
        
    
    















