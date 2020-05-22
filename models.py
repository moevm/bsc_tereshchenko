from main import db


class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    list_sections = db.relationship('Sections', backref='courses', primaryjoin="Courses.id==Sections.course")

    # c.list_sections, где с - объект класса Courses, выдаст все разделы курса
    # s.courses, где s - объект класса Sections, выдаст id курса

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title)


class Sections(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer(), nullable=False)
    course = db.Column(db.Integer(), db.ForeignKey('courses.id'), nullable=False)

    # строчное представление объекта
    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.title)

# class Lessons(db.Model):
#     __tablename__ = 'lessons'
#     id = db.Column(db.Integer(), nullable=False, primary_key=True)
#     title = db.Column(db.Integer(), nullable=False)
#     content = db.Column(db.Text(), nullable=False)

# class Units(db.Model):
#     __tablename__ = 'units'
#     id = db.Column(db.Integer(), nullable=False, primary_key=True)
#     position = db.Column(db.Integer(), nullable=False)
#     section = db.Column(db.Integer(), db.ForeignKey('sections.id'), nullable=False)
#     lesson = db.Column(db.Integer(), db.ForeignKey('lesson.id'), nullable=False)
#     # lessonID = db.relationship('Lessons', backref='unitID', primaryjoin="Units.lesson==Lessons.id", uselist=False)

# def parse(number, index):
#    page = http.get(f"www.stepik.com/courses/{number}/sections/{index}")
#    units = xml.parser.parse(page) # xmlpath
#    db.query("INSERT INTO units (blah, blah, blah) VALUES $1", [units])

class Words(db.Model):
    __tablename__ = 'words'
    section = db.Column(db.Integer(), db.ForeignKey('sections.id'), primary_key=True, nullable=False)
    method = db.Column(db.Integer(), primary_key=True, nullable=False)
    word = db.Column(db.Text(), primary_key=True, nullable=False)
    definition = db.Column(db.Text())
    priority = db.Column(db.Float())
