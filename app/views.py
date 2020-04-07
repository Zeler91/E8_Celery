import requests
from datetime import datetime
from flask import render_template, request, redirect, url_for
from app import app, db, celery
from .models import Results, Tasks


@celery.task
def word_count(_id, word):
    task = Tasks.query.get(_id)
    task.task_status = 'PENDING'
    db.session.commit()
    if task.address.startswith('http') or address.startswith('https'):
        address = task.address
    else:
        address = 'http://' + task.address
    res = requests.get(address) 
    words_count=0
    request_time = datetime.now() - task.timestamp
    if  request_time.seconds > 10 :          
        http_status_code = 408
    else:
        http_status_code = res.status_code
    if res.ok:
        words = res.text.lower().split()  
    result = Results(address = address, words_count = words.count(word), http_status_code = http_status_code)
    task.task_status = 'FINISHED'
    with app.app_context():
        db.session.add(result)
        db.session.commit()


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/add_website', methods=['POST', 'GET'])
def add_website():
    if request.method == 'POST':
        address = request.form.get('address')
        http_status = requests.get(address).status_code
        if http_status == 200:
            task = Tasks(address=address, timestamp=datetime.now(), task_status='NOT_STARTED', http_status = http_status)
            print(task)
            db.session.add(task)
            db.session.commit()
            word_count.delay(task._id, "python")
            return redirect('/') 

@app.route('/results')
def results():
    results = Results.query.all()
    return render_template('results.html', results=results)