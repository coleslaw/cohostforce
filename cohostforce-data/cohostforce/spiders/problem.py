import scrapy
import os, re
import requests
from bs4 import BeautifulSoup

from cohostforce.items import ProblemItem

class ProblemSpider(scrapy.Spider):

    name = "problem"
    allowed_domain = "https://codeforces.com/"
    start_urls = []

    def start_requests(self):
        pages_number = 2
        for page_id in range(1, pages_number):
            url = f"https://codeforces.com/problemset/page/{page_id}"
            self.start_urls.append(url)

        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.access_problem_href)

    def access_problem_href(self, response):
        hrefs = response.css("#pageContent div.datatable div:nth-child(6) table tr td:nth-child(1) a")
        for href in hrefs:
            href = href.css("::attr(href)").get().strip()
            url = self.allowed_domain + href
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        problem_name = response.css("#pageContent div.problemindexholder div.ttypography div div.header div.title::text").get()
        contest_name = response.css("#sidebar div:nth-child(1) table tbody tr:nth-child(1) th a::text").get()

        statement = response.css("#pageContent div.problemindexholder div.ttypography div div").getall()

        body_name = ['header', 'statement', 'input', 'output', 'example', 'note']

        text = ''
        for id in range(len(statement)):
            html = statement[id]
            sep = '\n'
            soup = BeautifulSoup(html)
            add_text = soup.get_text(separator=sep, strip=True)
            if not(add_text in text):
                text = text + add_text + '\n'

        problem_name = problem_name.replace('.', '_')
        problem_name = problem_name.replace(' ', '_')
        problem_name = problem_name + '.txt'



        '''header_url = 'data/contests/' + contest_name
        if not os.path.exists(header_url):
            os.makedirs(header_url)
        total_url = os.path.join(header_url, problem_name)
        with open(total_url, 'w') as f:
            f.write(text)'''

        yield {
            "Problem name": problem_name,
            "Description": text
        }
