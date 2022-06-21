from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLabel,
QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
QMessageBox, QApplication)
from PyQt5.QtGui import QPixmap
from os.path import join
from utils import params


class FinalWindow(QWidget):
    
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
        # Winner label
        
        # Set layout
        self.setLayout(self.center_layout)


    def show_winner(self, winner):
        self.winner_label = QLabel(f'Ha ganado {winner}!', self)
        self.winner_label.setObjectName('title')
        self.main_layout.addWidget(self.winner_label)
        self.show()

if __name__ == '__main__':

    app = QApplication([])
    window = FinalWindow()
    window.show()
    app.exec()