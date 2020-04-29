#!/usr/bin/python3

""" HTTParrot is http echo server which can be used when debugging, configure or testing your infrastructure.
    URL: https://github.com/k1nky/httparrot
"""

import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import sys
import time


class Message:

    def __init__(self):
        self.message = ''

    def add_line(self, data):
        self.message += str(data) + "\n"

    def to_binary(self):
        return bytes(self.message + "\n", 'utf-8')


class HTTParrotHandler(BaseHTTPRequestHandler):

    config = {}

    @classmethod
    def check_opt_echo(cls, option):
        return option in cls.config['echo']

    @staticmethod
    def parse_opt_header(header):
        return tuple(map(lambda x: x.replace(" ", ""), header.split(": ")))

    def prepare_msg(self):
        """ Prepare the response message """
        msg = Message()

        if self.check_opt_echo('all') or self.check_opt_echo('client'):
            msg.add_line(self.client_address)
        if self.check_opt_echo('all') or self.check_opt_echo('headers'):
            msg.add_line(self.headers)
        if self.check_opt_echo('all') or self.check_opt_echo('query'):
            msg.add_line(self.requestline)
        if self.check_opt_echo('all') or self.check_opt_echo('body'):
            if 'Content-Length' in self.headers:
                msg.add_line(self.rfile.read(int(self.headers['Content-Length'])))
        if self.config['time']:
            msg.add_line(int(time.time()))
        for body in self.config['body']:
            msg.add_line(body)

        return msg.to_binary()

    def do_response(self):
        """ Send the echo response """
        msg = self.prepare_msg()
        self.protocol_version = "HTTP/{}".format(self.config['version'])
        self.send_response(self.config['status'])
        
        for header in self.config['header']:            
            self.send_header(*self.parse_opt_header(header))
        self.send_header("Content-Length", len(msg))
        self.end_headers()

        self.wfile.write(msg)
        
    def do_error(self, e):
        """ Send error with HTTP code 500 """
        self.send_response(500)
        msg = bytes("Internal exception {}".format(e), "utf-8")        
        self.send_header("Content-Length", len(msg))
        self.end_headers()
        self.wfile.write(msg)
                
    def do_HEAD(self):
        """ Precess HEAD request """
        try:                        
            self.do_response()
        except Exception as e:
            self.do_error(e)

    def do_PUT(self):
        """ Precess PUT request """
        try:                        
            self.do_response()
        except Exception as e:
            self.do_error(e)
            
    def do_DELETE(self):
        """ Precess DELETE request """
        try:                        
            self.do_response()
        except Exception as e:
            self.do_error(e)
                        
    def do_POST(self):
        """ Precess POST request """
        try:                        
            self.do_response()
        except Exception as e:
            self.do_error(e)
    
    def do_GET(self):
        """ Precess GET request """
        try:                        
            self.do_response()
        except Exception as e:
            self.do_error(e)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def get_args():
    """ Parse run flags """
    parser = argparse.ArgumentParser(description="Simple HTTP echo server", prog="httparrot.py",
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40))
    parser.add_argument("--port", "-p",
                        type=int, default=[8000], action="store", nargs=1,
                        help="server port, default 8000")
    parser.add_argument("--address", "-a",
                        type=str, default=['localhost'], action="store", nargs=1,
                        help="server address, default localhost")
    parser.add_argument("--echo", metavar="TYPE", default=[],
                        type=str, action="append",
                        help="""echo types: 
                        headers - dump request headers,
                        body - dump request body,
                        query - dump request line,
                        client - dump client address and port,
                        none - no dump, default none
                        all - dump all, 
                        """,
                        choices=['all', 'headers', 'body', 'query', 'none'])
    parser.add_argument("--header",
                        type=str, default="", action="store", nargs='*',
                        help="extend response headers")
    parser.add_argument("--body",
                        type=str, default="", action="store", nargs='*',
                        help="extend response body")
    parser.add_argument("--status", "-s",
                        type=int, default=[200], action="store", nargs=1,
                        help="set response status, default 200")
    parser.add_argument("--version", "-v",
                        type=str, default=['1.1'], action="store", nargs=1,
                        help="set HTTP version, default - 1.1",
                        choices=['1.1', '1.0', '2'])
    parser.add_argument("--time", "-t", action="store_true",
                        help="extend response body with current time")
    parser.add_argument("--silent", "-q", action="store_true",
                        help="silent mode")

    return parser.parse_args()


def silent_mode(enabled):
    """ Enable silent mode """
    if enabled:
        dev_null = open('/dev/null', 'w')
        sys.stdout = dev_null
        sys.stderr = dev_null


if __name__ == "__main__":
    
    args = get_args()
    silent_mode(args.silent)

    httpd = ThreadedHTTPServer((args.address[0], args.port[0]), HTTParrotHandler)
    HTTParrotHandler.config = {
        'echo': args.echo,
        'header': args.header,
        'body': args.body,
        'time': args.time,
        'status': args.status[0],
        'version': args.version[0]
    }
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Bye")
    finally:
        httpd.server_close()
