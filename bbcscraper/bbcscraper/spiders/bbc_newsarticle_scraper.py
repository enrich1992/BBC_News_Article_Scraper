'''
Code written to scrape a news website (BBC : 'https://bbc.com/')
Extract all the main articles from the home page and
scrape information (such as article url, article title, article date, article author and article body)
related to each page.
This information is then sent and stored in a hosted Database (MongoDB Atlas)

Created on 16 April 2021
by Enrich Braz
'''


# Import required modules
import scrapy
from ..items import BbcscraperItem
from scrapy.http import Request
import regex


class cnnscrape(scrapy.Spider):
    # Important information about our spider which will tells it which website to start the crawl.
    name = 'bbccrawl'
    allowed_domains = ['bbc.com']
    start_urls = [
        'https://bbc.com/'
    ]

    def parse(self, response):

        # Create an Item which will store the information we want to scrape
        item = BbcscraperItem()

        # We first want to scrape all the urls of the various news titles listed on homepage
        # On inspecting the html page, we extract the url from the href attribute of h3
        # of the media__content division.
        # Some urls didn't contain the https://bbc.com part so we append this to those that don't.
        # Also certain media__content divisions didn't contain any url so we skip those Null responses.
        for media__content in response.css('div.media__content'):

            temp = media__content.css('h3 a::attr("href")').extract_first()
            if temp is None:
                continue
            elif temp.startswith('https:'):
                item['article_url'] = media__content.css('h3 a::attr("href")').get()
            else:
                item['article_url']='https://bbc.com'+temp

            # Now that we have a url in the proper format, we send a request to scrape the data from that URL page
            request = Request(item['article_url'], callback=self.parse_article_page, meta={'item': item})
            yield request

    # This function scrapes all the data we need from a given URL page
    def parse_article_page(self,response):
        # this retrieves our Item object from the previous function
        item=response.meta['item']

        # Scraping the article TITLE of each url page
        item['article_title'] = response.css('h1::text').get()
        # The source code of Certain pages store the article title in a different format
        if item['article_title'] is None:
            item['article_title'] = response.css('div.article-headline__text::text').get()

        # Scraping the DATE/TIME article was published
        item['article_date_time'] = response.css('time::text').get()
        # The source code of Certain pages store the date/time of article  in a different format
        if item['article_date_time'] is None:
            te= response.css('div.author-unit')
            item['article_date_time'] = te.css('span::text').get()
            if item['article_date_time'] is None:
                te1 = response.css('div.primary-content')
                item['article_date_time'] = te1.css('span::text').get()
                if item['article_date_time'] is None:
                    item['article_date_time'] = response.css('span::text').get()

        # Scraping the AUTHOR of the article
        item['article_author'] = response.css('div.author-unit a::text').get()
        # The source code of Certain pages store the author of the article in a different format
        if item['article_author'] is None:
            item['article_author'] = response.css('strong::text').get()
            # Some articles actually dont have any author mentioned, so we put No author found for such articles
            if item['article_author'] is None:
                item['article_author'] = 'No author Found'

        # Scraping the BODY of the article
        article_body=[]
        article_content = response.css('article')
        for p in article_content.xpath('//p//text()').extract():
            # we clean each string extracted from the para p.
            p = self.cleanfunc(p)
            article_body.append(p)

        item['article_body']=''.join(article_body)
        # Some data contain text styled in certain ways and hence have unicodes. So we need to clean it
        item['article_date_time'] = self.cleanfunc(item['article_date_time'])
        item['article_author'] = self.cleanfunc(item['article_author'])
        item['article_title'] = self.cleanfunc(item['article_title'])

        yield item

    # Function to clean unwanted text from articles
    def cleanfunc(self,line):

        # We clean the unicodes which often show up in html text
        line=line.encode("ascii","ignore")
        line=line.decode()
        line = regex.sub('\n', '', line)
        line = regex.sub('\"', '', line)
        # Every article body normally contains these lines, which are not related to the news.
        line = regex.sub('The BBC is not responsible for the content of external sites.', '', line)
        line = regex.sub('Read about our approach to external linking.', '', line)
        line = regex.sub('2021 BBC.', '', line)
        line = regex.sub('Follow us on Facebook, or on Twitter @BBCNewsEnts.', '', line)
        line = regex.sub('If you have a story suggestion email entertainment.news@bbc.co.uk.', '', line)
        return line
        # Please note that data extracted from article body will also contain, certain titles of other pages
        # towards the end. This can be removed by noting down the tiles and replacing them. However this is not
        # an elegant solution as the news webpage keeps changing almost everyday so the news titles will also
        # change. Due to time constraints, a proper solution wasn't arrived at to keep these titles out at the end.




