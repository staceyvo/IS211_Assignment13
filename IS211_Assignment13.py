import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from wtforms import Form, validators, StringField, PasswordField, DateField, SelectField

app = Flask(__name__)
app.secret_key = 'Footloose'


class LoginForm(Form):
    # create a login form
    username = StringField(u'Username', [validators.required(), validators.length(max=100)])
    password = PasswordField(u'Password', [validators.required(), validators.length(max=100)])


class Add_Student(Form):
    # add student information
    FirstName = StringField(u'FirstName', [validators.required(), validators.length(max=100)])
    LastName = StringField(u'LastName', [validators.required(), validators.length(max=100)])


class Add_Quiz(Form):
    # add student information
    Quiz_Name = StringField(u'Quiz_Name', [validators.required(), validators.length(max=100)])
    Question_Number = StringField(u'Question_Number', [validators.required(), validators.length(max=100)])
    Quiz_Date = DateField(u'Quiz_Date', [validators.required()], format='%Y-%m-%d')


class Add_Result(Form):
    # add quiz result
    con = sqlite3.connect('hw13.db')
    cur = con.cursor()
    cur.execute('SELECT FirstName, LastName, Student_ID FROM Students')
    students = cur.fetchall()
    student = SelectField(u'Student', choices=[
        (student[2], student[0] + ' ' + student[1]) for student in students
    ], validators=[validators.required()])

    quizzes = cur.execute('SELECT Quiz_Name, Quiz_ID FROM Quizzes').fetchall()
    quiz = SelectField(u'Quiz', choices=[
        (quiz[1], quiz[0]) for quiz in quizzes], validators=[validators.required()])
    grade = StringField(u'Grade', [validators.required(), validators.length(max=3)])


@app.route('/', methods=['GET'])
def home_route():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
               "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + \
           "click here to log in</b></a>"


@app.route('/login', methods=['POST', 'GET'])
def login():
    # entering the danger zone
    error = None

    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                        request.form['password'] != 'password':
            error = 'Invalid username or password. Please try again!'
        else:
            flash('You were successfully logged in')
            session['username'] = 'admin'
            return redirect(url_for('dashboard'))
    return render_template('login.html', my_form=LoginForm(), error=error)


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    # fetch data
    # execute query
    con = sqlite3.connect('hw13.db')
    cur = con.cursor()

    # process result
    students = cur.execute('SELECT * FROM Students').fetchall()
    quizzes = cur.execute('SELECT * FROM Quizzes').fetchall()
    con.close()

    # return template with added data
    return render_template('dashboard.html', students=students, quizzes=quizzes)


@app.route('/student/add', methods=['POST', 'GET'])
def add_student():
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None

    if request.method == 'POST':
        if Add_Student(request.form).validate():
            con = sqlite3.connect('hw13.db')
            cur = con.cursor()
            cur.execute('INSERT INTO Students VALUES(?,?,?)',
                        (request.form['FirstName'], request.form['LastName'], None))
            con.commit()
            con.close()
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Input')
    return render_template('add_student.html', my_form=Add_Student(), error=error)


@app.route('/quiz/add', methods=['POST', 'GET'])
def add_quiz():
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None

    if request.method == 'POST':
        if Add_Quiz(request.form).validate():
            con = sqlite3.connect('hw13.db')
            cur = con.cursor()
            cur.execute('INSERT INTO Quizzes VALUES(?,?,?,?)',
                        (None, request.form['Quiz_Name'], request.form['Question_Number'], request.form['Quiz_Date']))
            con.commit()
            con.close()
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Input')
    return render_template('add_quiz.html', my_form=Add_Quiz(), error=error)


@app.route('/results/add', methods=['POST', 'GET'])
def add_result():
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None

    if request.method == 'POST':
        con = sqlite3.connect('hw13.db')
        cur = con.cursor()
        cur.execute('INSERT INTO Results ("Grade", "Quiz_ID", "Student_ID") VALUES (?,?,?)',
                    (request.form['grade'], request.form['quiz'], request.form['student']))
        con.commit()
        con.close()

    my_form = Add_Result()
    return render_template('add_results.html', my_form=my_form, error=error)


@app.route('/student/<id>')
def student_id(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    con = sqlite3.connect('hw13.db')
    cur = con.cursor()
    id_query = cur.execute(
        'SELECT Quizzes.Quiz_Name, Results.Grade FROM Results JOIN Quizzes ON Results.Quiz_ID = Quizzes.Quiz_ID WHERE Student_ID = ?',
        id).fetchall()
    con.close()
    return render_template('student_id.html', data=id_query)


@app.route('/create_database')
def create_database():
    if 'username' not in session:
        return redirect(url_for('login'))

    con = sqlite3.connect('hw13.db')
    cur = con.cursor()
    with open('schema.sql') as fp:
        cur.executescript(fp.read())
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='localhost')
