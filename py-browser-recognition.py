import json
import time
import hashlib
import os.path

# from uuid import uuid4
from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

if os.path.exists('browsers.json'):
    with open('browsers.json') as data_file:
        data = json.load(data_file)
else:
    data = {}
    with open('browsers.json', 'w') as data_file:
        json.dump(data, data_file)
        data_file.close()

class Sighting(object):
    def __init__(self, req):
        self.timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
        self.ip = request.headers.get('X-Forwarded-For') or request.remote_addr


class Browser(object):
    def __init__(self, req, etag=None):
        ua = request.headers.get('User-Agent')
        self.type = ua if ua is not None else 'No user agent retrieved'

        sighting = Sighting(req)

        if etag:
            for k, v in data.iteritems():
                if k == etag:
                    data[etag]['seen'].append(sighting.__dict__)
        else:
            self.seen = [sighting.__dict__]

def handle_after_req(response):
    print 'headers: ', response.headers
    return response

app.after_request(handle_after_req)

@app.route('/')
def main():
    template = """
        <!doctype html>
            <html>
                <head></head>
                <body>
                    <div> Etag: 
                        {% if etag %} 
                            {{ etag }} 
                        {% else %}
                            None?
                        {% endif %}
                    </div>
                </body>
            </html>"""


    # etag = request.if_none_match
    etag = request.headers.get('If-None-Match')
    # request.headers.get('If-Modified-Since')
    if etag:
        resp = Response(render_template_string(template, etag=etag))
        resp.status_code = 304
        resp.set_etag(etag)
        # resp.cache_control.public = True
        # resp.cache_control.max_age = 31536000 # 365 days
        resp.expires = time.strptime('Tue, 15 Nov 2020 12:45:26', "%a, %d %b %Y %H:%M:%S")
        resp.last_modified = time.strptime('Tue, 15 Nov 1994 12:45:26', "%a, %d %b %Y %H:%M:%S")

        for k, v in data.iteritems():
            if k == etag:
                browser = Browser(request, etag)
                data[etag] = browser.__dict__
        

    else:
        etag = hashlib.sha1(request.remote_addr).hexdigest()
        resp = Response(render_template_string(template, etag=etag))
        resp.status_code = 200
        resp.set_etag(etag)
        # resp.cache_control.public = True
        # resp.cache_control.max_age = 63072000
        resp.expires = time.strptime('Tue, 15 Nov 2020 12:45:26', "%a, %d %b %Y %H:%M:%S")
        resp.last_modified = time.strptime('Tue, 15 Nov 1994 12:45:26', "%a, %d %b %Y %H:%M:%S")

        browser = Browser(request)
        data[etag] = browser.__dict__

    with open('browsers.json', 'w') as browsers:
        json.dump(data, browsers, indent=4)
        browsers.close()

    return resp