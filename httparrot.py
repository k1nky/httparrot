#!/usr/bin/python3

import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import sys
import time
   
def get_args():
    
    parser = argparse.ArgumentParser(description="Simple HTTP echo server", prog="httparrot.py",
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=40))
    parser.add_argument("--port", "-p", 
                        type=int, default=[8000], action="store", nargs=1, help="server port, default 8000")
    parser.add_argument("--address", "-a", 
                        type=str, default=['localhost'], action="store", nargs=1, help="server address, default localhost")
    parser.add_argument("--echo", metavar="TYPE",
                        type=str, action="append", nargs='*', 
                        help="""echo types: 
                        headers - dump received headers,
                        body - dump received body,
                        query - dump request line,
                        none - no dump, default none
                        all - dump all, 
                        """,
                        choices=['all', 'headers', 'body', 'query', 'none'])
    parser.add_argument("--header", 
                        type=str, default="", action="store", nargs='*', help="extend response headers")
    parser.add_argument("--body", 
                        type=str, default="", action="store", nargs='*', help="extend response body")
    parser.add_argument("--status", "-s", 
                        type=int, default=[200], action="store", nargs=1, help="set response status, default 200")
    parser.add_argument("--version", "-v", 
                        type=str, default=['1.1'], action="store", nargs=1, help="set HTTP version, default - 1.1",
                        choices=['1.1','1.0','2'])
    parser.add_argument("--time", "-t", action="store_true", help="extend response body with current time")
    parser.add_argument("--silent", "-q", action="store_true", help="silent mode")
    
    return parser.parse_args()
    
def silent_mode(enabled):
    
    if enabled:
        dev_null = open('/dev/null', 'w')
        sys.stdout = dev_null
        sys.stderr = dev_null        

class HTTParrotHandler(BaseHTTPRequestHandler):
    
    config = {}
    
    check_opt_echo = lambda self, x: x in self.config['echo']
    parse_opt_header = lambda self, s: tuple( map(lambda x: x.replace(" ",""), s.split(":")) )

    def prepare_msg(self):
        
        msg = '';
        
        if self.check_opt_echo('all') or self.check_opt_echo('headers'):
            msg += str(self.headers)
        if self.check_opt_echo('all') or self.check_opt_echo('query'):
            msg += str(self.requestline) + "\n"
        if self.check_opt_echo('all') or self.check_opt_echo('body'):
            if 'Content-Length' in self.headers:
                msg += str(self.rfile.read(int(self.headers['Content-Length']))) + "\n"
                
        if self.config['time']:
            msg += str(int(time.time())) + "\n"
            
        for body in self.config['body']:
            msg += body + '\n'            
        
        return bytes(msg + "\n", 'utf-8')
        

    def do_respone(self):
        
        msg = self.prepare_msg();
        
        self.protocol_version = "HTTP/{}".format(self.config['version'])           
        self.send_response(self.config['status'])
        
        for header in self.config['header']:            
            self.send_header(*self.parse_opt_header(header))
                        
        self.send_header("Content-Length", len(msg))
        self.end_headers()
        self.wfile.write(msg)
        
    def do_error(self, e):
        
        self.send_response(500)
        msg = bytes("Internal exception {}".format(e), "utf-8")        
        self.send_header("Content-Length", len(msg))
        self.end_headers()
        self.wfile.write(msg)
                
    def do_HEAD(self):
        
        try:                        
            self.do_respone()
        except Exception as e:
            self.do_error(e)

    def do_PUT(self):
        
        try:                        
            self.do_respone()
        except Exception as e:
            self.do_error(e)
            
    def do_DELETE(self):
        
        try:                        
            self.do_respone()
        except Exception as e:
            self.do_error(e)
                        
    def do_POST(self):
        
        try:                        
            self.do_respone()
        except Exception as e:
            self.do_error(e)
    
    def do_GET(self):
        
        try:                        
            self.do_respone()
        except Exception as e:
            self.do_error(e)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    
    pass        

if __name__ == "__main__":
    
    args = get_args()    
    
    silent_mode(args.silent)

    httpd = ThreadedHTTPServer((args.address[0], args.port[0]), HTTParrotHandler)
    HTTParrotHandler.config = {
        'echo': args.echo[0],
        'header': args.header,
        'body': args.body,
        'time': args.time,
        'status': args.status[0],
        'version': args.version[0]
    }
    
    try:
        httpd.serve_forever()
    except:
        pass

    httpd.server_close()
