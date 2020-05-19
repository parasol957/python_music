# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
import base64
import random
import codecs
import requests
from fake_useragent import UserAgent
from http.cookiejar import LWPCookieJar
import hashlib

'''
之前也写过网易云音乐的评论爬取，下载歌曲，还有其他等等。。。

网易云音乐登录加密方式其实和评论的加密方式是一样的，只不过传入的参数不同罢了，而登录需要构造下面login方法注释里字典格式

注意千万不要使用json.dumps(字典)来将字典转为json格式字符串。因为字典它是无序的，转出来的json字符串有可能是不一样的，这样
导致最终加密出来的字符串是不同的

其实上一篇爬取评论的时候，我就写了登录方式。但是登录失败了。加密方式是没有变的，通过js调试，我发现checkToken这个参数的值，
它是变化的，所以那时就一直想找到checkToken它的参数是怎么来的。找得头都大，位置大概知道了。但是解出来的话，我能力不够(其实就不太愿意花时间去弄)，
我也在网上搜索过，但也没找到想要的答案。弄了一段时间，就先放一放了。

昨天晚上写完微博的模拟登录，今早想起了网易云音乐登录还没写完。捣腾了一会儿。发现之前一直想解出的checkToken参数，不传也
可以成功登录。

不必要弄懂全部参数的加密方式，有时候这个参数后台不是判断的必要条件。
'''


class WYY:
    ua = UserAgent()

    def __init__(self):
        self.arg2 = "010001"
        self.arg3 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.arg4 = "0CoJUm6Qyw8W8jud"
        self.session = requests.Session()
        self.session.headers = {
            "Referer": "https://music.163.com/",
            "User-Agent": self.ua.random
        }
        self.session.cookies = LWPCookieJar(filename="./cookie.txt")
        self.__get_random_str()

    def __AES_encrypt(self, text, key):
        '''
        获取到加密后的数据
        :param text: 首先CBC加密方法，text必须位16位数据
        :param key: 加密的key
        :return: 加密后的字符串
        '''
        iv = "0102030405060708"
        pad = 16 - len(text) % 16
        if isinstance(text, str):
            text = text + pad * chr(pad)
        else:
            text = text.deocde("utf-8") + pad * chr(pad)
        aes = AES.new(key=bytes(key, encoding="utf-8"), mode=2, iv=bytes(iv, encoding="utf-8"))
        res = aes.encrypt(bytes(text, encoding="utf-8"))
        res = base64.b64encode(res).decode("utf-8")
        return res

    def __get_encText(self, args1):
        encText = self.__AES_encrypt(args1, self.arg4)
        encText = self.__AES_encrypt(encText, self.random_16_str)
        return encText

    def __get_encSecKey(self):
        '''通过查看js代码，获取encSecKey'''
        text = self.random_16_str[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(self.arg2, 16) % int(self.arg3, 16)
        return format(rs, 'x').zfill(256)

    def __get_random_str(self):
        '''这是16位的随机字符串'''
        str_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        random_str = ""
        for i in range(16):
            index = random.randint(0, len(str_set) - 1)
            random_str += str_set[index]
        self.random_16_str = random_str

    def __getFormData(self, args1):
        '''获取到提交的数据'''
        data = {"params": self.__get_encText(args1), "encSecKey": self.__get_encSecKey()}
        return data

    def login(self, username: str = None, password: str = None):
        '''网易云登录'''
        '''
        参数一为构造这样的字典格式
        checkToken: "9ca17ae2e6ffcda170e2e6eed9ee33fb9d9dd6cb7a98ef8eb2d85b879b9ababc6788b6ab96f95afcb8adaabc2af0feaec3b92aadb88ab1c446a1ef0099f65a879f9ba6c85a9bb0a2b9e945f5eca69bd952af95ee9e"
        csrf_token: ""
        password: "5cf36a0d72feb44111716322921ed011"
        phone: "18716758271"
        rememberLogin: "true"
        '''
        api = "https://music.163.com/weapi/login/cellphone?csrf_token="
        headers = {}
        headers["content-type"] = "application/x-www-form-urlencoded"
        headers["user-agent"] = self.ua.random
        headers["referer"] = "https://music.163.com/"
        if not username:
            username = input("输入你的电话>>:").strip()
        else:
            username = username.strip()
        if not password:
            password = input("输入你的密码>>:").strip()
        else:
            password = password.strip()
        self.arg1_login = '{"phone":"%s","password":"%s","rememberLogin":"true","checkToken":"","csrf_token": ""}' % (
            username, hashlib.md5(bytes(password, encoding="utf-8")).hexdigest())
        formdata = self.__getFormData(self.arg1_login)
        response = self.session.post(url=api, headers=headers, data=formdata)
        results = response.json()

        if results["code"] == 200:
            self.session.cookies.save()
            print("登录成功")
        else:
            print(results["msg"])

    def text(self):
        '''测试方式'''
        pass


if __name__ == '__main__':
    wyy = WYY()
    wyy.login()