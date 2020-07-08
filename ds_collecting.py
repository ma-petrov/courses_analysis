import requests
import re
import lxml.html as html
from bs4 import BeautifulSoup

STEPIK_URL = "https://stepik.org/course/{}/promo"

def parse_course_page(page_num): #71439
    soup = BeautifulSoup(requests.get(STEPIK_URL.format(page_num)).text, 'lxml')
    """
    with open('course_page_content.txt', 'w') as f:
        for element in soup.find_all('div'):
            f.writelines(element.lines)
    """
    for tag in soup.find_all(class_='toc-promo__lesson toc-promo-lesson ember-view'):
        print(tag)
        """
        regex = re.compile('[А-Яа-я]+')
        text = regex.findall(tag.name)
        print(text)
        """

        

# Content description class: 'toc-promo-lesson__title'
# 'toc-promo__lesson toc-promo-lesson ember-view'

parse_course_page(71439)



"""
hrefs = re.findall('["\']https[A-Za-z0-9:/.]+["\']', response.text)
"""