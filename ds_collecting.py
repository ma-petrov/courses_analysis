"""
Version 2.0 (Stepik)
Site parcing based on Selenium WebDriver
"""

import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

STEPIK_URL = "https://stepik.org/course/{}/promo"

driver = webdriver.Chrome(executable_path='C:/ProgramData/chromedriver_win32/chromedriver.exe')
driver.get(STEPIK_URL.format('1'))
driver.close()
