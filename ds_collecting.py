"""
Version 2.0 (Coursera)
Site parcing based on Selenium WebDriver
"""

import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

COURSERA_URL = 'https://ru.coursera.org/courses'

# function make driver waits 20 seconds and find elemet by class name
def wait_and_find_by_class(driver, element):
    try:
        return WebDriverWait(driver, 20).until(lambda driver : driver.find_element_by_class_name(element))
    finally:
        pass

# 
def main():

    course_mark = []

    driver = webdriver.Chrome(executable_path='C:/ProgramData/chromedriver_win32/chromedriver.exe')
    driver.get(COURSERA_URL)
    driver.implicitly_wait(20)

    # finding element with course mark and adding in to list course_mark
    element = driver.find_element_by_class_name('ratings-text')
    course_mark.append(str(element))
    print(course_mark)

    #element = wait_and_find_by_class(driver, 'ratings-text')
    #course_mark.append(str(element))
    #print(course_mark)

    element = driver.find_element_by_class_name('image-wrapper vertical-box')
    element.click()

if __name__ == "__main__":
    main()

