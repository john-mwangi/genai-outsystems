import json
import pathlib
from urllib.parse import urljoin

import html2text
import scrapy
from scrapy.http import HtmlResponse


class OsdocsSpider(scrapy.Spider):
    name = "osdocs"
    allowed_domains = ["outsystems.com"]
    start_urls = [
        "https://success.outsystems.com/documentation/11/",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not pathlib.Path("output").exists():
            pathlib.Path("output").mkdir()

        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = True
        self.converter.ignore_emphasis = True
        self.converter.ignore_images = True
        self.converter.ignore_tables = True

    def parse(self, response: HtmlResponse):
        url = "https://success.outsystems.com/screenservices/Documentation_UI/TOC/LeftTableOfContents/DataActionGetLeftToCDataSource"

        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Content-Length": 341,
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://success.outsystems.com",
            "Outsystems-Locale": "en-US",
            "Pragma": "no-cache",
            "Referer": "https://success.outsystems.com/documentation/11/",
        }

        yield scrapy.Request(
            url, callback=self.parse_toc, headers=headers, method="POST"
        )

    def parse_toc(self, response: HtmlResponse):
        raw_data = response.body
        data = json.loads(raw_data)
        headings = data["data"]["Hierarchy"]["List"]

        urls = list(self.parse_list_of_nested_dicts(headings))

        with open("output/urls.txt", mode="w") as f:
            f.write(urls)

    def parse_list_of_nested_dicts(self, data: list[dict]):
        for item in data:
            for k, v in item.items():
                if k == "URL":
                    yield v
            topics = item["Topics"]["List"]
            if len(topics) > 0:
                self.parse_list_of_nested_dicts(topics)
