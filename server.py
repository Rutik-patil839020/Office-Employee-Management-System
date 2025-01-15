import json
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer

conn = psycopg2.connect(
    host="localhost",
    database="Rutik",
    user="postgres",
    password="1234"
)
cursor = conn.cursor()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-type', content_type)

        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        if self.path == '/api/videos':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            title = data.get('title')
            category = data.get('category')
            mobile = data.get('mobile')
            email = data.get('email')
            url = data.get('url')
            description = data.get('description')

            if title and category and mobile and email and url and description:
                try:
                    cursor.execute(
                        "INSERT INTO youtube (title, category, mobile, email, url, description) VALUES (%s, %s, %s, %s, %s, %s)",
                        (title, category, mobile, email, url, description)
                    )
                    conn.commit()

                    self._set_headers()
                    response = {'message': 'Data stored successfully'}
                    self.wfile.write(json.dumps(response).encode('utf-8'))

                except Exception as e:
                    print(f"Database error: {e}")
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'message': 'Error storing data'}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'message': 'Invalid input data'}
                self.wfile.write(json.dumps(response).encode('utf-8'))

# Start server
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
