# Run with Python 3
# Saves all step texts from course into single HTML file.
import requests

# Enter parameters below:
# 1. Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)
client_id = 'XWYMcdcbRvMO24cyfSPq4Ual6L4lcULKdrwbX7V2'
client_secret = 'dU2oCp4vcyXDvfSelXbjqQEMmrSzOE0FBYrDHhe2o0SbdSZ0lxxvZ2369dCurTOE1MfkCWLL3H7duoB4H52VK2AdrFxwk3mv8tk1xm6RqIze0hHRkjrIHQZ3RB6LHLVU'
api_host = 'https://stepik.org'
course_id = 10524
sec = 'Введение'

# 2. Get a token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post('https://stepik.org/oauth2/token/',
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


def fetch_objects(obj_class, obj_ids, keep_order=True):
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
    if (keep_order):
        return sorted(objs, key=lambda x: obj_ids.index(x['id']))
    return objs

def print_text_of_lesson(course_id, sec):

    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])

    unit_ids = [unit for section in sections for unit in section['units'] if section['title'] == sec]
    units = fetch_objects('unit', unit_ids)

    lesson_ids = [unit['lesson'] for unit in units]
    lessons = fetch_objects('lesson', lesson_ids)

    step_ids = [step for lesson in lessons for step in lesson['steps']]
    steps = fetch_objects('step', step_ids)

    # for section in sections:

    # with open('text_of_section/course{}.html'.format(course_id), 'w', encoding='utf-8') as f:
    # sec_text =
    for step in steps:
        text = step['block']['text']
        url = '<a href="https://stepik.org/lesson/{}/step/{}">{}</a>' \
            .format(step['lesson'], step['position'], step['id'])
        # f.write('<h1>{}</h1>'.format(url))
        # f.write(text)
        # f.write('<hr>')
    return

# print_text_of_lesson(course_id, sec)
