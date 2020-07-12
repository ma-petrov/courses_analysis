"""
Version 1.0 (Coursera)
Site parcing by BeautifulSoup
"""

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


COURSERA_URL = 'https://ru.coursera.org'
CATALOG_PAGE = '/courses?page={}&index=prod_all_products_term_optimization'

# dataset variables:
TITLE = 'TITLE'
RATING = 'RATING'
VAR_1 = 'VAR_1'
VAR_2 = 'VAR_2'
VAR_3 = 'VAR_3'

# is used for testing
def get_html_and_save_to_file(url):
    response = requests.get(url)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
"""
def main():
    get_html_and_save_to_file(COURSERA_URL + COURSES)
"""



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

    PARAM_1 = 'начал новую карьеру, пройдя эти курсы'
    PARAM_2 = 'получил значимые преимущества в карьере благодаря этому курсу'
    PARAM_3 = 'стал больше зарабатывать или получил повышение'
    param_dict = {PARAM_1: VAR_1, PARAM_2: VAR_2, PARAM_3: VAR_3}

    try:
        response = requests.get(COURSERA_URL + url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
    except:
        print('Error: course page {} not found'.format(url))
        return None

    data = {TITLE: '', RATING: None, VAR_1: None, VAR_2: None, VAR_3: None}
    
    data.update({TITLE: soup.find('h1', {'class': 'banner-title m-b-0 banner-title-without--subtitle'}).next_element})

    try:
        rating = 'empty-rating'
        rating = soup.find('span', {'class': '_16ni8zai m-b-0 rating-text number-rating number-rating-expertise'}).next_element
        data.update({RATING: float(rating)})
    except:
        print('Error: cant convert value {} to float'.format(rating))

    for tag in soup.find_all('div', class_='_1k3yl1y'):
        param = tag.find('div', class_='font-sm').next_element
        value = tag.find('h2').next_element
        try:
            if param in param_dict.keys():
                data.update({param_dict.get(param): float(value)})
        except:
            print('Error: cant convert value {} to float'.format(value))

    return data



# main function
def main():

    # list of courses sample
    sample = []

    # get first page of course catalog
    for i in range(1):
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

            data = {TITLE: '', RATING: None, VAR_1: None, VAR_2: None, VAR_3: None}
            
            if page_type == 'Курс':
                # Calling course page parsing function by link in tag 'a':
                # If parse_course_page is unseccessful it will return None
                # If successful - data would updated with course vars and would inserted into sample
                course_vars = parse_course_page(url)
                if course_vars != None:
                    data.update(course_vars)
                    sample.append(data)

            elif page_type == 'Специализация':
                # Calling specialization page parsing function and collecting corse links
                # Then calling course page parsing function by links in courses list
                courses = parse_specialization_page(url)
                if courses != None:
                    for course in courses:
                        course_vars = parse_course_page(course)
                        if course_vars != None: 
                            data.update(course_vars)
                            sample.append(data)

            else:
                # Not usable, only pass
                pass

    df = pd.DataFrame(sample)
    df.to_csv('sample.csv')
            


if __name__ == "__main__":
    main()

