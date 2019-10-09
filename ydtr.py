#!/usr/bin/env python3
# -*- coding: utf-8 -*-  

import requests
import sys
import urllib
from bs4 import BeautifulSoup


headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5",
           "Accept-Encoding": "gzip, deflate"}


def translate(word):
    print("word:", word)
    url = "http://dict.youdao.com/w/{0}/#keyfrom=dict2.top".format(urllib.parse.quote(word))
    print("url:", url)
    session = requests.get(url, headers=headers)
    if session.status_code != 200:
        print("HTTP %d: %s" % (session.status_code, session.reason))
        return
    html = BeautifulSoup(session.content, features="lxml")
    session.close()

    phrase = html.find_all("div", id="phrsListTab")
    if len(phrase) == 0:
        print("No such word.")
        return
    phrase = phrase[0]
    keyword = phrase.find_all("span", class_="keyword")[0].string
    print("keyword:", keyword)

    for pronounce in phrase.find_all("span", class_="pronounce"):
        phonetic_type = pronounce.contents[0].strip()
        phonetic = pronounce.find_all("span", class_="phonetic")
        if len(phonetic) == 0:
            continue
        phonetic = phonetic[0].string
        if phonetic_type != "":
            print(phonetic_type, phonetic)
        else:
            print(phonetic)

    trans = phrase.find_all("div", class_="trans-container")
    if len(trans) > 0:
        trans = trans[0]
        translation = trans.ul
        # English word
        for line in translation.find_all("li"):
            print(line.string)
        # Chinese word
        for wordgroup in translation.find_all("p", class_="wordGroup"):
            line = wordgroup.get_text().strip().split('\n')
            line = map(lambda x: x.strip(), filter(lambda x: x != "", line))
            line = map(lambda x: x.strip('#').replace('#', ' '), ('#'.join(line)).split(';'))
            print('; '.join(line))
        # additional
        addition = trans.find_all("p", class_="additional")
        if len(addition) > 0:
            addition = addition[0].string.split()
            print(' '.join(addition))

    etransform = html.find_all("div", id="eTransform")
    if len(etransform) > 0:
        etransform = etransform[0]
        # phrase
        wordgroups = etransform.find_all("div", id="wordGroup")
        if len(wordgroups) > 0:
            for wordgroup in wordgroups[0].find_all("p", class_="wordGroup")[:4]:
                line = filter(lambda x: x != '', map(lambda x: x.strip(), wordgroup.get_text().split('\n')))
                line = map(lambda x: x.strip('#').replace('#', ': '), ('#'.join(line)).split(';'))
                print('; '.join(line))
        # synonym
        synonyms = etransform.find_all("div", id="synonyms")
        if len(synonyms) > 0:
            line = synonyms[0].get_text().strip().split('\n')
            line = map(lambda x: x.strip(), filter(lambda x: x != "", line))
            #print(list(line))
        # wordroot


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for word in sys.argv[1:]:
            translate(word)
    else:
        while True:
            print("> ", end='')
            try:
                word = input()
            except EOFError:
                print("\nbye")
                break
            translate(word)
