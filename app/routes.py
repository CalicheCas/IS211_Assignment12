from flask import render_template, flash, redirect, url_for, request, current_app
from app import app, db
from app.forms import LoginForm, RegistrationForm, StudentForm, YearForm, ClassForm, QuizForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Student, Year, Class, Quiz
from werkzeug.urls import url_parse
import sqlalchemy


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    app.logger.error("Rendering index")
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            app.logger.error("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        app.logger.error("User {} has been registered.".format(user))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/student', methods=['GET', 'POST'])
@login_required
def student():
    form = StudentForm()
    # years = ['Freshman', 'Sophomore', 'Junior', 'Senior']
    app.logger.info('test')

    if form.validate_on_submit():
        fname = form.firstname.data
        lname = form.firstname.data
        year_id = form.year.data

        db.session.add(Student(first_name=fname, last_name=lname, year_id=int(year_id)))
        db.session.commit()

    students = Student.query.all()

    return render_template('student.html', title='Students', form=form, students=students)


@login_required
@app.route('/year', methods=['GET', 'POST'])
def year():

    form = YearForm()
    if form.validate_on_submit():
        desc = form.desc.data
        db.session.add(Year(desc=desc))
        db.session.commit()

    years = Year.query.all()
    return render_template('year.html', Title='Year', form=form, years=years)


@login_required
@app.route('/class', methods=['GET', 'POST'])
def classes():

    form = ClassForm()
    if form.validate_on_submit():
        name = form.name.data
        subject = form.subject.data
        student_id = form.student_id.data

        db.session.add(Class(name=name, subject=subject, student_id=int(student_id)))
        db.session.commit()
    c = Class.query.all()

    return render_template('class.html', Title='Classes', form=form, classes=c)


@login_required
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():

    form = QuizForm()
    if form.validate_on_submit():
        date = form.created_at.data
        print(type(date))

        grade = form.grade.data
        print(type(grade))
        class_id = form.class_id.data
        print(type(class_id))
        db.session.add(Quiz(created_at=date, grade=str(grade), class_id=int(class_id)))
        db.session.commit()
    quizzes = Quiz.query.all()
    print(quizzes)

    return render_template('quiz.html', Title='Quizzes', form=form, quizzes=quizzes)


@login_required
@app.route('/result', methods=['GET'])
def results():

    sql = sqlalchemy.text('''SELECT st.first_name, st.last_name, y.desc, c.name, q.grade FROM Student st LEFT 
                        JOIN Year y ON st.year_id = y.id LEFT JOIN Class c ON c.student_id = st.id 
                        LEFT JOIN Quiz q ON q.class_id = c.id''')

    r = db.engine.execute(sql).fetchall()

    return render_template('result.html', Title='Results', results=r)
