from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class StudentForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    submit = SubmitField('Add Student')


class YearForm(FlaskForm):
    desc = StringField("School Year", validators=[DataRequired()])
    submit = SubmitField('Submit')


class ClassForm(FlaskForm):
    name = StringField("Class Name", validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    student_id = StringField("Student ID", validators=[DataRequired()])
    submit = SubmitField('Submit')


class QuizForm(FlaskForm):
    created_at = DateField('Date', format='%Y-%m-%d')
    grade = StringField("Grade", validators=[DataRequired()])
    class_id = StringField("Class ID", validators=[DataRequired()])
    submit = SubmitField('Submit')
