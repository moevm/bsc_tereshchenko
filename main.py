from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import my_second_version
import my_save_course_steps
from flask_script import Manager
from flask_migrate import Migrate

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '6251'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6251@localhost:5432/flask_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Courses, Sections, Units, Lessons


@app.route('/')
def index():
    return render_template('start_page.html', number=request.form.get('number'))  # , int(number)


@app.route('/frames', methods=['post', 'get'])
def frames():
    number = request.form.get('number')
    course_title = my_second_version.print_course_title(number)
    if db.session.query(Courses).filter_by(id=int(number)).scalar() is None:
        new_course = Courses(title=course_title, id=number)
        db.session.add(new_course)
        db.session.commit()
    return render_template('frames.html', id=number, course_title=course_title)


@app.route('/selection/<int:number>', methods=['post', 'get'])
def selection(number):
    razd = my_second_version.print_text(number)
    razd1 = razd.split('\n')
    for i in range(len(razd1)):
        if db.session.query(Sections).filter_by(course=number, position=i+1).first() is None:
            new_section = Sections(id=my_second_version.print_section_id(number, i),
                                   title=my_second_version.print_section_title(number, i),
                                   position=my_second_version.print_section_position(number, i),
                                   course=my_second_version.print_section_courseID(number, i))
            db.session.add(new_section)
            db.session.commit()
    # template_context = dict(id=number, course_title=course_title, razd=razd1)
    return render_template('selection_page.html', razd=enumerate(razd1), number=number)


@app.route('/text/<int:number>/<int:index>')
def text(number, index):
    razd = my_second_version.print_text(number)
    razd1 = razd.split('\n')
    # sec = razd1[index]
    # sections = db.session.query(Sections).filter_by(course=number, position=index).all()
    # print(sections[index].title)

    # my_save_course_steps.print_text_of_lesson(number, sec)

    # texts = Texts.query.filter_by(course_id=number, section=index)
    return render_template('text.html', razd=razd1, number=number, index=index)

    # units = db.query("SELECT * FROM unit WHERE course_id = $1 AND section_num = $2", [number, index])
    #
    # page = http.get(f"www.stepik.com/courses/{number}/sections/{index}")
    # units = xml.parser.parse(page) # xmlpath
    # return render_template('text.html', units=units)


if __name__ == "__main__":
    app.run(host="127.0.0.10", port=1000)  # debug=True

# def parse(number, index):
#    page = http.get(f"www.stepik.com/courses/{number}/sections/{index}")
#    units = xml.parser.parse(page) # xmlpath
#    db.query("INSERT INTO units (blah, blah, blah) VALUES $1", [units])
