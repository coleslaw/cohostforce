import scrapy
import os, re
from csv import DictWriter, writer

def get_title(rating):
    if rating < 1200:
        return 'Newbie'
    elif rating < 1400:
        return 'Pupil'
    elif rating < 1600:
        return 'Specialist'
    elif rating < 1900:
        return 'Expert'
    elif rating < 2100:
        return 'Candidate Master'
    elif rating < 2300:
        return 'Master'
    elif rating < 2400:
        return 'International Master'
    elif rating < 2600:
        return 'Grandmaster'
    elif rating < 3000:
        return 'International Grandmaster'
    else:
        return 'Legendary Grandmaster'



class ContestSpider(scrapy.Spider):

    name = "contest"
    allowed_domain = "https://codeforces.com"
    start_urls = []

    def start_requests(self):
        pages_number = 639
        for page_id in range(1, pages_number):
            url = f"https://codeforces.com/ratings/page/{page_id}"

            self.start_urls.append(url)

        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.access_user_href)

    def access_user_href(self, response):
        hrefs = response.css("#pageContent  div.datatable.ratingsDatatable  div:nth-child(6)  table tr td a::attr(href)").getall()
        for href in hrefs:
            url = self.allowed_domain + href
            yield scrapy.Request(url=url, callback=self.access_contest_href)

    def access_contest_href(self, response):
        href = response.xpath('//div[@id="pageContent"]/div[1]/ul/li/a[text()="Contests"]//@href').get()
        url = self.allowed_domain + href
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        string = str(response)

        string = string.replace('<200 https://codeforces.com/contests/with/', '')
        string = string.replace('>', '')
        username = string

        key_block = response.css('table.tablesorter.user-contests-table thead tr')
        table = {}
        table_keys = []
        table_values = []

        for key in key_block:
            table_keys = key.css('th').css('::text').extract()
        table_keys.append('Title')

        data_block = response.css('table.tablesorter.user-contests-table tbody tr')
        for data in data_block:
            values = data.css('td')[0:-1].css('::text').extract()
            columns_data = []
            for item in values:
                item = item.strip()
                if item != '':
                    columns_data.append(item)
            columns_data.append(get_title(int(columns_data[-1])))

            table_values.append(columns_data)

        user_contest_url = 'data/info/contest_info/' + username + '.csv'
        with open(user_contest_url, 'a'): # create new file
            os.utime(user_contest_url, None)

        with open(user_contest_url, 'w+') as f_object:
            dictwriter_object = writer(f_object)
            dictwriter_object.writerow(table_keys)
            for value in table_values:
                dictwriter_object.writerow(value)
