"""Serve the built site under the same project prefix as GitHub Pages."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'build/pages'
PREFIX = '/MyAlgorithmProblems'


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(302)
            self.send_header('Location', PREFIX + '/')
            self.end_headers()
            return
        parsed = urlsplit(self.path)
        if parsed.path.startswith(PREFIX + '/'):
            self.path = self.path[len(PREFIX):]
        elif parsed.path != '/favicon.ico':
            self.send_error(404)
            return
        super().do_GET()


if __name__ == '__main__':
    if not (ROOT / 'index.html').exists():
        raise SystemExit('Run python website/build.py first.')
    print('Local: http://127.0.0.1:8765/MyAlgorithmProblems/', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8765), partial(Handler, directory=str(ROOT))).serve_forever()
