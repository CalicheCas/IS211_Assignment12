from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(15), index=True, unique=True, nullable=False)

    def __repr__(self):
        return '<Year {}>'.format(self.desc)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))

    def __repr__(self):
        return '<Student {} {}>'.format(self.first_name, self.last_name)


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return '<Class {} -  Subject {}>'.format(self.name, self.subject)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, index=True)
    grade = db.Column(db.String(4), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))

    def __repr__(self):
        return '<Quiz: TimeStamp {} - Grade {} - ClassId {}>'.format(self.created_at, self.grade, self.class_id)
