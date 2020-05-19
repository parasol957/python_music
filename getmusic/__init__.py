#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: parasol
# @time: 2020/5/15 17:42

import requests
import urllib.parse
import sys
import json
import time

sys.path.append("..")
import get_cookies

headers = {
    "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
}


def search(key='体面', pn=1, rn=30):
    data_cookie = get_cookies.getCookies()
    url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord'
    headers['Referer'] = 'http://www.kuwo.cn/search/list?key=' + urllib.parse.quote(key)

    headers['csrf'] = data_cookie['cookies']['kw_token']
    params = {
        'key': key,
        'pn': pn,
        'rn': rn,
        'reqId': data_cookie['reqId']
    }
    music_data = requests.get(url, headers=headers, cookies=data_cookie['cookies'], params=params)
    return json.loads(music_data.text)


def getDtail(rid):
    data_cookie = get_cookies.getCookies()
    headers = {
        "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        'Referer': 'http://www.kuwo.cn/',
        'csrf': data_cookie['cookies']['kw_token']
    }
    params = {
        'format': 'mp3',
        'rid': rid,
        'response': 'url',
        'type': 'convert_url3',
        'br': '128kmp3',
        'from': 'web',
        't:': int(round(time.time() * 1000)),
        'reqId': data_cookie['reqId']
    }
    url = 'http://www.kuwo.cn/url'
    resData = requests.get(url, headers=headers, cookies=data_cookie['cookies'], params=params)
    return resData.text
