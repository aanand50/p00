# Kevin Lin, Raymond Lin, Christopher Louie
# Death Row Coders
# SoftDev
# October 11, 2024
# 1

import os
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
import sqlite3

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret
wordCount = 200
DB_FILE="discobandit.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT);")
c.execute("CREATE TABLE IF NOT EXISTS stories(name TEXT);")
c.execute("CREATE TABLE IF NOT EXISTS usertext(user TEXT, storyid INTEGER, text TEXT);")

def length(a):
    return len(a) - len(a.replace(" ", ""))

@app.route("/")
def disp_loginpage():
    if 'username' in session:
        return redirect("/response.html")
    return render_template( 'login.html' )

@app.route("/response.html" , methods=['POST'])
def authenticate():
    if(request.form.get('username') != None and session.get('username') == None): #Only change username if it's not none
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')

        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        c.execute("INSERT INTO users(username,password) VALUES (?,?);", (session['username'],session['password']))

        db.commit()
        db.close()
        
    return render_template( 'response.html', username = session['username'])

#@app.route("/stories")
def view():
    text = request.form.get("text")
    if(length(text) < wordCount):
        c.execute("INSERT INTO usertext(user,storyid,text) VALUES (?,?,?);", (session['username'],session['storyid'] ,session['text']))

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('logout.html')
    
if __name__ == "__main__":
    app.debug = True 
    app.run()

