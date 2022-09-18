import http.server
from socketserver import ThreadingTCPServer
import random
import re
import time

# ----- Setting Begin -----

PORT = 8000
DOC_ROOT = "public" # DocumentRoot 

# delay setting
# [ path pattern regexp, handler, *handler params]
DELAY_SETTING = [
    [ '\/delay500\/.*', 500 ], # sleep 500 millisec
    [ '\/delay100_300\/.*', 100, 300 ], # sleep 100-300 millisec
    [ '\/delay10000\/.*', 10000 ], # sleep 10000 millisec
]

# exclude setting
# path pattern array
EXCLUDE_SETTING = [
    '.*\/?index\.html?',
    '.*\/$',
]

# ------ Setting End -----

def sleep_millisecond(method, path, *args):
    if len(args) == 1:
        delay = float(args[0]) / 1000.0
        # print('Delay Request: "%s %s", delay: %f' % (method, path, delay))
        time.sleep(delay)
        return delay
    elif len(args) == 2:
        delay = random.randrange(args[0], args[1]) / 1000.0
        # print('Delay Request: "%s %s", delay: %f' % (method, path, delay))
        time.sleep(delay)
        return delay
    return 0.0

class DelaySetting:
    def __init__(self, ptn, *handler_params):
        self.ptn = re.compile(ptn)
        self.handler = sleep_millisecond
        self.handler_params = handler_params
    def match(self, path):
        return self.ptn.match(path)
    def execute(self, method, path):
        return self.handler(method, path, *self.handler_params)


class DelayingHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    exclude_setting = []
    delay_setting = []

    @classmethod
    def Init(cls):
        for setting in DELAY_SETTING:
            DelayingHttpRequestHandler.delay_setting += [DelaySetting(*setting)]
        for ptn in EXCLUDE_SETTING:
            DelayingHttpRequestHandler.exclude_setting += [re.compile(ptn)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOC_ROOT, **kwargs)

    def is_exclude(self, path):
        for ptn in self.__class__.exclude_setting:
            if ptn.match(path):
                return True
        return False

    def log_message(self, format, *args):
        base = format % args
        print('%s delay:%f' % (base, self.delay))

    # CORS
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        self.delay = 0.0
        if not self.is_exclude(self.path):
            for setting in self.__class__.delay_setting:
                if setting.match(self.path):
                    self.delay = setting.execute("GET", self.path)
                    break
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

DelayingHttpRequestHandler.Init()

handler_object = DelayingHttpRequestHandler

ThreadingTCPServer.allow_reuse_address = True

# Star the server
with ThreadingTCPServer(("", PORT), handler_object) as server:
    server.serve_forever()
