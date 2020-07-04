import requests
import re

STEPIK_URL = "https://stepik.org/course/{}/promo"

with open('course_list_html.txt', 'w') as f:
    for i in range(2000):
        response = requests.get(STEPIK_URL.format(str(i)))
        if (response.status_code != 404):
            f.write(str(i)+'\n')
        else:
            print('E: page {} does not exists'.format(STEPIK_URL.format(str(i))))

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