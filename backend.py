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

TITLE = u"活動即將開始"
TITLE_COLOR = "#000000"
TITLE_SIZE = 70
TITLE_ACTIVE = False

DATA_DEBATE = {
    'title': u'活動即將開始',
    'color': '#000000',
    'size': 70,
    'display': False
}

DEBATE_ALERT_FOLDER = 'static/dabate/alert'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['DEBATE_ALERT_FOLDER'] = DEBATE_ALERT_FOLDER
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
    DATA_DEBATE_ALERT['img'] = str(ts) + '.png'
    file.save(os.path.join(app.config['DEBATE_ALERT_FOLDER'], DATA_DEBATE_ALERT['img']))


DATA_DEBATE_ALERT = {
    'img': get_alert_photo(),
    'display': False
}

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


@app.route('/debate/title', methods=['GET', 'POST'])
def test():
    global TITLE
    global TITLE_COLOR
    global TITLE_SIZE
    if request.method == 'POST':
        data = request.get_json(silent=True)
        DATA_DEBATE['title'] = unicode(data['title'])
        DATA_DEBATE['color'] = unicode(data['color'])
        DATA_DEBATE['size'] = data['size']
        DATA_DEBATE['display'] = unicode(data['display'])
        return generate_json(DATA_DEBATE)
    else:
        return generate_json(DATA_DEBATE)

@app.route('/debate/data/alert', methods=['GET', 'POST'])
def debate_alert():
    global DATA_DEBATE_ALERT
    if request.method == 'POST':
        data = request.get_json(silent=True)
        DATA_DEBATE_ALERT['display'] = data['display']
        DATA_DEBATE_ALERT['img'] = get_alert_photo()
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



@app.route('/debate/photos', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return generate_json({'msg': 'OK'})
    else:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return generate_json(files)


@app.route('/data')
def data():
    global TITLE
    global TITLE_COLOR
    global TITLE_SIZE
    global TITLE_ACTIVE
    msg = {'title':TITLE,'color':TITLE_COLOR,'size':TITLE_SIZE,'titleActive':TITLE_ACTIVE}
    return generate_json(msg)


@app.route('/title', methods=['GET', 'POST'])
def title():
    global TITLE
    global TITLE_COLOR
    global TITLE_SIZE
    global TITLE_ACTIVE
    if request.method == 'POST':
        data = request.get_json(silent=True)
        TITLE = unicode(data['title'])
        TITLE_COLOR = unicode(data['color'])
        TITLE_SIZE = unicode(data['size'])
        TITLE_ACTIVE = data['titleActive']
        msg = {'title':TITLE,'color':TITLE_COLOR,'size':TITLE_SIZE,'titleActive':TITLE_ACTIVE}
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
    app.run(host='0.0.0.0', port=config.SERVER_PORT, threaded=True, debug=True, use_reloader=True)
