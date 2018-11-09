 # !/usr/bin/python
 # -*- coding: utf-8 -*-

import json
from flask import Flask, make_response, request, render_template, Response, redirect, url_for
from bson import json_util
from instance import config
from instance import error_msg
import time
from werkzeug import secure_filename
import os
from threading import Timer

TITLE = u"活動即將開始"
TITLE_COLOR = "#000000"
TITLE_SIZE = 70

DATA_DEBATE = {
    'title': u'活動即將開始',
    'color': '#000000',
    'size': 70,
    'display': False
}

DEBATE_ALERT_FOLDER = 'static/debate/alert'
DEBATE_Q_FOLDER = 'static/debate/question'
DEBATE_A_FOLDER = 'static/debate/answer'
DEBATE_C_FOLDER = 'static/debate/comment'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['DEBATE_ALERT_FOLDER'] = DEBATE_ALERT_FOLDER
app.config['DEBATE_Q_FOLDER'] = DEBATE_Q_FOLDER
app.config['DEBATE_A_FOLDER'] = DEBATE_A_FOLDER
app.config['DEBATE_C_FOLDER'] = DEBATE_C_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_alert_photo():
    files = os.listdir(app.config['DEBATE_ALERT_FOLDER'])
    files.sort()
    file = files[-1]
    return (app.config['DEBATE_ALERT_FOLDER']+'/'+file)

def save_alert_photo(file):
    ts = time.time()
    ts = int(ts*1000000)
    DATA_DEBATE_ALERT['img'] = str(ts) + '.gif'
    file.save(os.path.join(app.config['DEBATE_ALERT_FOLDER'], DATA_DEBATE_ALERT['img']))

def get_q_photo():
    files = os.listdir(app.config['DEBATE_Q_FOLDER'])
    files.sort()
    file = files[-1]
    return (app.config['DEBATE_Q_FOLDER']+'/'+file)

def save_q_photo(file):
    ts = time.time()
    ts = int(ts*1000000)
    DATA_DEBATE_Q['img'] = str(ts) + '.png'
    file.save(os.path.join(app.config['DEBATE_Q_FOLDER'], DATA_DEBATE_Q['img']))

def get_answer_photo():
    files = os.listdir(app.config['DEBATE_A_FOLDER'])
    files.sort()
    file = files[-1]
    return (app.config['DEBATE_A_FOLDER']+'/'+file)

def save_answer_photo(file):
    ts = time.time()
    ts = int(ts*1000000)
    DATA_DEBATE_ANSWER['img'] = str(ts) + '.png'
    file.save(os.path.join(app.config['DEBATE_A_FOLDER'], DATA_DEBATE_ANSWER['img']))

def get_comment_photo():
    files = os.listdir(app.config['DEBATE_C_FOLDER'])
    files.sort()
    file = files[-1]
    return (app.config['DEBATE_C_FOLDER']+'/'+file)

def save_comment_photo(file):
    ts = time.time()
    ts = int(ts*1000000)
    DATA_DEBATE_COMMENT['img'] = str(ts) + '.png'
    file.save(os.path.join(app.config['DEBATE_C_FOLDER'], DATA_DEBATE_COMMENT['img']))

DATA_DEBATE_ALERT = {
    'img': get_alert_photo(),
    'display': False,
    'countDown': 4,
    'currentCountDown': 0
}

DATA_DEBATE_Q = {
    'title': 'Q_TITLE',
    'img': get_q_photo(),
    'display': False,
    'countDown': 10,
    'currentCountDown': 0
}

DATA_DEBATE_ANSWER = {
    'img': get_answer_photo(),
    'display': False,
    'countDown': 15,
    'currentCountDown': 0
}

DATA_DEBATE_COMMENT = {
    'title': 'COMMENT_TITLE',
    'img': get_comment_photo(),
    'display': False,
    'countDown': 6,
    'currentCountDown': 0
}


