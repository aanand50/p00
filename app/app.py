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
<<<<<<< HEAD:app/app.py
def homepage():
    if 'username' in session:
        return redirect("/response.html")
    return redirect(url_for("login"))
=======
def disp_loginpage():
    return render_template( 'login.html' )
>>>>>>> refs/remotes/origin/main:app.py

@app.route("/response.html" , methods=['POST'])
def register():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username="+"'"+request.form.get('username')+"'"+";")
    user = c.fetchone()
    if(user != None and request.form.get('password') == 
    if(request.form.get('username') != None and user == None): #Only change username if it's not none
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')

        c.execute("INSERT INTO users(username,password) VALUES (?,?);", (session['username'],session['password']))

        db.commit()
        db.close()
<<<<<<< HEAD:app/app.py

    return render_template( 'response.html', username = session['username'])
=======
    return render_template( 'homePage.html')
>>>>>>> refs/remotes/origin/main:app.py

#@app.route("/stories")
def view():
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
