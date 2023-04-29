import scrapy
import os, re
import requests
from bs4 import BeautifulSoup

class ProblemSpider(scrapy.Spider):

    name = "problem"
    allowed_domain = "https://codeforces.com/"
    start_urls = []

    def start_requests(self):
        pages_number = 85
        for page_id in range(1, pages_number + 1):
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
        contest_name = response.css("#sidebar div table tbody tr:nth-child(1) th a::text").get()

        statement = response.css("#pageContent div.problemindexholder div.ttypography div div").getall()

        body_name = ['header', 'statement', 'input', 'output', 'example', 'note']

        text = ''
        for id in range(len(statement)):
            html = statement[id]
            sep = '\n'

            soup = BeautifulSoup(html)
            for img in soup.find_all('img'):
                src = img['src']
                img.replace_with(src)

            add_text = soup.get_text(separator=sep, strip=True)

            if not(add_text in text):
                text = text + add_text + '\n'

        yield {
            "Contest name": contest_name,
            "Problem name": problem_name,
            "Description": text
        }
