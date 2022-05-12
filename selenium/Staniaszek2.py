###### STANIASZEK ######
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
    driver.get(page)
    driver.implicitly_wait(1)
    karty = driver.find_elements(By.CSS_SELECTOR,("a[href*='glosowanie-drukuj']"))
    
    ##### Saving links to lists and delete duplicates
    for element in karty:
        href2 = element.get_attribute("href")
        if href2 is not None:
            if href2 not in glosowanie1:
                glosowanie1.append(href2)

while Limit == True:
    limit = 0
    for link in glosowanie1:
        if limit == 100:
            break
        driver.get(link)
        driver.implicitly_wait(3)
        
        senators = driver.find_elements(By.CSS_SELECTOR, ".col-sm-4")  ### NAZWISKA SENATOROW
        glosy = driver.find_elements(By.CSS_SELECTOR, ".col-sm-2")       #### GLOS 
        tytul = driver.find_element(By.CSS_SELECTOR, ".tytul")          #### NAZWA GLOSOWANIA 
        for i in range(len(senators)):
            nazwisko.append(senators[i].text)
            try:
                glos.append(glosy[i].text)
            except:
                glos.append("brak")
            ustawa.append(link)
        limit += 1 


    df = pd.DataFrame(list(zip(nazwisko, glos,ustawa)),
                columns =['Surname', 'Vote', 'Link'])
    df.to_csv('tabela.csv', sep=';')



while Limit == False:
    for link in glosowanie1:
        driver.get(link)
        driver.implicitly_wait(3)

        senators = driver.find_elements(By.CSS_SELECTOR, ".col-sm-4")  ### NAZWISKA SENATOROW
        glosy = driver.find_elements(By.CSS_SELECTOR, ".col-sm-2")       #### GLOS 
        tytul = driver.find_element(By.CSS_SELECTOR, ".tytul")          #### NAZWA GLOSOWANIA 
        for i in range(len(senators)):
            nazwisko.append(senators[i].text)
            try:
                glos.append(glosy[i].text)
            except:
                glos.append("brak")
            ustawa.append(link)


    df = pd.DataFrame(list(zip(nazwisko, glos,ustawa)),
                columns =['Surname', 'Vote', 'Link'])
    df.to_csv('tabela.csv', sep=';')














        
        
        
        
        
        
        
        
    
    















