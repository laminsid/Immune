#!/usr/bin/env python3
"""Run ImmuneErrorRadar GitHub Research Workbench locally.
No external dependencies. Opens http://127.0.0.1:8501/web/ .
"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import webbrowser, argparse, os

ROOT = Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, default=8501)
    ap.add_argument('--no-browser', action='store_true')
    args=ap.parse_args()
    url=f'http://{args.host}:{args.port}/web/'
    print('ImmuneErrorRadar Research Workbench')
    print('Root:', ROOT)
    print('URL :', url)
    print('Boundary: research use only; not clinical; not medical device.')
    if not args.no_browser:
        try: webbrowser.open(url)
        except Exception: pass
    ThreadingHTTPServer((args.host,args.port), Handler).serve_forever()
if __name__=='__main__': main()
