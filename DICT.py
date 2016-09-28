#!/usr/bin/env python
import re;
import urllib;
import urllib2;
import sys;
import json

GREEN = "\033[1;32m";
DEFAULT = "\033[0;49m";
BOLD = "\033[1m";
UNDERLINE = "\033[4m";
NORMAL = "\033[m";
RED = "\033[1;31m"
BLUE = "\033[1;34m"
HCZCOLOR = "\033[1;33m"

def get_elements_by_path(xml, elem):
	if type(xml) == type(''):
		xml = [xml];
	if type(elem) == type(''):
		elem = elem.split('/');
	if (len(xml) == 0):
		return [];
	elif (len(elem) == 0):
		return xml;
	elif (len(elem) == 1):
		result = [];
		for item in xml:
			result += get_elements(item, elem[0]);
		return result;
	else:
		subitems = [];
		for item in xml:
			subitems += get_elements(item, elem[0]);
		return get_elements_by_path(subitems, elem[1:]);
def get_text(xml):
	textre = re.compile("\!\[CDATA\[(.*?)\]\]", re.DOTALL);
	match = re.search(textre, xml);
	if not match:
		return xml;
	return match.group(1);
def get_elements(xml, elem):
	p = re.compile("<" + elem + ">" + "(.*?)</" + elem + ">", re.DOTALL);
	it = p.finditer(xml);
	result = [];
	for m in it:
		result.append(m.group(1));
	return result;
def yodao_trans(argv):
	xml = urllib2.urlopen("http://dict.yodao.com/search?keyfrom=dict.python&q="
		+ urllib.quote_plus(" ".join(argv)) 
		+ "&xmlDetail=true&doctype=xml").read();
        #print xml;
	original_query = get_elements(xml, "original-query");
	queryword = get_text(original_query[0]);
	
	custom_translations = get_elements(xml, "custom-translation");
	print BOLD + UNDERLINE + queryword + NORMAL;
	translated = False;
	
	for cus in custom_translations:
		source = get_elements_by_path(cus, "source/name");
		
		print RED + "Translations from " + source[0] + DEFAULT;
		contents = get_elements_by_path(cus, "translation/content");
		for content in contents[0:5]:
			print GREEN + get_text(content) + DEFAULT;
		translated = True;

	yodao_translations = get_elements(xml, "yodao-web-dict");
	printed = False;
	for trans in yodao_translations:
                webtrans = get_elements(trans, "web-translation");
		for web in webtrans[0:5]:
			if not printed:
				print RED + "Translations from yodao:" + DEFAULT;
				printed = True;
	        	keys = get_elements(web, "key");
			values = get_elements_by_path(web, "trans/value");
			summaries = get_elements_by_path(web, "trans/summary");
			key = keys[0].strip();
			value = values[0].strip();
			print BOLD +  get_text(key) + ":\t" +DEFAULT + GREEN + get_text(value) + NORMAL;

def liststr(str):
	return " ".join(str)

def hcz_trans(argv):
	arg = liststr(argv)
	data = urllib.urlopen('http://fanyi.youdao.com/openapi.do?keyfrom=tinxing&key=1312427901&type=data&doctype=json&version=1.1&q=' + urllib.quote_plus(arg)).read();
	qdata = json.loads(data)

	if qdata["errorCode"] != 0:
		print "error:", qdata["errorCode"]
		print data

	print  qdata["query"], "-", HCZCOLOR +liststr(qdata["translation"])+ DEFAULT

	if qdata.has_key("basic"):
		print BLUE + "Youdao:" + DEFAULT
		if qdata["basic"].has_key("phonetic"):
			print "/"+qdata["basic"]["phonetic"]+"/"
		print HCZCOLOR +liststr(qdata["basic"]["explains"])+ DEFAULT

	if qdata.has_key("web"):
		print BLUE + 'From web:'+ DEFAULT
		for i in qdata["web"]: 
			print i["key"], HCZCOLOR +liststr(i["value"])+ DEFAULT

def main(argv):
	if len(argv) <= 0:
		print "usage: dict.py word_to_translate";
		sys.exit(1);
	hcz_trans(argv)
	print 
	yodao_trans(argv);
if __name__ == "__main__":
	main(sys.argv[1:]);
