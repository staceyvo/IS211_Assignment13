import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from wtforms import Form, validators, StringField, PasswordField


app = Flask(__name__)

class LoginForm(Form):
    #create a login form
    username = StringField(u'Username', [validators.required(), validators.length(max=100)])
    password = PasswordField(u'Password', [validators.required(), validators.length(max=100)])

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
    if request.method == 'POST':
        if LoginForm(request.form).validate():
            username, password = request.form['username'], request.form['password']
            if (username, password) == ('admin', 'password'):
                session['username'] = request.form['username']
                return redirect(url_for('/'))
    return render_template('loggins', my_form=LoginForm())



@app.route('/create_database')
def create_database():
    con = sqlite3.connect('hw13.db')
    cur = con.cursor()
    with open('schema.sql') as fp:
        cur.executescript(fp.read())


if __name__ == '__main__':
    app.run(host='localhost')
