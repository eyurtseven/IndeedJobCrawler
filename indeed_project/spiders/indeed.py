# -*- coding: utf-8 -*-
import datetime
import scrapy
import logging
import sys

from indeed_project.items import IndeedProjectItem
from indeed_project.search_parameter import get_position_list, get_city_list


def generate_starter_urls():
    url_list = []

    position_list = get_position_list()
    city_list = get_city_list()

    pos_city_pattern = "https://tr.indeed.com/jobs?q=%s&l=%s"
    pos_pattern = "https://tr.indeed.com/jobs?q=%s&l="
    city_pattern = "https://tr.indeed.com/jobs?q=&l=%s"

    for city in city_list:
        url_list.append(city_pattern % city.encode(sys.getfilesystemencoding()))

    for position in position_list:
        url_list.append(pos_pattern % position.encode(sys.getfilesystemencoding()))
        pass

    for city in city_list:
        for position in position_list:
            params = (position.encode(sys.getfilesystemencoding()), city.encode(sys.getfilesystemencoding()))
            url_list.append(pos_city_pattern % params)
            pass

    return url_list


class IndeedIstanbulSpider(scrapy.Spider):
    name = "indeed_istanbul"
    allowed_domains = ["tr.indeed.com"]

    def start_requests(self):
        urls = generate_starter_urls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for jobListingContainer in response.css('.result'):

            if len(jobListingContainer.css('div.iaP span.iaLabel')) == 0:
                continue

            job_url = jobListingContainer.css('.jobtitle a::attr(href)').extract_first()
            if job_url is None:
                continue
            url_data = job_url
            if not (job_url.startswith('http') or job_url.startswith('https')):
                url_data = "http://tr.indeed.com" + job_url

            yield scrapy.Request(
                url_data,
                callback=self.job_detail_parse
            )
        pass

        next_page = response.xpath('//div[@class="pagination"]/a[last()]/@href').extract_first()
        logging.log(logging.INFO, next_page)
        if next_page:
            npt = next_page
            if not (npt.startswith('http') or npt.startswith('https')):
                npt = "http://tr.indeed.com" + next_page

                yield scrapy.Request(
                    npt,
                    callback=self.parse
                )

    @staticmethod
    def job_detail_parse(response):

        if 'indeed' in response.url:
            job_title = response.css('.jobtitle font::text').extract_first()
            company = response.css('.company::text').extract_first()
            location = response.css('.location::text').extract_first()
            summary = response.css('.summary').extract_first()
            date = response.css('.date::text').extract_first()
            job_url = response.url

            item = IndeedProjectItem(
                job_title=job_title,
                job_url=job_url,
                company=company,
                location=location,
                summary=summary,
                date=date,
                create_date=datetime.datetime.now()
            )

            yield item
        pass
