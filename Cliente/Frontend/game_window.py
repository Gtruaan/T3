from PyQt5.QtCore import pyqtSignal, QRect
from PyQt5.QtWidgets import (QWidget, QLabel,
QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
QMessageBox, QApplication, QGridLayout)
from PyQt5.QtGui import QPixmap
from os.path import join
from utils import params, clean_layout


def coords_to_pixel(col, row):
    '''
    Ayuda para hacer placement de las estrellas y las piezas :)))
    '''
    return (50 + col * 67, 150 + row * 67)

class GameScreen(QWidget):

    signal_roll_dice  = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        self.h, self.w = params('GAME_HEIGHT'), params('GAME_WIDTH')
        self.pieces = set()
        self.occupied_spots = set()
        self.layout_pieces = QGridLayout()
        self.setGeometry(600, 200, self.w, self.h)
        self.setFixedSize(self.w, self.h)
        self.setWindowTitle('DCCasillas')
        self.setStyleSheet(open(join('Frontend', 'game_style.css')).read())
        
        self.generate_elements()

    def generate_elements(self):
        '''
        Genera todos los elementos y widgets de la ventana de juego
        '''
        # Top Layout bar
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.mid_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.mid_layout)
        self.main_layout.addStretch(10)
        # Board image
        board_path = join('Sprites', 'Juego', 'tablero.png')
        self.board = QLabel(self)
        self.board.setPixmap(QPixmap(board_path))
        self.board.setGeometry(50, 150, 402, 402)
        self.board.setScaledContents(True)
        # Dice layout
        dice_path = join('Sprites', 'Logos', 'dado.png')
        self.dice = QLabel(self)
        self.dice.setPixmap(QPixmap(dice_path))
        self.dice.setFixedSize(100, 100)
        self.dice.setScaledContents(True)
        self.roll_dice = QPushButton('Tirar dado', self)
        self.roll_dice.clicked.connect(self.roll)
        self.dice_number = QLabel('Numero obtenido: 0', self)
        self.dice_number.setObjectName('bigger_title')
        self.layout_dice = QHBoxLayout()
        self.layout_roll_dice = QVBoxLayout()
        self.layout_dice.addWidget(self.dice)
        self.layout_roll_dice.addStretch(1)
        self.layout_roll_dice.addWidget(self.roll_dice)
        self.layout_roll_dice.addWidget(self.dice_number)
        self.layout_roll_dice.addStretch(1)
        self.layout_dice.addLayout(self.layout_roll_dice)
        self.top_layout.addStretch(1)
        self.top_layout.addLayout(self.layout_dice)
        self.top_layout.addStretch(6)
        # Player bar
        self.player_bar_label = QLabel(self)
        self.player_bar_label.setGeometry(500, 50, self.w - 550, self.h - 100)
        self.player_bar_label.setObjectName('bar_background')
        self.player_bar_text = QLabel('Jugadores', self)
        self.player_bar_text.setObjectName('bigger_title')
        self.player_bar_text.setGeometry(540, 30, 200, 100)
        self.layout_player_bar = QVBoxLayout()
        self.mid_layout.addStretch(10)
        self.mid_layout.addLayout(self.layout_player_bar)
        self.mid_layout.addStretch(1)
        # Turn Label
        self.turn_label = QLabel('Jugador de turno: ninguno', self)
        self.turn_label.setObjectName('bigger_title')
        self.main_layout.addWidget(self.turn_label)
        # Logo
        logo_path = join('Sprites', 'Logos', 'logo.png')
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap(logo_path))
        self.logo.setGeometry(180, 290, 135, 110)
        self.logo.setScaledContents(True)
        # Stars PIDO PERDON POR ESTA PARTE Y LO MAL HECHA QUE ESTA PERO FUNCIONA
        star_path = join('Sprites', 'Juego', 'estrella.png')
        star1 = QLabel(self)
        star1.setPixmap(QPixmap(star_path))
        x, y = coords_to_pixel(1, 2)
        x, y = x + 12, y + 12
        star1.setGeometry(x, y, 40, 40)
        star1.setScaledContents(True)
        star2 = QLabel(self)
        star2.setPixmap(QPixmap(star_path))
        x, y = coords_to_pixel(3, 1)
        x, y = x + 12, y + 12
        star2.setGeometry(x, y, 40, 40)
        star2.setScaledContents(True)
        star3 = QLabel(self)
        star3.setPixmap(QPixmap(star_path))
        x, y = coords_to_pixel(4, 3)
        x, y = x + 12, y + 12
        star3.setGeometry(x, y, 40, 40)
        star3.setScaledContents(True)
        star4 = QLabel(self)
        star4.setPixmap(QPixmap(star_path))
        x, y = coords_to_pixel(2, 4)
        x, y = x + 12, y + 12
        star4.setGeometry(x, y, 40, 40)
        star4.setScaledContents(True)
        # Set layout
        self.setLayout(self.main_layout)

    def render_members(self, members):
        '''
        Similar al metodo en waiting_room, actualiza tarjetas de miembros
        '''
        clean_layout(self.layout_player_bar)
        for member in members:
            member_card_layout = QHBoxLayout()
            member_card_layout.addStretch(1)
            piece_path = join('Sprites', 'Fichas', 
            'Simples', f'ficha-{member["color"]}.png')
            self.piece_image = QLabel(self)
            self.piece_image.setPixmap(QPixmap(piece_path))
            self.piece_image.setFixedSize(80, 55)
            self.piece_image.setScaledContents(True)
            member_card_layout.addWidget(self.piece_image)
            info_layout = QVBoxLayout()
            name = QLabel(member['username'])
            name.setObjectName('title')
     
            info_layout.addWidget(name)
            info_layout.addWidget(QLabel(f'Turno: {member["turn"]}'))
            info_layout.addWidget(QLabel(f'Fichas en base: {member["based"]}'))
            info_layout.addWidget(QLabel(f'Fichas en color: {member["near"]}'))
            info_layout.addWidget(QLabel(f'Fichas en victoria: {member["done"]}'))
            
            member_card_layout.addLayout(info_layout)
            member_card_layout.addStretch(1)
            self.layout_player_bar.addLayout(member_card_layout)

    def render_pieces(self, piece_positions):
        '''
        Genera y posiciona las piezas en el tablero
        '''
        clean_layout(self.layout_pieces)
        for piece in piece_positions:
            if piece['is_double']:
                # TODO: NECESITO AGREGARLE UNA E AL AZUL EN EL BACKEND XDDD
                piece_path = join('Sprites', 'Fichas', 
                'Dobles', f'fichas-{piece["color"]}s.png')
            else:
                piece_path = join('Sprites', 'Fichas', 
                'Simples', f'ficha-{piece["color"]}.png')
            piece_label = QLabel(self)
            self.layout_pieces.addWidget(piece_label)
            piece_label.setPixmap(QPixmap(piece_path))
            x, y = piece['position']
            x, y = coords_to_pixel(x, y)
            piece_label.setGeometry(x, y, 66, 66)
            piece_label.setScaledContents(True)
            self.pieces.add(piece_label)
            piece_label.show()

    def update_turn(self, username):
        '''
        actualiza display del turno
        '''
        self.turn_label.setText(f'Jugador de turno: {username}')

    def roll(self):
        self.signal_roll_dice.emit()

    def update_last_roll(self, last_roll):
        self.dice_number.setText(f'Numero obtenido: {last_roll}')


if __name__ == '__main__':

    app = QApplication([])
    window = GameScreen()
    window.show() 
            
    app.exec()