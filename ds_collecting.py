"""
Version 1.1 (Coursera)
Site parcing by BeautifulSoup

Added parameters to dataset
"""

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

COURSERA_URL = 'https://ru.coursera.org'
CATALOG_PAGE = '/courses?page={}&index=prod_all_products_term_optimization'

def parse_specialization_page(url):
    """
    Returns list of course page urls
    Params:
    url - url of specialization page
    """
    try:
        response = requests.get(COURSERA_URL + url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
    except:
        print('Error: project page {} not found'.format(url))
        return None

    data = []
    for tag in soup.find_all(class_=re.compile('CourseItem')):
        data.append(tag.find('a').get('href'))

    return data



def parse_course_page(url):
    """
    Returns dictionriy with parameters of course
    Params:
    url - url of course page
    """
    # dataset variables:
    TITLE = 'title'
    URL = 'url'
    RATING = 'rate'
    TEACHER_RATING = 'teach_rate'
    NEW_CARRIER = 'new_car'
    TAKE_ADVANTAGES = 'advent'
    EARN_MORE = 'earn_more'
    LEVEL = 'level'
    LANGUAGE = 'lang'
    EXEC_TIME = 'exec_time'
    CHAPTERS_CNT = 'chap_cnt'
    COURSE_DUR = 'course_dur'
    CHAP_AVG_DUR = 'chap_avg_dur'
    EDU_NAME = 'edu_name'

    work = {
        'начал новую карьеру, пройдя эти курсы': NEW_CARRIER,
        'получил значимые преимущества в карьере благодаря этому курсу': TAKE_ADVANTAGES,
        'стал больше зарабатывать или получил повышение': EARN_MORE
    }

    levels = {
        'Начальный уровень': 1,
        'Промежуточный уровень': 2,
        'Продвинутый уровень': 3
    }

    languages = {
        'Русский': 1,
        'Английский': 2
    }

    try:
        response = requests.get(COURSERA_URL + url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
    except:
        print('Error: course page {} not found'.format(url))
        return None

    # data structure of sample
    data = {
        TITLE: '',
        URL: COURSERA_URL + url,
        RATING: None,
        TEACHER_RATING: None,
        NEW_CARRIER: None,
        TAKE_ADVANTAGES: None,
        EARN_MORE: None,
        LEVEL:None,
        LANGUAGE: None,
        EXEC_TIME: None,
        CHAPTERS_CNT: None,
        COURSE_DUR: None,
        CHAP_AVG_DUR: None,
        EDU_NAME: None
    }
    
    # Collecting course title
    data.update({TITLE: soup.find('h1', {'class': 'banner-title m-b-0 banner-title-without--subtitle'}).next_element})

    # Collecting course rating
    try:
        rating = 'empty-rating'
        rating = soup.find('span', class_=re.compile('number-rating')).next_element
        data.update({RATING: float(rating)})
    except:
        print('Error: cant convert value {} to float'.format(rating))

    # Collecting teacher rating
    try:
        rating_sum = 0
        rating_cnt = 0
        rating_value = 'empty'
        for rating in soup.find_all('span', class_='avg-instructor-rating__total'):
            rating_value = rating.find('span').next_element
            num_list = re.findall(r'[0-9]+[.,][0-9]+', rating_value)
            rating_sum += float(num_list[0])
            rating_cnt += 1        
        data.update({TEACHER_RATING: rating_sum/rating_cnt})
    except:
        print('Error: cant convert value {} to float'.format(rating_value))


    # Collecting NEW_CARRIER, TAKE_ADVANTAGES, EARN_MORE variables
    for tag in soup.find_all('div', {'class': '_1k3yl1y'}):
        param = tag.find('div', class_='font-sm').next_element
        value = tag.find('h2').next_element
        try:
            if param in work.keys():
                data.update({work.get(param): float(value)})
        except:
            print('Error: cant convert value {} to float'.format(value))

    # Collecting LEVEL, LANGUAGE, EXEC_TIME 
    tags = soup.find('div', {'class': 'ProductGlance _9cam1z p-t-2'})
    for tag in tags.find_all(class_=re.compile('_16ni8zai')):
        element = tag.next_element
        # If tag is about level
        if element in levels.keys():
            data.update({LEVEL: levels.get(element)})
        # If tag is about language
        if element in languages.keys():
            data.update({LANGUAGE: languages.get(element)})
        # If tag is about execution time:
        try:
            if re.match(r'Прибл.\s[0-9]+\s(ча(с|а|ов)|недел[иья])', element):
                try:
                    time = int(re.findall(r'[0-9]+', element))
                    if element == re.compile(r'недел[иья]'):
                        data.update({EXEC_TIME: 168*time})
                    elif element == re.compile(r'ча(с|а|ов)'):
                        data.update({EXEC_TIME: time})
                    else:
                        print('Unknown time')
                except:
                    print('Error: cant convert {} to int number from string'.format(element))
        except:
            pass
        
    # Chapters quantity is length of chapter description tag list
    tags = soup.find_all(class_='_jyhj5r SyllabusWeek')
    chapters_cnt = len(tags)
    data.update({CHAPTERS_CNT: chapters_cnt})
    # Collecting course and chapter estimated duration time 
    course_dur = 0 # minutes
    chap_avg_dur = 0 # minutes
    for tag in tags:
        element = tag.find('div', {'data-test': 'duration-text-section'}).find('span').next_element
        try:
            time = int((re.findall(r'[0-9]+', element))[0])
        except:
            time = 0
            print('Error: cant convert number to int from string {}'.format(element))
        
        if re.match(r'[0-9]+\sминут', element):
            course_dur += time
        elif re.match(r'[0-9]+\sч\.', element):
            course_dur += 60*time

    if chapters_cnt > 0:
        chap_avg_dur = course_dur/chapters_cnt

    # Coolecting university name
    tag = soup.find('h4', class_='headline-4-text bold rc-Partner__title')
    try:
        data.update({EDU_NAME: tag.next_element})
    except:
        print('Error: cant find university name')

    data.update({COURSE_DUR: course_dur, CHAP_AVG_DUR: chap_avg_dur})
    
    return data



# main function
def main():

    # list of courses sample
    sample = []

    # Gettig first page of course catalog
    for i in range(45):
        print('loop:'+str(i+1))
        # Gettig soup object of courses catalog page
        try:
            response = requests.get(COURSERA_URL + CATALOG_PAGE.format(i+1))
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
        except:
            print('Error: page {} dont reply'.format(CATALOG_PAGE.format(i+1)))
            return
        
        # Collecting tags with links to courses of specializations pages and calling parsing functions for them
        for tag in soup.find_all('li', class_='ais-InfiniteHits-item'):
            url = tag.find('a').get('href')
            card_info = tag.find(class_='card-info vertical-box')
            page_type = card_info.find(class_='_jen3vs _1d8rgfy3').next_element
            
            if page_type == 'Курс':
                # Calling course page parsing function by link in tag 'a':
                # If parse_course_page is unseccessful it will return None
                # If successful - data would updated with course vars and would inserted into sample
                data = parse_course_page(url)
                if data != None:
                    sample.append(data)

            elif page_type == 'Специализация':
                # Calling specialization page parsing function and collecting corse links
                # Then calling course page parsing function by links in courses list
                courses = parse_specialization_page(url)
                if courses != None:
                    for course in courses:
                        data = parse_course_page(course)
                        if data != None:
                            sample.append(data)

            else:
                # Not usable, only pass
                pass

    df = pd.DataFrame(sample)
    df.to_csv('sample.csv')
            


if __name__ == "__main__":
    main()