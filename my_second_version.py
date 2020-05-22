# Run with Python 3
# Clone course from one Stepik instance (domain) into another
import re
import os
import csv
import ast
import json
import requests
import datetime
import main
import collections
import stanfordnlp
import pke

# Enter parameters below:
# 1. Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)

client_id = 'XWYMcdcbRvMO24cyfSPq4Ual6L4lcULKdrwbX7V2'
client_secret = 'dU2oCp4vcyXDvfSelXbjqQEMmrSzOE0FBYrDHhe2o0SbdSZ0lxxvZ2369dCurTOE1MfkCWLL3H7duoB4H52VK2AdrFxwk3mv8tk1xm6RqIze0hHRkjrIHQZ3RB6LHLVU'
api_host = 'https://stepik.org'

course_id = 10524
sec_id = 1
# mode = 'SAVE' # IMPORTANT: use SAVE first, then use PASTE with uncommented (or changed) lines above (client keys and host)

# cross_domain = True # to re-upload videos

# 2. Get a token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post('{}/oauth2/token/'.format(api_host),
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
token = response.json().get('access_token', None)
if not token:
    print('Unable to authorize with provided credentials')
    exit(1)


# 3. Call API (https://stepik.org/api/docs/) using this token.
def fetch_object(obj_class, obj_id):
    api_url = '{}/api/{}s/{}'.format(api_host, obj_class, obj_id)
    response = requests.get(api_url,
                            headers={'Authorization': 'Bearer ' + token}).json()
    return response['{}s'.format(obj_class)][0]


def fetch_objects(obj_class, obj_ids):
    objs = []
    # Fetch objects by 30 items,
    # so we won't bump into HTTP request length limits
    step_size = 30
    for i in range(0, len(obj_ids), step_size):
        obj_ids_slice = obj_ids[i:i + step_size]
        api_url = '{}/api/{}s?{}'.format(api_host, obj_class,
                                         '&'.join('ids[]={}'.format(obj_id)
                                                  for obj_id in obj_ids_slice))
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + token}
                                ).json()

        objs += response['{}s'.format(obj_class)]
    return objs


course = fetch_object('course', course_id)
sections = fetch_objects('section', course['sections'])

# idd = course['id']
# course = { key: course[key] for key in ['title'] }

#------------- course -------------

def print_course_id(course_id):
    id = str(course_id)
    return id


def print_course_title(course_id):
    course = fetch_object('course', course_id)
    tit = str(course['title'])
    return tit


def print_text(course_id):
    a = []
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    for section in sections:
        sec = section['title']
        # id = str(section['id'])
        a += [sec]
        # a += [id]
    myString = '\n'.join(a)
    return myString

#------------- section -------------

def print_section_id(course_id, index): # id = index + 1
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    for i, section in enumerate(sections):
        if i == index:
            sec_id = section['id']
            return sec_id

def print_section_title(course_id, index):
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    for i, section in enumerate(sections):
        if i == index:
            sec_tit = section['title']
            return sec_tit

def print_section_position(course_id, index):
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    for i, section in enumerate(sections):
        if i == index:
            sec_pos = section['position']
            return sec_pos

def print_section_courseID(course_id, index):
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    for i, section in enumerate(sections):
        if i == index:
            sec_course = section['course']
            return sec_course

#------------- unit -------------

def print_unit_id(course_id, index): # id = index + 1
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    unit_ids = [unit for section in sections for unit in section['units']]
    units = fetch_objects('unit', unit_ids)
    for i, unit in enumerate(units):
        if i == index:
            unit_id = unit['id']
            return unit_id

def print_unit_position(course_id, index): # id = index + 1
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    unit_ids = [unit for section in sections for unit in section['units']]
    units = fetch_objects('unit', unit_ids)
    for i, unit in enumerate(units):
        if i == index:
            unit_pos = unit['position']
            return unit_pos

def print_unit_section(course_id, index): # id = index + 1
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    unit_ids = [unit for section in sections for unit in section['units']]
    units = fetch_objects('unit', unit_ids)
    for i, section in enumerate(sections):
        if i == index:
            unit_sec = section['section']
            return unit_sec

