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
    browser.add_cookie({"name": "MUSIC_U", "value": "005BE67412AC76FCB8F9270B18757DADA94AC0F63DCD8CFFD9931ED10E5F13403C5E44CD0DE95DB6BE0D33A78A53D7BD724C7FF974847E79EC9724255DC884A6BA9A2F3EB277078A64A018A4A1642A352F797C9AA39D80D846DDAE158787F51534180F909F59035F039C43FDC6B9FB9AAB7BF362F0C3188A84E2B1F58C7660B61C705CDB037E6134737D865C606E4D9CAB04DF41095E89ADE6F50507092BB7F7D8BCEBF5347C974CBA59F706FAB7D5CB9E12802A6C042D379B3C3CEA3D69B3282CB245FBC7FA2EE4EB5A03DB3D44E574E56AD699F1E59E63FB6BBEDE2A6CB5AF037E3EB99A7D725D9D78AE6DD62B1D7889287FCFFE8B3BCF928A8CC8CAC72192FDCB45B819CDDA80CA713AECC6D2BD55D8B845030088C3EEC7979437D2299A7DF53333803DC6BE129D5361934C6C81BB7F60F4B48D9D56505CCDB106D220BFAFFC423420A40A7774E5FDBF97AFECE9F73E270FEBF8F45156EFDC31BDD7672B776A"})
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
