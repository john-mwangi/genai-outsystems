from pathlib import Path

from src.params import URLS_LIMIT, urls_path
from src.scrape_website import ContentType, extract_react_html, page_parsed, parse_html


# TODO: implement asynchronous (Puppeteer, Playwright)
def main(url: str):
    page_name = url.split("/")[-2]

    html_parsed = page_parsed(page_name, content_type=ContentType.HTML)
    txt_parsed = page_parsed(page_name, content_type=ContentType.TEXT)

    if not html_parsed:
        extract_react_html(url)

    if not txt_parsed:
        html_files = Path(ContentType.HTML.value).glob("*.html")
        files = list(html_files)

        for file in files:
            with open(file, mode="r") as f:
                html = f.read()

            parse_html(html, f"{file.stem}.txt")


if __name__ == "__main__":
    with open(urls_path) as f:
        urls = [line.strip() for line in f.readlines()]

    if URLS_LIMIT is not None:
        urls = urls[:URLS_LIMIT]

    for url in urls:
        main(url)
