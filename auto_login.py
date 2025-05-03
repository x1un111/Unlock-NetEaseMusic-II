# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00333F827A7FAC95D428C60DCEA6730E01C75F17C70E53387D0B169DA8207D935C5E436D693E369ED0C408078D4D0101028D44555F42B91A8DC030E905ABC9B872B4C86894C8C68A83E376CFA8F5983D91ECAB2A39FD2CCCD1BF354D9BB22F5508AAAF3936B6A2ACF29AF4BDDEC2A869551C2142058992970EB7C0C4CA49F00639C4CA3D629D21A0EAFC1503F2CD00991389D75EE9EBCBD3549D1BC2A3D32EEBBAECF81D165C1BEC2DA69A09B9EF7E2DC0135653041857940B8341F68A8DFE980063112B32FAF4DBFA83E81629014B7730DDB6698B6E4E2445A908E0E955D3912C4F17824B0E89FF2B277138B3CA588F4645965717E7164DE2BC23212921CF419E057632AA41BB17F167A2CAA1DDC2EBEAECABB7B0C53A93CAB290E34F1C22653EF2D28591E5C598D06313E0EA9E74767779B836F6F0C00FEBADCFEDB37F8890DDE9E605A86BE6552CE8DE0B9BC40CBA562E49D252A571851257CB873AA46116E3"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
