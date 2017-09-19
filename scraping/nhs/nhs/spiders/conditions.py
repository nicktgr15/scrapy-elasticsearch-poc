# -*- coding: utf-8 -*-
import scrapy
import re
from w3lib.html import remove_tags, remove_tags_with_content


class ConditionsSpiderSpider(scrapy.Spider):
    name = 'conditions'

    def start_requests(self):
        urls = [
            "http://www.nhs.uk/Conditions/Pages/hub.aspx"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_conditions_home_page)

    def parse_conditions_home_page(self, response):
        """
        Verify that 27 requests (26 letters + 0-9) were made

        @url http://www.nhs.uk/Conditions/Pages/hub.aspx
        @returns requests 27 27
        """
        for letter_href in response.css('#haz-mod1 ul li a::attr(href)'):
            yield response.follow(letter_href, self.parse_conditions_for_letter)

    def parse_conditions_for_letter(self, response):
        """
        Verify that 9 requests were made (1 is dropped because regex is
        not matching)

        @url http://www.nhs.uk/Conditions/Pages/BodyMap.aspx?Index=J
        @returns requests 9 9

        """
        for letter_condition_href in response.css('#haz-mod5 li a::attr(href)'):
            if re.search("^/conditions/", letter_condition_href.extract()):
                yield response.follow(letter_condition_href,
                                      self.parse_condition_page)

    def parse_condition_page(self, response):
        """
        Verify that 1 item is returned and 3 additional requests are made (one
        for each one of the tab items). Also verify that the expected fields
        are contained in the returned item.

        @url http://www.nhs.uk/conditions/Food-poisoning/Pages/Introduction.aspx
        @returns requests 3 3
        @returns items 1
        @scrapes main_content url title

        """
        main_content = response.css('.healthaz-content').extract_first()
        main_content_text = remove_tags(
            remove_tags_with_content(main_content, ('script', 'noscript')))

        yield {
            "main_content": main_content_text,
            "url": response.url,
            "title": response.css('.healthaz-header h1::text').extract_first()
        }

        for tab_href in response.css('#ctl00_PlaceHolderMain_articles a::attr(href)'):
            yield response.follow(tab_href, self.parse_condition_page)
