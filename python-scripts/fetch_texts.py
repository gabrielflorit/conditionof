#/usr/bin/python

import time
import urllib2
import json
import os.path



article_array = json.load(open('query_results.json','r'))

for article in article_array:
    if 'www.nytimes.com' in article['url']:
        the_split = article['url'].split("http://www.nytimes.com/")
        if len(the_split) > 1:
            filename = "texts/" + the_split[1].replace('/','_')
            if not os.path.isfile(filename):
                try:
                    req = urllib2.Request(article['url']+"?pagewanted=print")
                    req.add_header('Accept-Encoding', 'identity')
                    req.add_header('Referer', article['url'])
                    r = urllib2.urlopen(req)
                    local_file = open(filename, "w")
                    local_file.write(r.read())
                    local_file.close()
                except IOError:
                    print "Well, that was a fail"
    if 'query.nytimes.com' in article['url']:
        the_split = article['url'].split("http://query.nytimes.com/")
        if len(the_split) > 1:
            filename = "texts/" + the_split[1].replace('/','_')
            if not os.path.isfile(filename):
                try:
                    req = urllib2.Request(article['url']+"&pagewanted=print")
                    req.add_header('Accept-Encoding', 'identity')
                    req.add_header('Referer', article['url'])
                    r = urllib2.urlopen(req)
                    local_file = open(filename, "w")
                    local_file.write(r.read())
                    local_file.close()
                except IOError:
                    print "Well, that was a fail"