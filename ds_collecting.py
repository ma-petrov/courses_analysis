import requests
import re

STEPIK_URL = "https://stepik.org/course/{}/promo"

def get_page_html(url):
    response = requests.get(url)
    if (response.status_code != 404):
        return response.text
    else:
        print('E: page {} does not exists'.format(url))
        return ''
"""
with open('course_list_html.txt', 'w') as f:
    for i in range(2000):
        f.write(get_page_html(STEPIK_URL.format(str(i))))
"""      

with open('course_list_html.txt', 'w') as f:
    get_page_html(STEPIK_URL.format(71439))
"""
hrefs = re.findall('["\']https[A-Za-z0-9:/.]+["\']', response.text)

with open('hrefs_list.txt', 'w') as f:
    for href in hrefs:
        f.write(href)
        f.write('\n')

with open('course_list_html.txt', 'w') as f:
    f.write(response.text)

requests.models.Response
"""