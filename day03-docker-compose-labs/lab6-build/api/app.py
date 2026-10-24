import os
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        app_env = os.getenv('APP_ENV', 'development')
        response = f'{{"status": "UP", "environment": "{app_env}", "version": "2.0"}}'

        self.wfile.write(response.encode('utf-8'))


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), SimpleHandler)
    print("API Server listening on port 8000...")
    server.serve_forever()
