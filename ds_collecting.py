"""
Version 1.0 (Coursera)
Site parcing by BeautifulSoup
"""

import requests
import re
from bs4 import BeautifulSoup


COURSERA_URL = 'https://ru.coursera.org'
COURSES = '/courses?page={}&index=prod_all_products_term_optimization'

# is used for testing
def get_html_and_save_to_file(url):
    response = requests.get(url)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
"""
def main():
    get_html_and_save_to_file(COURSERA_URL + COURSES)
"""


# This function return list of dictionries, that contains url and mark of course
# @args: url - url of specialization page
def parse_specialization_page(url):
    try:
        soup = BeautifulSoup(requests.get(COURSERA_URL + url).text, 'lxml')
    except:
        print('Error: project page {} not found'.format(url))
        return None

    data = []
    for tag in soup.find_all(class_=re.compile('CourseItem')):
        link = tag.find('a').get('href')
        mark = tag.find(class_=re.compile('rating-text')).next_element
        data.append({'course_link': link, 'course_mark': mark})

    return data
# end of function parse_specialization_page



# This function return parameters of course
# @args: url - url of course page
def parse_course_page(url):
    return 'values'
# end of function parse_course_page



# main function
def main():

    # get first page of course catalog
    """
    try:
        soup = BeautifulSoup(requests.get(COURSERA_URL + COURSES).text, 'lxml')
    except:
        print('Error: coursera don\'t reply')
        return
    """
    
    with open('index.html', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    for tag in soup.find_all('li', {'class': 'ais-InfiniteHits-item'}):
        link = tag.find('a').get('href')
        print(COURSERA_URL + link) # here must be method to parse course page

        mark = tag.find('span', {'class': 'ratings-text'})
        print(mark.next_element)

if __name__ == "__main__":
    main()

