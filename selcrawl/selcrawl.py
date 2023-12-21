import subprocess
import time

from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def clean_path(path: str):
    return path.split(sep=":", maxsplit=1)[1].split()[0]


def install_driver(browser: str = "firefox"):
    cmd = f"selenium-manager --browser {browser}"

    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)

    lines = result.stdout.splitlines()

    driver_path = [line for line in lines if line.startswith("INFO\tDriver path:")]
    browser_path = [line for line in lines if line.startswith("INFO\tBrowser path:")]

    if driver_path:
        driver_path = clean_path(driver_path[0])
        browser_path = clean_path(browser_path[0])

        print("Driver path:", driver_path)
        print("Browser path:", browser_path)

        return driver_path, browser_path
    else:
        print("Driver not found.")


def get_driver():
    driver_path, browser_path = install_driver()
    webdriver_service = Service(executable_path=driver_path)

    options = Options()
    options.add_argument("--enable-javascript")
    options.binary_location = browser_path

    driver = Firefox(service=webdriver_service, options=options)

    return driver


if __name__ == "__main__":
    url = "https://success.outsystems.com/documentation/11/"
    PAGE_LOAD_TIME = 60

    driver = get_driver()
    driver.get(url)

    print(f"waiting for {PAGE_LOAD_TIME} sec...")
    time.sleep(PAGE_LOAD_TIME)

    print("sending keys...")
    actions = ActionChains(driver)
    options_key = "\u2325"

    (
        actions.send_keys(Keys.TAB)
        .send_keys(Keys.ENTER)
        .key_down(Keys.COMMAND)
        .send_keys("f")
        .key_up(Keys.COMMAND)
        .perform()
    )

    print("done")

    while True:
        pass
