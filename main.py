from flask import Flask, request, render_template
import my_second_version
import subprocess
from flask_script import Manager

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index1.html', number=request.form.get('number'))  # , int(number)

@app.route('/index', methods=['post', 'get'])
def index():
    number = request.form.get('number')
    course_title = my_second_version.print_course_title(number)
    razd = my_second_version.print_text(number)
    razd1 = razd.split('\n')
    # template_context = dict(id=number, course_title=course_title, razd=razd1)
    return render_template('index.html', id=number, course_title=course_title, razd=razd1)  # **template_context)

if __name__ == "__main__":
    app.run( host="127.0.0.10", port=1000) #debug=True,
