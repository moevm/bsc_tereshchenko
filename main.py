from flask import Flask, request, render_template
import my_second_version
import my_save_course_steps
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
    razd = my_second_version.print_text(number)
    razd1 = razd.split('\n')
    sec = razd1[index]
    my_save_course_steps.print_text_of_lesson(number, sec)
    return render_template('text.html', razd=razd1, number=number, index=index)


    #units = db.query("SELECT * FROM unit WHERE course_id = $1 AND section_num = $2", [number, index])
    #
    # page = http.get(f"www.stepik.com/courses/{number}/sections/{index}")
    # units = xml.parser.parse(page) # xmlpath
    # return render_template('text.html', units=units)


if __name__ == "__main__":
    app.run(host="127.0.0.10", debug=True, port=1000)  #

#def parse(number, index):
#    page = http.get(f"www.stepik.com/courses/{number}/sections/{index}")
#    units = xml.parser.parse(page) # xmlpath
#    db.query("INSERT INTO units (blah, blah, blah) VALUES $1", [units])