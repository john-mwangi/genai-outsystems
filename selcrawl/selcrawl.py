from html2text import HTML2Text
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def main():
    options = Options()
    options.add_argument("--enable-javascript")

    webdriver_service = Service(executable_path="./chromedriver")
    driver = webdriver.Chrome(service=webdriver_service, options=options)

    url = "https://success.outsystems.com/documentation/11/"
    driver.get(url)
    driver.implicitly_wait(30)

    page_source = driver.page_source

    converter = HTML2Text()
    converter.ignore_emphasis = True
    converter.ignore_images = True
    converter.ignore_links = True
    converter.ignore_tables = True

    text = converter.handle(page_source).strip()

    with open("output.txt", mode="w") as f:
        f.write(text)

    driver.quit()


if __name__ == "__main__":
    main()
