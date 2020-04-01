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
from flask import Flask, request, render_template
from flask_script import Manager
import subprocess


# Enter parameters below:
# 1. Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)

client_id = 'XWYMcdcbRvMO24cyfSPq4Ual6L4lcULKdrwbX7V2'
client_secret = 'dU2oCp4vcyXDvfSelXbjqQEMmrSzOE0FBYrDHhe2o0SbdSZ0lxxvZ2369dCurTOE1MfkCWLL3H7duoB4H52VK2AdrFxwk3mv8tk1xm6RqIze0hHRkjrIHQZ3RB6LHLVU'
api_host = 'https://stepik.org'
'''
app1 = Flask(__name__)
@app1.route('/')
def form():
    number = request.form['number']
    return number
if __name__ == "__main__":
    app1.run(debug=True, host="127.0.0.10", port=1000)
'''
#number =
course_id = 10524 #main.number()
#print ("course_id:", course_id)
#mode = 'SAVE' # IMPORTANT: use SAVE first, then use PASTE with uncommented (or changed) lines above (client keys and host)

#cross_domain = True # to re-upload videos

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
'''
app1 = Flask(__name__)

@app1.route('/', methods=['GET', 'POST'])
def form():
    return render_template('index1.html')

@app1.route('/number', methods=['POST'])
def number():
    course_idi = request.form['number']
    template_context = dict(id=course_idi, course_title=course_title)
    return render_template('index.html', **template_context), course_idi
course_id = course_idi

if __name__ == "__main__":
    app1.run(debug=True, host="127.0.0.10", port=1000)
'''
course = fetch_object('course', course_id)
sections = fetch_objects('section', course['sections'])

#idd = course['id']
#course = { key: course[key] for key in ['title'] }

def print_course_id():
    id = str(course_id)
    return id

def print_course_title():
    tit = str(course['title'])
    return tit

def print_text():
    a = []
    #print('Вы ввели сourse ID:', course_id, "\nВаш курс:", course['title'], "\nВыберите пожалуйста интересующий раздел курса:")
    for section in sections:
        sec = section['title']
        a += [sec]
    myString = '\n'.join(a)
    #print(myString)
    return myString
print_text()

