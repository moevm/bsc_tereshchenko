from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import my_second_version
import my_save_course_steps
from flask_script import Manager
from flask_migrate import Migrate

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '6251'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vkr:vkr123@db:5432/vkr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Courses, Sections, Words


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


@app.route('/selection/<int:course_id>', methods=['post', 'get'])
def selection(course_id):
    sections = my_second_version.get_sections(course_id)
    for section in sections:
        if db.session.query(Sections).get(section['id']) is None:
            new_section = Sections(id=section['id'],
                                   title=section['title'],
                                   position=section['position'],
                                   course=course_id)
            db.session.add(new_section)
    db.session.commit()
    return render_template('selection_page.html', sections=sections)


@app.route('/text/<int:section_id>')
def text(section_id):
    # razd = my_second_version.print_text(course)
    # razd1 = razd.split('\n')

    section = db.session.query(Sections).get(section_id)

    words = db.session.query(Words).filter_by(section=section.id).all()
    if len(words) == 0:
        collected_words = my_second_version.get_words(section_id)
        words = []
        for word in collected_words:
            new_word = Words(word=word['word'],
                             section=section_id,
                             priority=word['priority'],
                             definition=word['definition'],
                             method=word['method'])
            db.session.add(new_word)
            words.append(new_word)
        db.session.commit()
    m1 = enumerate([word for word in words if word.method == 1])
    m2 = enumerate([word for word in words if word.method == 2])
    m3 = enumerate([word for word in words if word.method == 3])
    return render_template('text.html', razd=section.title, m1=m1, m2=m2, m3=m3)

    # units = db.query("SELECT * FROM unit WHERE course_id = $1 AND section_num = $2", [number, index])

    # page = http.get(f"www.stepik.com/courses/{number}/sections/{index}")
    # units = xml.parser.parse(page) # xmlpath
    # return render_template('text.html', units=units)

db.create_all()
db.session.commit()

if __name__ == "__main__":
    app.run(host="127.0.0.10", port=1000)  # debug=True

# def parse(number, index):
#    page = http.get(f"www.stepik.com/courses/{number}/sections/{index}")
#    units = xml.parser.parse(page) # xmlpath
#    db.query("INSERT INTO units (blah, blah, blah) VALUES $1", [units])
