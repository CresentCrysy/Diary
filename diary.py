from flask import Flask, render_template, jsonify, request
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('diary.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.Diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    file = request.files["file_give"]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    profile = request.files['prof_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/prof-{mytime}.{extension}'
    profile.save(profilename)

    time = today.strftime('%Y-%m-%d-%H-%M-%S')

    doc = {
    'file': filename,
    'profile':profilename,
    'title': title_receive,
    'content': content_receive,
    'time': time,
    }
    db.Diary.insert_one(doc)
    return jsonify({'message':'Diary saved'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

