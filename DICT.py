#!/usr/bin/env python3
import re
import urllib
import urllib.request
import sys
import json
import logging

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
        textre = re.compile("\!\[CDATA\[(.*?)\]\]", re.DOTALL)
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

    def trans(self, argv):
        xml = urllib.request.urlopen("http://dict.yodao.com/search?keyfrom=dict.python&q="
                                     + urllib.parse.quote_plus(" ".join(argv))
                                     + "&xmlDetail=true&doctype=xml").read().decode('utf-8')
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
                print(BOLD + self.get_text(key) + ":\t" + DEFAULT + GREEN + self.get_text(value) + NORMAL)


# ----------------------------------------------------------------------------------------#

class youdaodict:
    def __init__(self):
        self.url = 'http://fanyi.youdao.com/openapi.do?keyfrom=tinxing&key=1312427901&type=data&doctype=json&version=1.1&q='

    @staticmethod
    def list_str(string):
        return " ".join(string)

    def trans(self, argv):
        arg = self.list_str(argv)
        print(self.url + urllib.parse.quote_plus(arg))
        data = urllib.request.urlopen(self.url + urllib.parse.quote_plus(arg)).read()
        qdata = json.loads(data)

        if qdata["errorCode"] != 0:
            print("error:", qdata["errorCode"])
            print(data)
        print(qdata["query"], '-', YELLOW + self.list_str(qdata["translation"]) + DEFAULT)

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
def main(argv):
    # print(sys.version)
    if len(argv) <= 0:
        print("usage: %s word_to_translate" % (sys.argv[0]))
        sys.exit(1)
    try:
        youdaod = youdaodict()
        youdaod.trans(argv)
        print()
    except Exception as e:
        logger.error(str(e), exc_info=True)

    try:
        yodao = yodaodict()
        yodao.trans(argv)
    except Exception as e:
        logger.error(str(e), exc_info=True)


if __name__ == "__main__":
    main(sys.argv[1:])
