import requests

OPENEDU_URL = "https://openedu.ru/course/"

response = requests.get(OPENEDU_URL)

with open('course_list_html.txt', 'w') as f:
    if (f.write(response.text)):
        print('log (i): html is writed to file')
    else:
        print('log (e): writing html to file error')