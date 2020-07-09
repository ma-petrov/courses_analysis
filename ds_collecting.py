import pandas as pd
import re
import requests
import lxml.html as html
from bs4 import BeautifulSoup

ONLINE_EDU_URL = 'https://online.edu.ru/public/course?faces-redirect=true&cid={}' # Example: 3476



def parse_course_page(page_html):
    soup = BeautifulSoup(page_html, 'lxml')

    for tag in soup.find_all(class_='ui-panelgrid ui-widget course-view-table rc-table-small'):
        regex = re.compile(r'[А-Яа-я0-9][А-Яа-я0-9\-\s,.]+')
        tag_list = regex.findall(str(tag))
    
    lections_cnt = 0
    is_native_lang = True
    duration_weeks = 0
    is_certified = False
    i = 0
    while i < len(tag_list) - 1:
        if (tag_list[i] == 'Количество лекций'):
            try:
                lections_cnt = int(tag_list[i + 1])
                i += 2
            except:
                lections_cnt = -1
                i += 1
        elif (tag_list[i] == 'Язык'):
            if (tag_list[i + 1] == 'Русский'):
                is_native_lang = True
            else:
                is_native_lang = False
            i += 2
        elif (tag_list[i] == 'Длительность'):
            try:
                duration_weeks = int((re.compile('[0-9]+').findall(tag_list[i + 1]))[0])
                i += 2
            except:
                duration_weeks = -1
                i += 1
        elif (tag_list[i] == 'Сертификат'):
            if (tag_list[i + 1] == 'Есть'):
                is_certified = True
            i += 2
        else:
            i += 1

    var_dict = {
        'lections_cnt': lections_cnt,
        'is_native_lang': is_native_lang,
        'duration_weeks': duration_weeks,
        'is_certified': is_certified
    }

    return var_dict

    
sample = []

i = 3500
while (i < 10000):
    page_num = str(i)
    response = requests.get(ONLINE_EDU_URL.format(page_num))
    if (response.status_code != 404):
        var_dict = {'id': i}
        var_dict.update(parse_course_page(response.text))
        sample.append(var_dict)
        print(var_dict)
    i += 1

df = pd.DataFrame(sample)
df.to_csv('sample.csv')


# 'ui-panelgrid ui-widget course-view-table rc-table-small'
# 'ui-outputpanel ui-widget user-profile-view'
# 'ui-outputpanel ui-widget

"""
hrefs = re.findall('["\']https[A-Za-z0-9:/.]+["\']', response.text)
"""