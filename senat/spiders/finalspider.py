#Michał Sekowski
import scrapy

#preparing classes needed for scraper to work, class Link will carry links, and Senathor will contain
#Senator name, type of vote and link
class Link(scrapy.Item):
    link = scrapy.Field()

class Senathor(scrapy.Item): 
    voteID    = scrapy.Field()
    name      = scrapy.Field()
    vote      = scrapy.Field()

class LinksSpider(scrapy.Spider):

    #setting up starting page

    name = 'senat_scraper'
    allowed_domains = ['www.senat.gov.pl']
    start_urls = ['https://www.senat.gov.pl/prace/posiedzenia/tematy-posiedzen-senatu-ix-kadencji/']

    #Below there is 100-pages limit mechanism, if limit value is True, only data from 100 votings will be gathered,
    #otherwise data from whole cadency will be colected

    limit = True
    countlimit = 100
    count = 0

    #defining first parse function, thats job is to gather links leading to specific session sites

    def parse(self, response):
        follow_it = []
        follow_it2 =[]
        xpath = '//div[@class="tresc"]//a/@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] =s.get()

            #initial selection contains a lot of links that im not interested in, some of them are download links,
            #some are duplicates and some do not even work. Therefore I use If function to append to my list of links
            #only those that I need

            if ("posiedzenia" in str(l['link'])) and ("download" not in str(l['link'])) and ("senat/posiedzenia" not in str(l['link'])) and (l['link'] not in follow_it):
                follow_it.append(l['link'])

        #step below is well-described in project description. Basically I reduce number of needed parse functions by 1
        #by simply replacing parts of links

        for item_url in follow_it:
            item_url = item_url.replace('tematy','przebieg')
            item_url = item_url.replace(',1',',1,glosowania')
            follow_it2.append(item_url)

            #now that I have proper links and no duplicates, I can step one level deeper in scraping
            #and for each of links collected in parse, call for parse2 function

            yield scrapy.Request(item_url,
                      callback=self.parse2, dont_filter=True)

    def parse2(self, response):
        selection = response.xpath('//*[@class="col-lg-4 col-md-4 col-sm-4 col-xs-4"]/a/@href')
        for s in selection:
            r = Link()
            r['link'] =s.get()

            #parse2 function collects final links which lead to pages with data I would like to scrap.
            #Therefore in this place I put second part of that 100-page limiter mentioned at beginning of class
            #If limit=True, code will go through first If statement, collecting data from 100 pages.
            #If limit=False, code from second If will be used, and data from whole cadency will be gathered.

            #For each link selected in this new selection, final function parse3 is called.
            #What is different from previous yield, is using "meta" parameter. What it does it enables
            #to pass objects between parse functions. I use it to pass links, so that it can be yielded
            #within senathor class, thus making further analysis possible


            if ((self.limit == True) and (self.count < self.countlimit)):
                self.count = self.count + 1
                yield scrapy.Request(r['link'],
                      callback=self.parse3, dont_filter=True, meta={'item': r['link']})
            if (self.limit == False):
                yield scrapy.Request(r['link'],
                      callback=self.parse3, dont_filter=True, meta={'item': r['link']})

    #Here I define last parse function, which from pages received from parse2, scraps data about Senators
    #that took part in certain voting and how did they vote


    def parse3(self, response):
        counter = 0
        xpath = '(//div)[@class ="senator"]'
        selection = response.xpath(xpath)

        #I noticed that number of senators present on different votings do vary. Because of that, before I scrap data,
        #Firstly I count how many senators were on chosen voting

        for j in selection:
            counter += 1
        
        for i in range(1,counter):
            S = Senathor()

            #to get to next senator, such Xpath should be used:
            #'(//div)[@class ="senator"][1]/div[1]/text()'
            #'(//div)[@class ="senator"][2]/div[1]/text()'
            #'(//div)[@class ="senator"][3]/div[1]/text()'
            #and so on. Because of this, I used some simple string-building trick, that allowed
            #to change that integer inside xpath fully automatic, and reach all senators.
            #Also this is why I needed to count how many senators are present on website earlier.


            S['name'] = response.xpath('(//div)[@class ="senator"]['+str(i)+']/div[1]/text()').get().strip()
            S['vote'] = response.xpath('(//div)[@class ="senator"]['+str(i)+']/div[2]/text()').get().strip()
            S['voteID'] = response.meta['item']
            yield S

            #Finally, for each senator, scraper yields Senathor class, which consist of name, vote and link to site with voting