def countDown():
    global DATA_DEBATE_ALERT
    global DATA_DEBATE_Q
    global DATA_DEBATE_ANSWER
    global DATA_DEBATE_COMMENT

    if DATA_DEBATE_ALERT['currentCountDown'] > 0:
        DATA_DEBATE_ALERT['currentCountDown'] -= 1
    else:
        DATA_DEBATE_ALERT['display'] = False
    
    if DATA_DEBATE_Q['currentCountDown'] > 0:
        DATA_DEBATE_Q['currentCountDown'] -= 1
    else:
        DATA_DEBATE_Q['display'] = False
    
    if DATA_DEBATE_ANSWER['currentCountDown'] > 0:
        DATA_DEBATE_ANSWER['currentCountDown'] -= 1
    else:
        DATA_DEBATE_ANSWER['display'] = False
    
    if DATA_DEBATE_COMMENT['currentCountDown'] > 0:
        DATA_DEBATE_COMMENT['currentCountDown'] -= 1
    else:
        DATA_DEBATE_COMMENT['display'] = False
    # print str(DATA_DEBATE_ALERT['currentCountDown']) + ' | ' + str(DATA_DEBATE_Q['currentCountDown'] + ' | ' + str(DATA_DEBATE_ANSWER['currentCountDown'])
    t = Timer(1.0, countDown)
    t.start()



@app.route('/')
def index():
    return ('watchout!')

@app.route('/enter')
def enter():
    return render_template('index.html')

@app.route('/debate')
def debate():
    return render_template('debate.html')

@app.route('/debate_back')
def test_back():
    return render_template('debate_back.html')


@app.route('/debate/data', methods=['GET'])
def test():
    global DATA_DEBATE_ALERT
    global DATA_DEBATE_Q
    global DATA_DEBATE_ANSWER
    global DATA_DEBATE_COMMENT
    if request.method == 'GET':
        DATA_DEBATE_ALERT['img'] = get_alert_photo()
        DATA_DEBATE_Q['img'] = get_q_photo()
        DATA_DEBATE_ANSWER['img'] = get_answer_photo()
        DATA_DEBATE_COMMENT['img'] = get_comment_photo()
        outputData = {
            'debateAlert': DATA_DEBATE_ALERT,
            'debateQuestion': DATA_DEBATE_Q,
            'debateAnswer': DATA_DEBATE_ANSWER,
            'debateComment': DATA_DEBATE_COMMENT
        }
        return generate_json(outputData)
    else:
        return generate_json({})

@app.route('/debate/data/alert', methods=['GET', 'POST'])
def debate_alert():
    global DATA_DEBATE_ALERT
    if request.method == 'POST':
        data = request.get_json(silent=True)
        DATA_DEBATE_ALERT['display'] = data['display']
        DATA_DEBATE_ALERT['img'] = get_alert_photo()
        DATA_DEBATE_ALERT['countDown'] = int(data['countDown'])
        DATA_DEBATE_ALERT['currentCountDown'] = int(data['currentCountDown'])
        return generate_json(DATA_DEBATE_ALERT)
    else:
        DATA_DEBATE_ALERT['img'] = get_alert_photo()
        return generate_json(DATA_DEBATE_ALERT)

@app.route('/debate/data/alert/photo', methods=['GET', 'POST'])
def debate_alert_photo():
    global DATA_DEBATE_ALERT
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            save_alert_photo(file)
            return generate_json(DATA_DEBATE_ALERT)
    else:
        DATA_DEBATE_ALERT['img'] = get_alert_photo()
        return generate_json(DATA_DEBATE_ALERT)

@app.route('/debate/data/question', methods=['GET', 'POST'])
def debate_question():
    global DATA_DEBATE_ALERT
    global DATA_DEBATE_Q
    global DATA_DEBATE_ANSWER
    global DATA_DEBATE_COMMENT
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if DATA_DEBATE_COMMENT['display'] is False: 
            DATA_DEBATE_Q['display'] = data['display']
            DATA_DEBATE_ANSWER['display'] = False
        DATA_DEBATE_Q['img'] = get_q_photo()
        DATA_DEBATE_Q['title'] = data['title']
        DATA_DEBATE_Q['countDown'] = int(data['countDown'])
        DATA_DEBATE_Q['currentCountDown'] = int(data['currentCountDown'])
        return generate_json(DATA_DEBATE_Q)
    else:
        DATA_DEBATE_Q['img'] = get_q_photo()
        return generate_json(DATA_DEBATE_Q)

@app.route('/debate/data/question/photo', methods=['GET', 'POST'])
def debate_question_photo():
    global DATA_DEBATE_Q
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            save_q_photo(file)
            return generate_json(DATA_DEBATE_Q)
    else:
        DATA_DEBATE_Q['img'] = get_q_photo()
        return generate_json(DATA_DEBATE_Q)

