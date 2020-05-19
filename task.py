#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: parasol
# @time: 2020/5/15 17:32
import execjs
import requests


def getCookies():
    js_str = get_js()
    ctx = execjs.compile(js_str)  # 加载JS文件
    test1 = ctx.call('l', 4)  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数
    reqId = ctx.call('c', test1)  # 获取reqId

    get_cookie_url = 'http://www.kuwo.cn/'
    r = requests.get(get_cookie_url)
    cookies = requests.utils.dict_from_cookiejar(r.cookies)  # 获取cookie
    data = {
        'reqId': reqId,
        'cookies': cookies
    }
    return data


def get_js():
    # f = open("./../js/my.js", 'r', encoding='utf-8') # 打开JS文件
    f = open("2.js", 'r', encoding='utf-8')  # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


