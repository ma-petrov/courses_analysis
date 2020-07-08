import requests
import re
import lxml.html as html
from bs4 import BeautifulSoup

ONLINE_EDU_URL = 'https://online.edu.ru/public/course?faces-redirect=true&cid=3476'

def parse_course_page(url):
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    
    for tag in soup.find_all(class_='ui-outputpanel ui-widget user-profile-view'):
        regex = re.compile(r'[0-9]+.\s[А-Яа-я0-9\-\s,.]+')
        text = regex.findall(str(tag))
        #print(text)

    for tag in soup.find_all(class_='ui-outputpanel ui-widget'):
        regex = re.compile(r'[0-9]+.\s[А-Яа-я0-9\-\s,.]+')
        text = regex.findall(str(tag))
        print(text)



parse_course_page(ONLINE_EDU_URL)


# 'ui-outputpanel ui-widget user-profile-view'
# 'ui-outputpanel ui-widget

"""
hrefs = re.findall('["\']https[A-Za-z0-9:/.]+["\']', response.text)
"""