@app.route('/debate/data/answer', methods=['GET', 'POST'])
def debate_answer():
    global DATA_DEBATE_ALERT
    global DATA_DEBATE_Q
    global DATA_DEBATE_ANSWER
    global DATA_DEBATE_COMMENT
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if DATA_DEBATE_Q['display'] is False and DATA_DEBATE_COMMENT['display'] is False: 
            DATA_DEBATE_ANSWER['display'] = data['display']
            if data['display']:
                DATA_DEBATE_ALERT['display'] = False
                DATA_DEBATE_Q['display'] = False
        DATA_DEBATE_ANSWER['img'] = get_answer_photo()
        DATA_DEBATE_ANSWER['countDown'] = int(data['countDown'])
        DATA_DEBATE_ANSWER['currentCountDown'] = int(data['currentCountDown'])
        return generate_json(DATA_DEBATE_ALERT)
    else:
        DATA_DEBATE_ANSWER['img'] = get_answer_photo()
        return generate_json(DATA_DEBATE_ANSWER)

@app.route('/debate/data/answer/photo', methods=['GET', 'POST'])
def debate_answer_photo():
    global DATA_DEBATE_ANSWER
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            save_answer_photo(file)
            return generate_json(DATA_DEBATE_ANSWER)
    else:
        DATA_DEBATE_ANSWER['img'] = get_answer_photo()
        return generate_json(DATA_DEBATE_ANSWER)

@app.route('/debate/data/comment', methods=['GET', 'POST'])
def debate_comment():
    global DATA_DEBATE_ALERT
    global DATA_DEBATE_Q
    global DATA_DEBATE_ANSWER
    global DATA_DEBATE_COMMENT
    if request.method == 'POST':
        data = request.get_json(silent=True)
        DATA_DEBATE_COMMENT['display'] = data['display']
        if data['display']:
            DATA_DEBATE_ALERT['display'] = False
            DATA_DEBATE_Q['display'] = False
            DATA_DEBATE_ANSWER['display'] = False
        DATA_DEBATE_COMMENT['img'] = get_comment_photo()
        DATA_DEBATE_COMMENT['title'] = data['title']
        DATA_DEBATE_COMMENT['countDown'] = int(data['countDown'])
        DATA_DEBATE_COMMENT['currentCountDown'] = int(data['currentCountDown'])
        return generate_json(DATA_DEBATE_COMMENT)
    else:
        DATA_DEBATE_COMMENT['img'] = get_comment_photo()
        return generate_json(DATA_DEBATE_COMMENT)

@app.route('/debate/data/comment/photo', methods=['GET', 'POST'])
def debate_comment_photo():
    global DATA_DEBATE_COMMENT
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            save_comment_photo(file)
            return generate_json(DATA_DEBATE_COMMENT)
    else:
        DATA_DEBATE_COMMENT['img'] = get_comment_photo()
        return generate_json(DATA_DEBATE_COMMENT)

@app.route('/data')
def data():
    global TITLE
    global TITLE_COLOR
    global TITLE_SIZE
    msg = {'title':TITLE,'color':TITLE_COLOR,'size':TITLE_SIZE}
    return generate_json(msg)


@app.route('/title', methods=['GET', 'POST'])
def title():
    global TITLE
    global TITLE_COLOR
    global TITLE_SIZE
    if request.method == 'POST':
        data = request.get_json(silent=True)
        TITLE = unicode(data['title'])
        TITLE_COLOR = unicode(data['color'])
        TITLE_SIZE = unicode(data['size'])
        msg = {'title':TITLE,'color':TITLE_COLOR,'size':TITLE_SIZE}
        return generate_json(msg)
    else:
        return render_template('title.html', title_color=TITLE_COLOR, title_size=TITLE_SIZE)


def generate_json(f):
    result = json.dumps(f, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None,
                        indent=True, separators=None, encoding="utf-8", sort_keys=False, default=json_util.default)
    resp = make_response(result)
    if request.headers.get('Accept', '').find('application/json') > -1:
        resp.mimetype = 'application/json'
    else:
        resp.mimetype = 'text/plain'
    return resp


if __name__ == "__main__":
    countDown()
    app.run(host='0.0.0.0', port=config.SERVER_PORT, threaded=True, debug=True, use_reloader=True)
