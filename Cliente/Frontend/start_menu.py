from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLabel,
QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
QMessageBox, QApplication)
from PyQt5.QtGui import QPixmap
from os.path import join
from utils import params


class StartMenu(QWidget):

    # Signal para enviar username
    signal_submit_username  = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()

        self.h, self.w = params('START_HEIGHT'), params('START_WIDTH')

        self.setGeometry(600, 200, self.w, self.h)
        self.setFixedSize(self.w, self.h)
        self.setWindowTitle('DCCasillas')
        self.setStyleSheet(open(join('Frontend', 'menu_style.truan')).read())
        
        self.generate_elements()

    def generate_elements(self):
        '''
        Genera todos los elementos y widgets de la ventana de inicio
        '''
        # Background image
        bg_path = join('Sprites', 'Logos', 'fondo.png')
        self.background_image = QLabel(self)
        self.background_image.setPixmap(QPixmap(bg_path))
        self.background_image.setGeometry(0, 0, self.w, self.h)
        self.background_image.setScaledContents(True)
        # Main layout
        self.main_layout = QVBoxLayout()
        self.center_layout = QHBoxLayout()
        self.center_layout.addStretch(1)
        self.center_layout.addLayout(self.main_layout)
        self.center_layout.addStretch(1)
        # Logo
        logo_path = join('Sprites', 'Logos', 'logo.png')
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap(logo_path))
        self.logo.setFixedSize(270, 225)
        self.logo.setScaledContents(True)
        self.main_layout.addWidget(self.logo)
        # Username layout
        self.username_layout = QVBoxLayout()
        self.main_layout.addLayout(self.username_layout)
        # Username edit
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText('Ingresa tu nombre')
        self.username_layout.addWidget(self.username_field)
        # Username submit
        self.username_submit = QPushButton('Jugar', self)
        self.username_layout.addWidget(self.username_submit)
        # Set layout
        self.setLayout(self.center_layout)
        # Conexion username submit
        self.username_submit.clicked.connect(self.submit)
        # Show
        self.show()

    def submit(self):
        '''
        Envia login al back-end para que se procese
        '''
        username = self.username_field.text()
        self.signal_submit_username.emit(username)

    def show_popup(self, text):
        '''
        Muestra error
        '''
        pop_up = QMessageBox()
        pop_up.about(self,'Error al ingresar', text)
        pop_up.show()
        
    def show_waiting_room(self, username):
        '''
        Pasa a la sala de espera
        '''
        self.hide()

if __name__ == '__main__':

    app = QApplication([])
    window = StartMenu()
    window.show()
    app.exec()