def print_unit_lesson(course_id, index): # id = index + 1
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    unit_ids = [unit for section in sections for unit in section['units']]
    units = fetch_objects('unit', unit_ids)
    for i, section in enumerate(sections):
        if i == index:
            unit_les = section['lesson']
            return unit_les

#------------- lesson -------------

def print_lesson_id(course_id, index): # id = index + 1
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    unit_ids = [unit for section in sections for unit in section['units']]
    units = fetch_objects('unit', unit_ids)
    lesson_ids = [unit['lesson'] for unit in units]
    lessons = fetch_objects('lesson', lesson_ids)
    for i, lesson in enumerate(lessons):
        if i == index:
            les_id = lesson['id']
            return les_id

def print_lesson_title(course_id, index): # id = index + 1
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    unit_ids = [unit for section in sections for unit in section['units']]
    units = fetch_objects('unit', unit_ids)
    lesson_ids = [unit['lesson'] for unit in units]
    lessons = fetch_objects('lesson', lesson_ids)
    for i, lesson in enumerate(lessons):
        if i == index:
            les_tit = lesson['title']
            return les_tit

def get_sections(course_id):
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])
    return sections

html_cleaner = re.compile(r'<[^>]+>')
word_finder = re.compile(r'\w+')

def get_words(section_id):
    unit_ids = fetch_object('section', section_id)['units']
    units = fetch_objects('unit', unit_ids)
    lesson_ids = [unit['lesson'] for unit in units]
    lessons = fetch_objects('lesson', lesson_ids)
    step_ids = [step for lesson in lessons for step in lesson['steps']]
    steps = fetch_objects('step', step_ids)
    all_words = []
    for step in steps:
        if step['block']['name'] == 'text':
            text = html_cleaner.sub('', step['block']['text'])
            words = word_finder.findall(text)
            words = [word for word in words if len(word) > 3]
            words = [word.lower() for word in words]
            all_words += words
        if step['block']['name'] == 'video':
            # Заглушка для скачивания видео и его анализа
            pass

    all_words = [word for word in all_words if word not in pke.utils.stopwords.words()]

    wiki_cache = {}

    method1_words = []
    for word, priority in collections.Counter(all_words).most_common():
        if len(method1_words) >= 10:
            break
        response = requests.get('https://ru.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=' + word).json()
        wiki_page = list(response['query']['pages'].values())[0]
        if 'extract' in wiki_page:
            method1_words.append({
                'word': word,
                'priority': priority,
                'definition': wiki_page['extract'],
                'method': 1,
            })
            wiki_cache[word] = wiki_page['extract']

    extractor = pke.unsupervised.TopicRank()
    extractor.load_document("\n".join(all_words), language='ru')
    extractor.candidate_selection()
    extractor.candidate_weighting()

    method2_words = []
    for word, priority in extractor.get_n_best(-1):
        if len(method2_words) >= 10:
            break
        if word in wiki_cache:
            method2_words.append({
                'word': word,
                'priority': priority,
                'definition': wiki_cache[word],
                'method': 2
            })
            continue
        response = requests.get('https://ru.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=' + word).json()
        wiki_page = list(response['query']['pages'].values())[0]
        if 'extract' in wiki_page:
            method2_words.append({
                'word': word,
                'priority': priority,
                'definition': wiki_page['extract'],
                'method': 2,
            })
            wiki_cache[word] = wiki_page['extract']

    extractor = pke.unsupervised.TextRank()
    extractor.load_document("\n".join(all_words), language='ru')
    extractor.candidate_selection()
    extractor.candidate_weighting()

    method3_words = []
    for word, priority in extractor.get_n_best(-1):
        if len(method3_words) >= 10:
            break
        if word in wiki_cache:
            method3_words.append({
                'word': word,
                'priority': priority,
                'definition': wiki_cache[word],
                'method': 2
            })
            continue
        response = requests.get('https://ru.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=' + word).json()
        wiki_page = list(response['query']['pages'].values())[0]
        if 'extract' in wiki_page:
            method3_words.append({
                'word': word,
                'priority': priority,
                'definition': wiki_page['extract'],
                'method': 3,
            })
            wiki_cache[word] = wiki_page['extract']

    return method1_words + method2_words + method3_words

