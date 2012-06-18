#!/usr/bin/python

import os
import re
import HTMLParser
import nltk
import json
#from nltk.tokenize import sent_tokenize

from pylab import *
from collections import defaultdict

freq = defaultdict(int)

pos = {'lest': 'JJS', 'replied': 'VBN', 'moments': 'NNS', 'pointed': 'VBN', 'defended': 'VBD', 'per': 'IN', 'summed': 'VBN', 'before': 'IN', '(': ':', ',': ',', 'late': 'JJ', 'to': 'TO', 'citing': 'VBG', 'praised': 'VBD', 'questioned': 'VBN', 'under': 'IN', 'agreed': 'VBD', 'his': 'PRP$', 'attribution': 'NN', 'early': 'RB', 'not': 'RB', 'during': 'IN', '--': ':', 'either': 'DT', 'speculation': 'NN', 'noted': 'VBD', 'because': 'IN', 'accused': 'VBD', 'estimated': 'VBN', 'out': 'IN', 'by': 'IN', 'said': 'VBD', 'for': 'IN', 'since': 'IN', 'expressed': 'VBN', 'denied': 'VBN', 'probably': 'RB', ';': ':', 'told': 'VBD', 'who': 'WP', 'here': 'RB', 'attributions': 'NNS', 'put': 'VBD', 'from': 'IN', 'went': 'VBD', 'suggested': 'VBD', 'both': 'DT', 'about': 'IN', 'last': 'JJ', 'ahead': 'RB', 'Tuesday': 'NNP', 'discussed': 'VBN', 'according': 'VBG', 'or': 'CC', 'explained': 'VBD', 'given': 'VBN', 'described': 'VBN', 'would': 'MD', 'due': 'JJ', '.': '.', ':': ':', 'was': 'VBD', 'is': 'VBZ', 'today': 'NN', '``': '``', 'that': 'IN', 'but': 'CC', 'recalled': 'VBN', 'this': 'DT', 'as': 'IN', 'until': 'IN', 'placed': 'VBN', 'while': 'IN', 'were': 'VBD', 'following': 'VBG', 'called': 'VBN', 'and': 'CC', 'played': 'VBN', 'cited': 'VBN', 'say': 'VBP', 'at': 'IN', 'have': 'VBP', 'in': 'IN', 'confirmed': 'VBN', ')': ':', 'when': 'WRB', 'you': 'PRP', 'gets': 'NNS', 'added': 'VBD', 'after': 'IN', 'yesterday': 'NN', 'on': 'IN', 'later': 'JJ', 'acknowledged': 'VBD', 'rather': 'RB', 'so': 'IN', 'the': 'DT'}

monthsdict = {"January": 0,
              "February": 1,
              "March": 2,
              "April": 3,
              "May": 4,
              "June": 5,
              "July": 6,
              "August": 7,
              "September": 8,
              "October": 9,
              "November": 10,
              "December": 11}

def twodigit(num):
    foo = str(num)
    if len(foo) == 2:
        return foo
    else:
        return "0"+foo

class MLStripper(HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

whitespace = re.compile(r'\s+')
quotes = re.compile(r'\'\'')

def scrub(line):
    try:
        s = MLStripper()
        s.feed(line.decode('utf-8','ignore').encode('ascii','ignore'))
        stripped = s.get_data()
    except HTMLParser.HTMLParseError:
        stripped = line
        print line
    return quotes.sub('"',whitespace.sub(' ', stripped))
    
out_list = []

xs = range(6 + 12*12)
blind = [0 for x in xs]
reasons = [0 for x in xs]

for root,files,dir in os.walk("texts"):
    dir.sort()
    dir = [x for x in dir if ".html" in x]
    for file in dir:
        f=open("texts/" + file, 'r')
        if "gst_fullpage" not in file:
            bits = file.split("_")
            year = int(bits[0])
            month = int(bits[1])
            day = int(bits[2])
            date_i = (month-1) + 12*(year-2000)
            url = "http://www.nytimes.com/" + file.replace('_','/')
        else:
            url = "http://query.nytimes.com/" + file.replace('_','/')
        for line in f:
#             m = re.search('<meta name="keywords" content="([^\"]+)">',line)
#             if m:
#                 print m.group(1).split(',')
            derp = line.split('<div class="timestamp">')
            if len(derp)>1:
                bits = derp[1].split(" ")
                year = int(bits[2][:4])
                month = monthsdict[bits[0]]
                day = int(bits[1].split(",")[0])
                date_i = (month-1) + 12*(year-2000)
            if "condition of anonymity" in line:
                blind[date_i] += 1
                scrubbed = scrub(line)
                sentences = nltk.sent_tokenize(scrubbed)
                for sentence in sentences:
                    if "condition of anonymity" in sentence:
                        words = nltk.word_tokenize(sentence)
#                        parts = nltk.pos_tag(words)
#                         if 'anonymity' in words:
#                             foo = parts[words.index('anonymity')+1]
#                             pos[foo[0]]=foo[1]
                        chunks = re.split(",|--",sentence)
                        for i in range(len(chunks)):
                            if "condition of anonymity " in chunks[i]:
                                clause = chunks[i].split("condition of anonymity ")[1]
                                if pos[words[words.index('anonymity')+1]] in ['IN']:
#                                if pos[words[words.index('anonymity')+1]] not in ['VBN','VBD',',','.']:
                                    out = {'reason':clause, 'sentence': sentence, 'url':url, 'date': str(year)+'-'+twodigit(month+1)+'-'+twodigit(day)}
                                    out_list.append(out)
#                    if "anonymity because" in sentence:
#                        print "because" + sentence.split("because")[1]
                blind[date_i] += 1
            if "anonymity because" in line:
                reasons[date_i] += 1
        f.close()

fh = open("reasons.json","wb")
json.dump(out_list,fh)

# words = freq.keys()
# words.sort(key=lambda foo: freq[foo], reverse=True)
# for word in words:
#     print word, freq[word]
#plot(xs,blind,xs,reasons)
#show()