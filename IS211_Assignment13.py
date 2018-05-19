import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from wtforms import Form, validators, StringField, PasswordField


app = Flask(__name__)
app.secret_key = 'Footloose'

class LoginForm(Form):
    #create a login form
    username = StringField(u'Username', [validators.required(), validators.length(max=100)])
    password = PasswordField(u'Password', [validators.required(), validators.length(max=100)])

class Add_Student(Form):
    # add student information
    FirstName = StringField(u'FirstName', [validators.required(), validators.length(max=100)])
    LastName = StringField(u'LastName', [validators.required(), validators.length(max=100)])


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
            return redirect(url_for('dashboard'))
    return render_template('loggins.html', my_form=LoginForm(), error=error)


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
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
    error = None

    if request.method == 'POST':
        if Add_Student(request.form).validate():
            con = sqlite3.connect('hw13.db')
            cur = con.cursor()
            cur.execute('INSERT INTO Students VALUES(?,?)', (request.form['FirstName'], request.form['LastName']))
            con.commit()
            con.close()
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Input')
    return render_template('playing_with_the_boys.html', my_form=Add_Student(), error=error)


@app.route('/create_database')
def create_database():
    con = sqlite3.connect('hw13.db')
    cur = con.cursor()
    with open('schema.sql') as fp:
        cur.executescript(fp.read())


if __name__ == '__main__':
    app.run(host='localhost')
