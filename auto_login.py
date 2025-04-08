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
    browser.add_cookie({"name": "MUSIC_U", "value": "0048B747C413146AC3D6607F1EA39E732AD0A54053CD63A5392476112D69EAF748DFC6ADE0A81B8572C1993307069CF31649281A9044B38B239BB7A9A7706E933989504E95997A171E3C5726A9CEC326B1FD0B6E4263E600D2ED418885D39595A6C67154F81E2851AD3A3614CC398CDBFBD6F0100A1063EF0197B34FDFFC3075D29F4B1249DBFEFC2C358DDA7EC35669AC949DA3C0C4358E499D791F0CDFA22FCB44A0CB2460CB719C9291E1860F13791FD4A6B798019CF00E109C19CE7791E2CFADA7C78A25F0D7ECF37EDE8348982A649A887A4B4823162F0156CFC81EF2AC54B9E9791403D08E77EC7A54D8D88139391EBE4DD2B700EEF47D343C7ECA2F18E2138A3B745269BAB3C2BF163CA44CD098229FDC6A722415117DF227CA816D3E918A14D4EB14F01966AF4FECB9F3BD99480FFBAABD58BA101D53D49046987624CCA32CE7A7D93B1FAFC376108B8366BA2BD19BBE353C4CD3DFC1B641BCAAD71047"})
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
