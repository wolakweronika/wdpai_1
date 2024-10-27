import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type


# Define the request handler class by extending BaseHTTPRequestHandler.
# This class will handle HTTP requests that the server receives.
class SimpleRequestHandler(BaseHTTPRequestHandler):
    user_list = [{
        'first_name': 'Weronika',
        'last_name': 'Wolak',
        'role': 'tester'
    }]

    # Handle OPTIONS requests (used in CORS preflight checks).
    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        if self.path == "/":
            self.get_html()
        elif self.path == "/data":
            self.get_data()
        elif self.path == "/styles.css":
            self.get_css()
        elif self.path == "/logic.js":
            self.get_js()

    def get_html(self) -> None:
        filepath = os.path.join(os.path.dirname(__file__), '../nginx/ui_app/index.html')
        try:
            with open(filepath, 'r') as index_file:
                html_content = index_file.read().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(html_content)
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def get_css(self) -> None:
        filepath = os.path.join(os.path.dirname(__file__), '../nginx/ui_app/styles.css')
        try:
            with open(filepath, 'rb') as index_file:
                css_content = index_file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(css_content)
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def get_js(self) -> None:
        filepath = os.path.join(os.path.dirname(__file__), '../nginx/ui_app/logic.js')
        try:
            with open(filepath, 'rb') as index_file:
                js_content = index_file.read()
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(js_content)
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def get_data(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(SimpleRequestHandler.user_list).encode('utf-8'))

    def do_POST(self) -> None:
        content_type = self.headers.get('Content-Type')
        if content_type == 'application/json':
            content_length = int(self.headers['Content-Length'])  # Get the size of data
            post_data = self.rfile.read(content_length)  # Read the POST data
            
            try:
                # Decode the JSON data
                received_data = json.loads(post_data.decode('utf-8'))

                # Ensure required keys are present in the received data
                if 'privacy_policy' in received_data and 'role' in received_data:
                    privacy_policy_accepted = received_data["privacy_policy"] == "on"
                    correct_role = received_data['role'] in ["Manager", "Development Lead", "Product Designer", "CTO"]

                    if privacy_policy_accepted and correct_role:
                        SimpleRequestHandler.user_list.append({
                            'first_name': received_data["first_name"],
                            'last_name': received_data["last_name"],
                            'role': received_data["role"],
                        })
                        self.send_response(200)
                    else:
                        self.send_response(400)  # Invalid data
                else:
                    self.send_response(400)  # Missing fields
                self.end_headers()

            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid JSON')
        else:
            self.send_response(415)
            self.end_headers()
            self.wfile.write(b'Unsupported Media Type')

    def do_DELETE(self):
        try:
            user_index = int(self.path.split('/')[-1])  # Get the index from the URL
            if 0 <= user_index < len(self.user_list):
                del SimpleRequestHandler.user_list[user_index]
                self.send_response(200)
            else:
                self.send_response(404)  # If the index is out of range
        except ValueError:
            self.send_response(400)  # Invalid index format
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000
) -> None:
    server_address: tuple = ('', port)
    httpd: HTTPServer = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
