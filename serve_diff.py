#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer

import sys
import difflib
import json
import argparse

differ = difflib.HtmlDiff(tabsize=2, wrapcolumn=100)

def process_dict_item(k, v):
    try:
        return k, int(v)
    except (TypeError, ValueError):
        if k == 'EbsOptimized' and v == 'true':
            return 'EbsOptimized', 1
        if k == 'NoEcho' and v == 'true':
            return 'NoEcho', 1
        return k, replace_quoted_ints_in_values(v)


def replace_quoted_ints_in_values(o):
    if isinstance(o, dict):
        return dict(process_dict_item(k, v) for k,v in o.items())
    elif isinstance(o, list):
        return list(replace_quoted_ints_in_values(l) for l in o)
    else:
        return o


def normalize_file(f, replace_ints=True):
    j = json.load(f)
    if replace_ints:
        j = replace_quoted_ints_in_values(j)
    return json.dumps(j, indent=2, sort_keys=True)


class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        replace_ints = not args.do_not_ignore_quoted_numbers
        s1, s2 = [normalize_file(open(f), replace_ints).splitlines() for f in (args.file1, args.file2)]
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(differ.make_file(s1,s2))
        return


if __name__ == '__main__':
    SocketServer.TCPServer.allow_reuse_address = True

    parser = argparse.ArgumentParser(description='Show differences between two json files, serve it per http.')
    parser.add_argument('--port', '-p', type=int, default=8000)
    parser.add_argument('--do-not-ignore-quoted-numbers', '-i', action='store_true',
                        help="Show boring changes like 500 -> \"500\"")

    parser.add_argument('file1')
    parser.add_argument('file2')

    args = parser.parse_args()

    print "serving on http://localhost:%d" % args.port
    httpd = SocketServer.TCPServer(("", args.port), Handler)
    httpd.serve_forever()
