#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import hashlib
import json
import logging
import os
import re
import sys
import time
import urllib
import urllib.request
import uuid

import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

GREEN = "\033[1;32m"
DEFAULT = "\033[0;49m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
NORMAL = "\033[m"
RED = "\033[1;31m"
BLUE = "\033[1;34m"
YELLOW = "\033[1;33m"


# ----------------------------------------------------------------------------------------#
class yodaodict:
    def get_elements_by_path(self, xml, elem):
        if type(xml) == type(''):
            xml = [xml]
        if type(elem) == type(''):
            elem = elem.split('/')
        if len(xml) == 0:
            return []
        elif len(elem) == 0:
            return xml
        elif len(elem) == 1:
            result = []
            for item in xml:
                result += self.get_elements(item, elem[0])
            return result
        else:
            subitems = []
            for item in xml:
                subitems += self.get_elements(item, elem[0])
            return self.get_elements_by_path(subitems, elem[1:])

    def get_text(self, xml):
        textre = re.compile(r"\!\[CDATA\[(.*?)\]\]", re.DOTALL)
        match = re.search(textre, xml)
        if not match:
            return xml
        return match.group(1)

    def get_elements(self, xml, elem):
        p = re.compile("<" + elem + ">" + "(.*?)</" + elem + ">", re.DOTALL)
        it = p.finditer(xml)
        result = []
        for m in it:
            result.append(m.group(1))
        return result

    def trans(self, arg):
        xml = urllib.request.urlopen(
            "http://dict.yodao.com/search?keyfrom=dict.python&q="
            + urllib.parse.quote_plus(arg) + "&xmlDetail=true&doctype=xml").read().decode('utf-8')
        # print(xml)
        original_query = self.get_elements(xml, "original-query")
        queryword = self.get_text(original_query[0])

        custom_translations = self.get_elements(xml, "custom-translation")
        print(BOLD + UNDERLINE + queryword + NORMAL)

        for cus in custom_translations:
            source = self.get_elements_by_path(cus, "source/name")
            print(RED + "Translations from " + source[0] + DEFAULT)
            contents = self.get_elements_by_path(cus, "translation/content")
            for content in contents[0:5]:
                print(GREEN + self.get_text(content) + DEFAULT)

        yodao_translations = self.get_elements(xml, "yodao-web-dict")
        printed = False
        for trans in yodao_translations:
            webtrans = self.get_elements(trans, "web-translation")
            for web in webtrans[0:5]:
                if not printed:
                    print(RED + "Translations from yodao:" + DEFAULT)
                    printed = True
                keys = self.get_elements(web, "key")
                values = self.get_elements_by_path(web, "trans/value")
                # summaries = self.get_elements_by_path(web, "trans/summary")
                key = keys[0].strip()
                value = values[0].strip()
                print(BOLD + self.get_text(key) + ":\t" + DEFAULT +
                      GREEN + self.get_text(value) + NORMAL)

        # ----------------------------------------------------------------------------------------#


class youdaodict:
    def __init__(self):
        self.url = 'http://fanyi.youdao.com/openapi.do?keyfrom=tinxing&key=1312427901&type=data&doctype=json&version=1.1&q='

    @staticmethod
    def list_str(string):
        return " ".join(string)

    def trans(self, arg):
        data = urllib.request.urlopen(
            self.url + urllib.parse.quote_plus(arg)).read()
        qdata = json.loads(data)

        if qdata["errorCode"] != 0:
            print("error:", qdata["errorCode"])
            print(data)
        print(qdata["query"], '-', YELLOW +
              self.list_str(qdata["translation"]) + DEFAULT)

        if "basic" in qdata:
            print(BLUE + "Youdao:" + DEFAULT)
            if "phonetic" in qdata["basic"]:
                print("/" + qdata["basic"]["phonetic"] + "/")
            print(YELLOW + self.list_str(qdata["basic"]["explains"]) + DEFAULT)

        if "web" in qdata:
            print(BLUE + 'From web:' + DEFAULT)
            for i in qdata["web"]:
                print(i["key"], YELLOW + self.list_str(i["value"]) + DEFAULT)


# ----------------------------------------------------------------------------------------#
# https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html


class OpenapiYoudao:
    YOUDAO_URL = 'https://openapi.youdao.com/api'

    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret

    @staticmethod
    def encrypt(signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    @staticmethod
    def truncate(q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    @staticmethod
    def do_request(data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(OpenapiYoudao.YOUDAO_URL, data=data, headers=headers)

    def trans(self, q):
        # q = "test a sentences"
        if self.app_key is None or self.app_key == '' or self.app_secret is None or self.app_secret == '':
            return

        data = {}
        data['from'] = 'auto'
        data['to'] = 'auto'
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = f'{self.app_key}{self.truncate(q)}{salt}{curtime}{self.app_secret}'
        sign = self.encrypt(signStr)
        data['appKey'] = self.app_key
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign

        response = self.do_request(data)
        # contentType = response.headers['Content-Type']
        # print(response.content)
        res = json.loads(response.content)
        if res['errorCode'] == '0':
            print(f"OpenapiYoudao:{GREEN}{res['translation']}{DEFAULT}")
        else:
            print(f"error code:{RED}{res['errorCode']}{DEFAULT}")


# ----------------------------------------------------------------------------------------#

def trans(word_or_sentences):
    try:
        youdaod = youdaodict()
        youdaod.trans(word_or_sentences)
        print()
    except Exception as e:
        logger.error(str(e), exc_info=True)

    try:
        yodao = yodaodict()
        yodao.trans(word_or_sentences)
        print()
    except Exception as e:
        logger.error(str(e), exc_info=True)

    try:
        if os.path.exists('config.ini'):
            config = configparser.ConfigParser()
            config.read("config.ini")
            app_key = config.get("openapi_youdao", "APP_KEY")
            app_secret = config.get("openapi_youdao", "APP_SECRET")
            openapiYoudao = OpenapiYoudao(app_key, app_secret)
            openapiYoudao.trans(word_or_sentences)
    except Exception as e:
        logger.error(str(e), exc_info=True)


# ----------------------------------------------------------------------------------------#
def main(argv):
    # print(sys.version)
    if len(argv) <= 0:
        # print("usage: %s word_or_sentences_to_translate" % (sys.argv[0]))
        print("please enter word or sentences (press CTRL-C to exit)>")
        while True:
            instr = input()
            trans(instr)
        # sys.exit(1)
    else:
        trans(" ".join(argv))


if __name__ == "__main__":
    main(sys.argv[1:])
