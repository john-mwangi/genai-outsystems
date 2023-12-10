import pathlib
from urllib.parse import urljoin

import html2text
import scrapy
from scrapy.http import HtmlResponse


class OsdocsSpider(scrapy.Spider):
    name = "osdocs"
    allowed_domains = ["outsystems.com"]
    start_urls = [
        "https://outsystems.com/documentation/11/",
        "https://success.outsystems.com/documentation/Best_Practices",
        "https://success.outsystems.com/documentation/How_to_Guides",
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
        text = self.converter.handle(response.body.decode())
        text = text.strip()

        url = response.url.strip("/")
        filename = f"output/{hash(url)}.txt"

        with open(filename, mode="w") as f:
            f.write(text)

        for link in response.xpath("//a/@href"):
            href: str = link.get()

            if href.startswith(
                "/documentation/11/",
                "/documentation/Best_Practices",
                "/documentation/How_to_Guides",
            ):
                url = urljoin(response.url, href)
                yield scrapy.Request(url, callback=self.parse)
