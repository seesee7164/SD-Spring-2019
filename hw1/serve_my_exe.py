#!/usr/bin/python
"""
Simple HTTP server in python, that invokes an executable to handle requests.
Usage::
    ./serve_my_exe.py exe_name
where exe_name is the name of the compiled executable.
Send a POST request::
    curl -d "3ok" http://localhost:25100
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from subprocess import *
import sys

exe_name = ""

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        incoming_data = self.rfile.read(content_length)
	global exe_name
        (stdout, stderr) = Popen('./' + exe_name, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate(incoming_data)
        outgoing_data = stdout
        if len(stderr) > 0:
          outgoing_data = 'stderr: ' + stderr + chr(0) + outgoing_data
          print >> sys.stderr, stderr
        self._set_headers()
        self.wfile.write(outgoing_data)
        
def run(server_class=HTTPServer, handler_class=S, port=25100):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        # run(port=int(argv[1]))
	exe_name = argv[1]
        run()
    else:
	print "Usage: ./server_my_exe exe_name"
        # run()
