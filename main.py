from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class MCPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path != '/search':
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
            return

        query_params = parse_qs(parsed_path.query)
        query = query_params.get('query', [''])[0]
        search_path = query_params.get('path', ['/'])[0]

        if not query:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Query parameter is required"}')
            return

        result = []
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if query in file:
                    file_path = os.path.join(root, file)
                    file_info = {
                        "name": file,
                        "path": file_path,
                        "size": os.path.getsize(file_path),
                        "created": datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
                    }
                    result.append(file_info)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

if __name__ == '__main__':
    server_address = ('127.0.0.1', 5000)
    httpd = HTTPServer(server_address, MCPRequestHandler)
    print('Starting MCP server on port 5000...')
    httpd.serve_forever()

# Cline Configuration Example
cline_config = {
    "endpoint": "http://127.0.0.1:5000/search",
    "method": "GET",
    "params": {
        "query": "example",
        "path": "/"
    }
}
