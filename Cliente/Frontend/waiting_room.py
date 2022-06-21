from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLabel,
QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
QMessageBox, QApplication)
from PyQt5.QtGui import QPixmap
from os.path import join
from utils import params, clean_layout


class WaitingRoom(QWidget):

    # Signal para enviar username
    signal_start_game  = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        self.is_admin = False
        
        self.h, self.w = params('START_HEIGHT'), params('START_WIDTH')

        self.setGeometry(600, 200, self.w, self.h)
        self.setFixedSize(self.w, self.h)
        self.setWindowTitle('DCCasillas')
        self.setStyleSheet(open(join('Frontend', 'menu_style.truan')).read())
        
        self.generate_elements()
        
    def set_admin(self):
        '''
        Se llama si el usuario es el primero en entrar a la sala y por ende
        recibe los privilegios de empezar la partida
        '''
        self.start_game.setText('Iniciar partida')
        self.start_game.clicked.connect(self.start)

    def generate_elements(self):
        '''
        Genera todos los elementos y widgets de la ventana de espera
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
        # Texto superior
        sup_text_label = QLabel('Esperando a iniciar la partida', self)
        sup_text_label.setObjectName('title')
        self.main_layout.addWidget(sup_text_label)
        self.main_layout.addStretch(1)
        # Layout member cards
        self.label_member_cards = QLabel(self)
        self.label_member_cards.setObjectName('member_card_label')
        self.label_member_cards.setGeometry(self.w / 2 - 220, self.h / 2 - 135, 420, 270)
        self.member_cards_layout = QVBoxLayout()
        self.main_layout.addLayout(self.member_cards_layout)
        self.main_layout.addStretch(1)
        # Iniciar partida
        self.start_game = QPushButton('Esperando al administrador', self)
        self.main_layout.addWidget(self.start_game)
        # Set layout
        self.setLayout(self.center_layout)

    def start(self):
        '''
        Envia signal para empezar la partida
        '''
        self.signal_start_game.emit()

    def show_popup(self):
        '''
        Muestra ventana de error por falta de jugadores
        '''
        pop_up = QMessageBox()
        pop_up.about(self,'Error al ingresar', 'No hay suficientes jugadores')
        pop_up.show()

    def render_members(self, members):
        '''
        Muestra a los miembros actualmente en la sala de espera
        '''
        clean_layout(self.member_cards_layout)
        for member in members:
            member_card_layout = QHBoxLayout()
            name = QLabel(member['username'])
            name.setObjectName('member_card_text')
            member_card_layout.addWidget(name)
            color = QLabel(member['color'])
            color.setObjectName('member_card_text')
            member_card_layout.addWidget(color)
            piece_path = join('Sprites', 'Fichas', 
            'Simples', f'ficha-{member["color"]}.png')
            self.piece_image = QLabel(self)
            self.piece_image.setPixmap(QPixmap(piece_path))
            self.piece_image.setFixedSize(65, 50)
            self.piece_image.setScaledContents(True)
            member_card_layout.addWidget(self.piece_image)
            self.member_cards_layout.addLayout(member_card_layout)

if __name__ == '__main__':

    app = QApplication([])
    window = WaitingRoom()
    window.show()
   
    app.exec()