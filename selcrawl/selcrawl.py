import subprocess
import sys
import time
import tkinter
from typing import Union

import pyautogui
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def clean_path(path: str) -> str:
    return path.split(sep=":", maxsplit=1)[1].strip()


def install_driver(browser: str = "firefox") -> Union[tuple[str, str], None]:
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


if __name__ == "__main__":
    url = "https://success.outsystems.com/documentation/11/getting_started/"
    PAGE_LOAD_TIME = 30

    driver = get_driver()
    driver.get(url)

    print(f"waiting for {PAGE_LOAD_TIME=} sec...")
    time.sleep(PAGE_LOAD_TIME)

    # accept cookies
    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()

    # open devtools
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

    # copy React generated code
    X = 984
    Y = 204

    pyautogui.click(button="right", x=X, y=Y)
    pyautogui.press("down", presses=6)
    pyautogui.press("right")
    pyautogui.press("down")
    pyautogui.press("enter")

    # paste content as string
    react_html = tkinter.Tk().clipboard_get()

    with open("output.html", mode="w") as f:
        f.write(react_html)

    driver.quit()
