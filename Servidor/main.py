import sys
from server import Server
from utils import params

if __name__ == '__main__':

    host = params('HOST')
    port = params('PORT')

    server = Server(host, port)

    try:
        while True:
            input('[i] CTRL + C cierra el servidor\n')
    except KeyboardInterrupt:
        sys.exit()