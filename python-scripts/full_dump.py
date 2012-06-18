#/usr/bin/python

import time
import urllib2
import json

out_array = []

api_key = #needs an article search API key from developer.nytimes.com

def fetch_offset(offset):
    try:
        return urllib2.urlopen("http://api.nytimes.com/svc/search/v1/article?format=json&query=%22condition+of+anonymity%22&begin_date=20000101&end_date=20121010&rank=oldest&offset="+str(offset)+"&api-key="+api_key)
    except urllib2.HTTPError:
    	print "Retrying"
        return fetch_offset(offset)

offset = 0

for offset in range(73):
    fp = fetch_offset(offset)
    obj = json.load(fp)
    for item in obj["results"]:
        out_array.append(item)
    print len(out_array)
    time.sleep(0.1)

outfile = open("query_results.json",'w')
json.dump(out_array,outfile)


