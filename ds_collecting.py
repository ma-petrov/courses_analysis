import requests
import re

OPENEDU_URL = "https://openedu.ru/course/"

response = requests.get(OPENEDU_URL)

hrefs = re.findall('href="[A-Za-z0-9:/.]+"', response.text)

with open('hrefs_list.txt', 'w') as f:
    for href in hrefs:
        f.write(href)
        f.write('\n')

with open('course_list_html.txt', 'w') as f:
    f.write(response.text)