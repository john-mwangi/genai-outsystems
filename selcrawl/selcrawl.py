import subprocess
import sys
import time
import tkinter
from pathlib import Path
from typing import Union

import pyautogui
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def clean_path(path: str) -> str:
    return path.split(sep=":", maxsplit=1)[1].strip()


def install_driver(browser: str = "firefox") -> Union[tuple[str, str], None]:
    """Installs the appropriate web driver.

    Args:
    ---
    brower: browser driver to install. See `$selenium-manager --help` for options

    Returns:
    ---
    driver_clean: driver absolute path
    browser_clean: binaries absolute path
    """

    cmd = f"selenium-manager --browser {browser}"

    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)

    lines = result.stdout.splitlines()

    driver_path = [line for line in lines if line.startswith("INFO\tDriver path:")]
    browser_path = [line for line in lines if line.startswith("INFO\tBrowser path:")]

    if driver_path:
        driver_clean = clean_path(driver_path[0])
        browser_clean = clean_path(browser_path[0])

        print("Driver path:", driver_clean)
        print("Browser path:", browser_clean)

        return driver_clean, browser_clean
    else:
        print("Driver not found.")
        return None


def get_driver():
    driver_path, browser_path = install_driver("chrome")
    webdriver_service = Service(executable_path=driver_path)

    options = Options()
    options.add_argument("--enable-javascript")
    options.add_argument("--start-maximized")
    options.binary_location = browser_path

    driver = Chrome(service=webdriver_service, options=options)

    return driver


def extract_react_html(url: str, page_load_time: int = 30):
    """Extracts React generated HTML from the browser's devtools and saves the
    content locally.

    Args:
    ---
    url: the page to extract html content
    page_load_time: time in secs to allow for the page to load
    """

    driver = get_driver()
    driver.get(url)

    print(f"waiting for {page_load_time=} sec...")
    time.sleep(page_load_time)

    # Accept cookies
    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()

    # Open devtools
    # https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
    cmd_ctrl = ["command", "option"] if sys.platform == "darwin" else ["ctrl", "shift"]

    with pyautogui.hold(cmd_ctrl):
        pyautogui.press("i")

    time.sleep(3)

    # # print X, Y positions
    # print("Press Ctrl-C to quit.")
    # try:
    #     while True:
    #         x, y = pyautogui.position()
    #         positionStr = "X: " + str(x).rjust(4) + " Y: " + str(y).rjust(4)
    #         print(positionStr, end="")
    #         print("\b" * len(positionStr), end="", flush=True)
    # except KeyboardInterrupt:
    #     print("\n")

    # Copy React generated code
    # TODO: Make this dynamic
    X = 984
    Y = 204

    pyautogui.click(button="right", x=X, y=Y)
    pyautogui.press("down", presses=6)
    pyautogui.press("right")
    pyautogui.press("down")
    pyautogui.press("enter")  # FIXME

    # Paste content as string
    react_html = tkinter.Tk().clipboard_get()

    dir_name = Path("html_files")

    if not dir_name.exists():
        dir_name.mkdir()

    file_path = dir_name / f"{hash(url)}.html"

    with open(file_path, mode="w") as f:
        f.write(react_html)

    driver.quit()


def parse_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.find_all("div", {"data-container-id": "b3-b4-b1-InjectHTMLWrapper"})

    print(text)


if __name__ == "__main__":
    url = "https://success.outsystems.com/documentation/11/getting_started/"
    # extract_react_html(url)

    html_files = Path("html_files").glob("*.html")

    file = list(html_files)[0]

    with open(file, mode="r") as f:
        html = f.read()

    parse_html(html)
