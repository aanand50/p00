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
def home():
    return render_template("homePage.html", projectName = "Land of Stories", description = "description")

@app.route("/response" , methods=['POST'])
def register():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if(request.form.get('username') == None):
        if(request.form.get('usernameL') != ""):
            c.execute("SELECT * FROM users WHERE username="+"'"+request.form.get('usernameL')+"'"+";")
            user = c.fetchone()
            if(user != None and user[1] == request.form.get('passwordL')):
                session['username'] = user[0]
                return redirect(url_for("home"))
    if(request.form.get('usernameL') == None):
        if(request.form.get('username') != ""): #Only change username if it's not none
            c.execute("SELECT * FROM users WHERE username="+"'"+request.form.get('username')+"'"+";")
            user = c.fetchone()
            if(user == None):

                c.execute("INSERT INTO users(username,password) VALUES (?,?);", (request.form.get('username'),request.form.get('password')))

                db.commit()
                db.close()
    return render_template('login.html')

@app.route('/createStories', methods=['GET', 'POST'])
def create_story():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if(request.method == 'POST'):
        if(request.form.get('title') != "" and request.form.get('text') != "" and session.get('username') != None):
            c.execute("SELECT * FROM stories WHERE name = ?;",(request.form.get('title'),))
            story = c.fetchone()
            if(story == None):
                c.execute("INSERT INTO stories(name) VALUES (?);", (request.form.get('title'),))
                c.execute("INSERT INTO usertext(user, story, text) VALUES (?,?,?);", (session.get('username'), request.form.get('title'), request.form.get('text')))
                db.commit()
                db.close()
                return redirect(url_for("home"))
    return render_template('createStories.html')

def edit():
    text = request.form.get("text")
    if(length(text) < wordCount):
        c.execute("INSERT INTO usertext(user,story,text) VALUES (?,?,?);", (session['username'],session['story'] ,session['text']))
        db.commit()
        db.close()

def display():
    c.execute("SELECT * FROM usertext WHERE story = ?;",(session.get('story'),))
    #storyTex

@app.route("/login")
def login():
    if(session.get('username') != None):
        return redirect(url_for("home"))
    return render_template("login.html", projectName="projectName PH")

@app.route("/logout")
def logout():
    session.pop('username',None)
    return render_template("logout.html")

@app.route("/newStories")
def newStories():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM stories;")
    story_names = c.fetchall()
    return render_template("newStories.html", allStories = story_names)

@app.route("/storyTemplate", methods=['GET'])
def story_temp():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if(request.args.get('story') != None):
        c.execute("SELECT * FROM usertext WHERE story = ?;",(request.args.get('story'),))
        story_text = c.fetchall()
        if(session.get('username') != None):
            loggedin = True
        else:
            loggedin = False
        return render_template("storyTemplate.html", storyText=story_text,isLoggedIn = loggedin,title=request.args.get('story'))
    return render_template("newStories.html", allStories = story_names)

if __name__ == "__main__":
    app.debug = True
    app.run()
