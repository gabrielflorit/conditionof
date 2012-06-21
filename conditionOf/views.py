import urllib2
import re
import os
import datetime
import json
from conditionOf import app
from flask import render_template, send_from_directory, request
from werkzeug.contrib.atom import AtomFeed

nyt_api_key = "b8e7be8d6a606fa1101a581d8b39e426:17:63577998"
good_words = ['on', 'about', 'because', 'from', 'since', 'for', 'that', 'after', 'while', 'per', 'by', 'as', 'so', 'at', 'during', 'in', 'under', 'before', 'until', 'out']

def is_url_new(url):
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls_seen WHERE url=%s", (url,))
    result = cursor.fetchone()
    return (result == None)

def mark_url_seen(url):
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls_seen VALUES (%s)", (url,))
    conn.commit()

def add_reason(because, url):
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reasons (because, url) VALUES (%s,%s)", (because,url))
    conn.commit()

def get_reasons():
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reasons")
    return [{'id': x[0], 'reason': x[1], 'url':x[2]} for x in cursor.fetchall()]

@app.route('/init')
def init_db():
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE urls_seen")
    cursor.execute("DROP TABLE reasons")
    cursor.execute("CREATE TABLE urls_seen (url TEXT)")
    cursor.execute("CREATE TABLE reasons (id SERIAL, because TEXT, url TEXT)")
    conn.commit()
    headers.append(('Content-Type', 'application/json'))
    return json.dumps({"init":"success"})

@app.route('/reasons')
def getjson():
    headers.append(('Content-Type', 'application/json'))
    return json.dumps(get_reasons()) 
    
@app.route('/update')
def update():
    feed = AtomFeed('Recent Posts',feed_url=request.url, url=request.url_root)
    yesterday = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d")
    tomorrow = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y%m%d")
    fp = urllib2.urlopen("http://api.nytimes.com/svc/search/v1/article?format=json&query=%22condition+of+anonymity%22&begin_date="+yesterday+"&end_date="+tomorrow+"&rank=oldest&api-key="+nyt_api_key)
    obj = json.load(fp)
    for result in obj['results']:
        if is_url_new(result['url']):
            if "?" in result['url']:
                query_string = "&pagewanted=print"
            else:
                query_string = "?pagewanted=print"
            req = urllib2.Request(result['url']+query_string)
            req.add_header('Accept-Encoding', 'identity')
            req.add_header('Referer', result['url'])
            r = urllib2.urlopen(req)
            for line in r:
                after = re.sub("<[^>]+>","",line).split("condition of anonymity ")
                if (len(after) > 1):
                    if (after[1].split()[0] in good_words):
                        chunks = re.split(",|--|(?<!.Mr|.Ms|Mrs|.Dr|..[A-Z])\.",after[1])
                        reason = chunks[0]
                        add_reason(reason,result['url'])
                        feed.add(reason, reason,
			                content_type='html',
			                url=result['url'],
			                updated=datetime.datetime.now())
            mark_url_seen(result['url'])
            break
    return feed.get_response()

@app.route('/load', methods=['POST'])
def load():
    add_reason(request.form['because'], request.form['url'])
    headers.append(('Content-Type', 'application/json'))
    return {"load":"success"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
