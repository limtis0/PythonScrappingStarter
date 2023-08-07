import os
from pathlib import Path

from typing import Union

from seleniumwire import webdriver
from seleniumwire.webdriver import Chrome
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_selenium(
        apply_stealth: bool = True,
        executable_path: Union[str, bytes, os.PathLike] = None,
        download_path: Union[str, bytes, os.PathLike] = None) -> Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    if apply_stealth:
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

    if download_path:
        prefs = {
            "download.default_directory": str(Path(download_path).absolute()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        }
        options.add_experimental_option("prefs", prefs)

    if executable_path:
        service = Service(executable_path)
    else:
        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(options=options, service=service)

    if apply_stealth:
        stealth(driver,
                languages=["en-US", "en"],
                platform="Win32",
                fix_hairline=True,
                )

    return driver
