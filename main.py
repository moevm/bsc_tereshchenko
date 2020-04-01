from flask import Flask, request, render_template
import my_second_version
import subprocess
from flask_script import Manager
from typing import Any

app = Flask(__name__)

'''
@app.route('/')
def index():
    name, age, profession = "Jerry", 24, 'Programmer'
    template_context = dict(name=name, age=age, profession=profession)
    return render_template('index.html', **template_context)
    
@app.route('/run')
def index():
    course_id, course_title = my_second_version.print_course_id(), my_second_version.print_course_title()
    
    return my_second_version.print_text()


class CourseForm(Form):
    num = NumberField('First name', [validators.Length(min=5, max=30)])
    #last_name = StringField('Last name', [validators.Length(min=5, max=30)])
'''

@app.route('/')
def form():
    #number = request.form.get('number')
    return render_template('index1.html', number=request.form.get('number'))#, int(number)

#num = request.form.get('number')
#print (num)
'''
@app.route('/number', methods=['post', 'get'])
def number():
    number = request.form.get('number')
    #return number
    return int(number)
'''


@app.route('/index', methods=['post', 'get'])
def index():
    number = request.form.get('number')
    course_id = number
    course_title = my_second_version.print_course_title()
    '''my_second_version.print_course_id(),'''
    razd = my_second_version.print_text()
    razd1 = razd.split('\n')
    # template_context = dict(id=number, course_title=course_title, razd=razd1)
    return render_template('index.html', id=number, course_title=course_title)  # **template_context)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.10", port=1000)
