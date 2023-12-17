from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_driver():
    options = Options()
    options.add_argument("--enable-javascript")
    options.add_argument("start-maximized")

    webdriver_service = Service(executable_path="./chromedriver")
    driver = webdriver.Chrome(options=options, service=webdriver_service)

    return driver


if __name__ == "__main__":
    driver = get_driver()
    url = "https://success.outsystems.com/documentation/11/"
    driver.get(url)
    page_source = driver.page_source
    source_text = BeautifulSoup(page_source, "html.parser")
    print(source_text.find_all("noscript"))

    while True:
        pass
