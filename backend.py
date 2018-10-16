 # !/usr/bin/python
 # -*- coding: utf-8 -*-

import json
from flask import Flask
from flask import make_response
from flask import request
from flask import render_template
from bson import json_util
from instance import config
from instance import error_msg
import datetime
from flask import Response

app = Flask(__name__)

TITLE = u"活動即將開始"
TITLE_COLOR = "#000000"
TITLE_SIZE = 70

@app.route('/')
def index():
    return ('watchout!')

@app.route('/enter')
def enter():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

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
    app.run(host='0.0.0.0', port=config.SERVER_PORT, threaded=True, debug=True, use_reloader=True)
