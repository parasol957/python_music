#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: parasol
# @time: 2020/5/15 16:12
# cookies2 = dict(map(lambda x: x.split('='), cookies.split(";")))
import execjs
import requests
import time
import json
# import get_cookies
#
import urllib.parse

import getmusic

from flask import Flask

from flask import request
from flask_cors import CORS

app = Flask(__name__)


def task(name, page, size):
    search_data = getmusic.search(name,page,size)
    return json.dumps(search_data, ensure_ascii=False)
    # for s in search_data['data']['list']:
    #     print(urllib.parse.unquote(s['name']))
    #     rid = s['rid']
    #     data = getmusic.getDtail(rid)
    #     return data


@app.route('/lists', methods=['POST'])
def lists():
    args = request.form.get("keywords")
    page = request.form.get("page")
    size = request.form.get("size")
    print(args, page, size)
    if (args):
        data = task(args, page, size)
        # return json.dumps(data, ensure_ascii=False)
        return data
    else:
        return json.dumps({
            'code': 300,
            'msg': "请输入值"
        }, ensure_ascii=False)


@app.route('/get_music', methods=['POST'])
def get_music():
    rid = request.form.get("rid")
    if rid:
        data = getmusic.getDtail(rid)
        return data
    else:
        return json.dumps({
            'code': 300,
            'msg': "请输入值"
        }, ensure_ascii=False)


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(debug=True, port=8777, host='0.0.0.0')
