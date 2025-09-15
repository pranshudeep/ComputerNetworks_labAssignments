import http.server
import socketserver
import hashlib
import os
import time
from email.utils import formatdate

PORT = 8080
FILE = "index.html"  

class CachingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == f"/{FILE}":
            try:
                with open(FILE, "rb") as f:
                    content = f.read()

                etag = hashlib.md5(content).hexdigest()

                last_modified = formatdate(
                    timeval=os.path.getmtime(FILE),
                    usegmt=True
                )

                if_none_match = self.headers.get("If-None-Match")
                if_modified_since = self.headers.get("If-Modified-Since")

                if if_none_match == etag or if_modified_since == last_modified:
                    self.send_response(304)
                    self.end_headers()
                    return

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("ETag", etag)
                self.send_header("Last-Modified", last_modified)
                self.end_headers()
                self.wfile.write(content)

            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        else:
            self.send_error(404, "Invalid Path")

with socketserver.TCPServer(("", PORT), CachingHandler) as httpd:
    print(f"Serving on http://localhost:{PORT}")
    httpd.serve_forever()
