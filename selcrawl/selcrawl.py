import subprocess
import sys
import time
import tkinter
from enum import Enum
from pathlib import Path
from typing import Union

import html2text
import pyautogui
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class ContentType(Enum):
    HTML = "html_files"
    TEXT = "txt_files"


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

    dir_name = Path(ContentType.HTML.value)

    if not dir_name.exists():
        dir_name.mkdir()

    page_name = url.split("/")[-2]
    file_path = dir_name / f"{page_name}.html"

    with open(file_path, mode="w") as f:
        f.write(react_html)

    driver.quit()


def parse_html(html: str, file_name: str):
    """Extract useful content from a html file and save it as a txt file"""

    print(f"Converting to text {file_name}...")

    soup = BeautifulSoup(html, "html.parser")

    converter = html2text.HTML2Text()
    converter.ignore_links = True
    converter.ignore_images = True
    converter.ignore_tables = True

    content = soup.find("div", id="b3-b4-b1-InjectHTMLWrapper")

    text = converter.handle(str(content))

    dir_name = Path(ContentType.TEXT.value)

    if not dir_name.exists():
        dir_name.mkdir()

    file_path = dir_name / file_name

    with open(file_path, mode="w") as f:
        f.write(text)


def page_parsed(page_name: str, type: ContentType):
    """Determines if a url's html content has been extracted or converted to text"""

    file_extension = type.value.split("_")[0]
    dir_name = type.value

    files = Path(dir_name).glob(f"*.{file_extension}")
    return any([file.stem == page_name for file in files])


def main(url: str):
    page_name = url.split("/")[-2]

    html_parsed = page_parsed(page_name, type=ContentType.HTML)
    txt_parsed = page_parsed(page_name, type=ContentType.TEXT)

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
    url = "https://success.outsystems.com/documentation/11/getting_started/"

    main(url)
