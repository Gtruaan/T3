import sys
from Backend.client import Client
from PyQt5.QtWidgets import QApplication
from utils import params


if __name__ == '__main__':
    host = params('HOST')
    port = params('PORT')
    
    app = QApplication(sys.argv)
     
    client = Client(host, port)
    
    sys.exit(app.exec())
    

   