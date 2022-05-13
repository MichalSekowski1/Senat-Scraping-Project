####################### LIBRARIES #######################################

from dataclasses import replace
from operator import contains
from pickle import FALSE, TRUE
import re
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


########################## LIMIT #######################################

#                      False - LIMIT OFF
#                      True - LIMIT ON
limit = True

###################### LINKS PART 1 ####################################

if limit == 1:
    Limit = 100 
   
# The "start" page. On this page we can find all links that will be useful for our analysis. 
# This code scraps all available links on this page. To do that, it uses "links" to save https links and "links2" to scrap http links.

url= 'https://www.senat.gov.pl/prace/posiedzenia/tematy-posiedzen-senatu-ix-kadencji'
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(url,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page)
links = soup.find_all('a', attrs={'href': re.compile("^https?://")})
links2 = soup.find_all('a', attrs={'href': re.compile("^http://")})

linksA = []
for link in links:
    linksA.append(link.get('href'))
    print(link.get('href'))

for link in links2:
    linksA.append(link.get('href'))
    print(link.get('href'))

print(linksA)

# Filtering scrapped links to left only that will be useful for our analysis.
linksAA = []
for l in linksA:
    if ("posiedzenia" in str(l)) and ("senat/posiedzenia" not in str(l)) and (l not in linksAA):
        linksAA.append(l)
    if limit == 1:
        if l == Limit:
            break
len(linksAA)


linksAAA = [s for s in linksAA if "prace/posiedzenia" in s]
linksAAA
len(linksAAA)
# Filtering finished succesfully.

###################### LINKS PART 2 ####################################
# This part gathers links to voting's results pages from links gathered during first stage.

linksB = []
for lB in linksAAA:
    lB = lB.replace('tematy','przebieg')
    lB = lB.replace(',1',',1,glosowania')
    linksB.append(lB)

len(linksB)


###################### LINKS PART 3 ####################################
# During this stage, code saves direct links to print views of the voting results. One link from the stage 2 can provide more than one link so
# the limit option could be useful here.

linksCC = []

for urlC in linksB:
    hdrC = {'User-Agent': 'Mozilla/5.0'}
    reqC = Request(urlC,headers=hdrC)
    pageC = urlopen(reqC)
    soupC = BeautifulSoup(pageC)

    linksC = soupC.find_all('a', attrs={'href': re.compile("^https?://")})
    for link in linksC:
        linksCC.append(link.get('href'))
        print(link.get('href'))

    linksCCC = [c for c in linksCC if "drukuj" in c]
    
if limit == 1:
    linksCCCC = list(set(linksCCC))
    linksCCCC = linksCCCC[:100]
else:
    linksCCCC = list(set(linksCCC))

len(linksCCCC)

########################### VOTES ###########################################
# At this stage we gather information that is interesting for us - voting results.
# We save at "names" names of the senators, at "voting" voting results for specific senator (yes, no, didn't participate during specific voting),
# at "glosowanie" we save link to the voting result to manage filtering options during post-scrapping analysis.

names = []
voting = []
glosowanie = []

for urlD in linksCCCC:
    hdrD = {'User-Agent': 'Mozilla/5.0'}
    reqD = Request(urlD,headers=hdrD)
    pageD = urlopen(reqD)
    soupD = BeautifulSoup(pageD)
    #linksD = soupD.find_all('div', {"class": 'senator'})
    s = soupD.find_all('div', {"class", 'col-lg-3 col-sm-4 col-xs-6'})
    senators = list(s)
    for name in senators:
        name1 = name.text.replace('\t',"").replace('\n',"")
        names.append(name1)
        glosowanie.append(urlD)

    g = soupD.find_all('div', {"class", 'col-lg-1 col-sm-2 col-xs-6'})
    glosy = list(g)
    for wynik in glosy:
        wynik1 = wynik.text.replace('\t',"").replace('\n',"")
        voting.append(wynik1)

    D = pd.DataFrame({'name': names, 'vote': voting, 'link':glosowanie})
        
    print(D)

###################### EXCEL GENERATION #######################################
# We save our results in Excel table. Now those results are ready for analysis and easy to read.

if limit == 1:
    D.to_excel('glosowanko100.xlsx', encoding="utf-8", index=False)
else:
    D.to_excel('glosowanko.xlsx', encoding="utf-8", index=False)
