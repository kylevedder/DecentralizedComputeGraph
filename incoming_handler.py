import threading
import requests
import pickle
from http.server import BaseHTTPRequestHandler, HTTPServer


class IncomingHandler:
    def __init__(self, address: str, port: int, callback):

        class StoppableHttpServer(HTTPServer):

            def serve_forever(self):
                self.stop = False
                while not self.stop:
                    self.handle_request()

        class Handler(BaseHTTPRequestHandler):

            def _set_response(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

            def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                callback_res = callback(pickle.loads(post_data))
                self._set_response()
                if callback_res is not None:
                    self.wfile.write(pickle.dumps(callback_res))

        server_address = (address, port)
        self.address = 'http://{}:{}'.format(address, port)
        self.httpd = StoppableHttpServer(server_address, Handler)
        self.thread = threading.Thread(target=self._run_server)

    def _run_server(self):
        try:
            print('Serve forever')
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        self.httpd.server_close()

    def start(self):
        self.thread.start()

    def stop(self):
        self.httpd.stop = True
        try:
            requests.post(url=self.address, data='')
        except:
            pass
        self.thread.join()
