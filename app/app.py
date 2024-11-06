import os
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3


app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret
wordCount = 200
DB_FILE="project.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT);")
c.execute("CREATE TABLE IF NOT EXISTS stories(name TEXT);")
c.execute("CREATE TABLE IF NOT EXISTS usertext(user TEXT, story TEXT, text TEXT);")

def length(a):
    return len(a) - len(a.replace(" ", ""))

@app.route("/")
#<<<<<<< HEAD:app/app.py
def homepage():
    if 'username' in session:
        return redirect(url_for("home"))

    return redirect(url_for("login"))
#=======
def disp_loginpage():
    return render_template( 'login.html' )
#>>>>>>> refs/remotes/origin/main:app.py

@app.route("/response.html" , methods=['POST'])
def register():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if(request.form.get('usernameL') != None):
        c.execute("SELECT * FROM users WHERE username="+"'"+request.form.get('usernameL')+"'"+";")
        user = c.fetchone()
        if(user[1] == request.form.get('passwordL')):
            session['username'] = user[0]
            return render_template( 'homePage.html',projectName = session['username'])
        else:
            return render_template('login.html')
    if(request.form.get('username') != None): #Only change username if it's not none
        c.execute("SELECT * FROM users WHERE username="+"'"+request.form.get('username')+"'"+";")
        user = c.fetchone()
        if(user == None):

            c.execute("INSERT INTO users(username,password) VALUES (?,?);", (request.form.get('username'),request.form.get('password')))

            db.commit()
            db.close()
            return render_template('login.html')
#<<<<<<< HEAD:app/app.py
#=======
#>>>>>>> refs/remotes/origin/main:app.py
@app.route('/createStories')
def create_story():
    pass
    #db = sqlite3.connect(DB_FILE)
    #c = db.cursor()
    #if(request.form.get('name') != None && request.form.get('text') != None):
    #    c.execute("INSERT INTO stories(name) VALUES (?);", (request.form.get('name')))
    #    c.execute("INSERT INTO usertext(user TEXT, story TEXT, text TEXT) VALUES (?,?,?);", (session['user'], request.form.get('name'), request.form.get('text')))

@app.route('/homepage')
def home():
    return render_template("homePage.html", projectName = "Land of Stories", description = "description")


def edit():
    text = request.form.get("text")
    if(length(text) < wordCount):
        c.execute("INSERT INTO usertext(user,story,text) VALUES (?,?,?);", (session['username'],session['story'] ,session['text']))

def display():
    c.execute("SELECT * FROM usertext WHERE story="+session['story']+";")
    #storyTex

@app.route("/login")
def login():
    return render_template("login.html", projectName="projectName PH")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('logout.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
