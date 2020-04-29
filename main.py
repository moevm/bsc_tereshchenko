from flask import Flask, request, render_template, flash
import my_second_version
import subprocess
from flask_script import Manager

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('start_page.html', number=request.form.get('number'))  # , int(number)


@app.route('/frames', methods=['post', 'get'])
def frames():
    number = request.form.get('number')
    course_title = my_second_version.print_course_title(number)
    return render_template('frames.html', id=number, course_title=course_title)


@app.route('/selection/<int:number>', methods=['post', 'get'])
def selection(number):
    razd = my_second_version.print_text(number)
    razd1 = razd.split('\n')
    # template_context = dict(id=number, course_title=course_title, razd=razd1)
    return render_template('selection_page.html', razd=enumerate(razd1), number=number)  # **template_context)


@app.route('/text/<int:number>/<int:index>')
def text(number, index):
    return render_template('text.html', index=index, number=number)


if __name__ == "__main__":
    app.run(host="127.0.0.10", debug=True, port=1000)  #
