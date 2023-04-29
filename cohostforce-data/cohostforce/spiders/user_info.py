import scrapy
import os, re
from csv import DictWriter, writer
from bs4 import BeautifulSoup

def get_title(rating):
    ratings = [1200, 1400, 1600, 1900, 2100, 2300, 2400, 2600, 3000]
    titles = ["Newbie", "Specialist", "Expert", "Candidate", "Master", "International Master", "Grandmaster", "International Grandmaster", "Legendary Grandmaster"]
    for id in range(len(ratings)):
        if rating < ratings[id]:
            return titles[id]

class ContestSpider(scrapy.Spider):

    name = "user_info"
    allowed_domain = "https://codeforces.com"
    start_urls = []
    map_link = {}

    def start_requests(self):
        pages_number = 640
        for page_id in range(1, pages_number):
            url = f"https://codeforces.com/ratings/page/{page_id}"
            self.start_urls.append(url)

        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.access_user_href)


    def access_user_href(self, response):
        hrefs = response.css("#pageContent  div.datatable.ratingsDatatable  div:nth-child(6)  table tr td a::attr(href)").getall()
        for href in hrefs:
            url = self.allowed_domain + href
            yield scrapy.Request(url=url, callback=self.get_user_info)


    def get_user_info(self, response):
        title = response.css("#pageContent div:nth-child(3) div div div span::text").get()
        html = response.css("#pageContent div:nth-child(3) div div div h1 a").get()
        soup = BeautifulSoup(html)
        username = soup.get_text(separator='')
        rating = response.css("#pageContent div:nth-child(3) div div ul li:nth-child(1) span::text").get()
        max_rating = response.css("#pageContent div:nth-child(3) div div ul li:nth-child(1) span span:nth-child(2)::text").get()

        href = response.xpath('//div[@id="pageContent"]/div[1]/ul/li/a[text()="Contests"]//@href').get()
        url = self.allowed_domain + href
        self.map_link[url] = {
            "title": title,
            "username": username,
            "rating": int(rating),
            "max_rating": int(max_rating),
        }
        yield scrapy.Request(url=url, callback=self.get_contests_info)


    def get_contests_info(self, response):
        user_info = self.map_link[response.request.url]

        # get key from table
        key_block = response.css('table.tablesorter.user-contests-table thead tr')
        table, table_keys = {}, []
        for html in key_block:
            table_keys = html.css('th').css('::text').extract()
        table_keys.append('Title')

        # initialize user_contest
        lst_contest = []

        data_block = response.css('table.tablesorter.user-contests-table tbody tr')
        for html in data_block:
            new_val = [value.strip() for value in html.css('td')[0:-1].css('::text').extract() if value.strip() != '']
            lst_contest.append(dict(zip(table_keys, new_val)))

        yield {
            "title": user_info['title'],
            "username": user_info['username'],
            "rating": user_info['rating'],
            "max_rating": user_info['max_rating'],
            "contests": lst_contest
        }

