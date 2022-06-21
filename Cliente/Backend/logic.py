from PyQt5.QtCore import QObject, pyqtSignal
from Frontend.game_window import GameScreen
from Frontend.start_menu import StartMenu
from Frontend.waiting_room import WaitingRoom
from Frontend.final_window import FinalWindow
import sys

class Logic(QObject):
    '''
    Clase que modela la logica del cliente. Incluye la logica del 
    menu de inicio, juego y post-juego.
    '''
    signal_login_error = pyqtSignal(str)
    signal_login_succesful = pyqtSignal(str)
    signal_update_member_cards = pyqtSignal(list)
    signal_set_admin = pyqtSignal()
    signal_transfer_admin = pyqtSignal()
    signal_update_pieces = pyqtSignal(list)
    signal_update_turn = pyqtSignal(str)
    signal_update_member_stats = pyqtSignal(list)
    signal_open_game = pyqtSignal()
    signal_update_dice = pyqtSignal(int)

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.start_window = StartMenu()
        self.waiting_room = WaitingRoom()
        self.game_window = GameScreen()
        self.victory_window = FinalWindow()

        self.turn = False
        self.username = None

        # === Conexiones ventana de inicio ===
        self.start_window.signal_submit_username.connect(self.verify_login)
        self.signal_login_error.connect(self.start_window.show_popup)
        self.signal_login_succesful.connect(self.start_window.hide)
        self.signal_login_succesful.connect(self.waiting_room.show)
        self.signal_update_pieces.connect(self.game_window.render_pieces)
        self.signal_update_turn.connect(self.game_window.update_turn)
        self.signal_update_member_cards.connect(self.waiting_room.render_members)
        self.signal_set_admin.connect(self.waiting_room.set_admin)
        self.signal_open_game.connect(self.waiting_room.hide)
        self.signal_open_game.connect(self.game_window.show)
        self.signal_update_member_stats.connect(self.game_window.render_members)
        self.waiting_room.signal_start_game.connect(self.start)
        self.game_window.signal_roll_dice.connect(self.send_roll)
        self.signal_update_dice.connect(self.game_window.update_last_roll)
        self.signal_transfer_admin.connect(self.waiting_room.set_admin)
        # === Conexiones sala de espera ===
        # === Fin conexiones ===

    def parse_message(self, message):
        '''
        Esta funcion toma un mensaje en forma de diccionario, revisa que tipo de mensaje es y
        actualiza la interfaz acorde a la info.
        '''
        if message['command'] == 'pong':
            self.id = message['id']
        if message['command'] == 'vfu':
            self.receive_login_verification(message['status'], 
            message['username'], message['is_admin'])
        if message['command'] == 'udm':
            self.signal_update_member_cards.emit(message['users'])
        if message['command'] == 'gud':
            if message['winner']:
                self.game_window.hide()
                self.victory_window.show_winner(message['winner'])
                
            self.turn = False
            self.signal_open_game.emit()
            self.signal_update_pieces.emit(message['list'])
            self.signal_update_turn.emit(message['current_turn'])
            self.signal_update_dice.emit(message['last_roll'])
            self.generate_member_stats(message['list'], message['users_colors'])
            if message['current_turn'] == self.username:
                self.turn = True
        if message['command'] == 'nad':
            if self.username == message['username']:
                self.signal_transfer_admin.emit()

    def verify_login(self, username):
        '''
        Envia username al servidor y recibe respuesta de su validez
        '''
        print(f'VERIFYING USERNAME {username}\n')
        message_dict = {
            'command' : 'vfu',
            'client_id' : self.id,
            'username' : username
        }
        self.client.send_message(message_dict)

    def receive_login_verification(self, status, username, is_admin):
        '''
        Recibe estado de la verificacion del login. Esta puede ser:
        1) a // Aceptado! Se procede a la sala de espera
        2) i // Formato incorrecto. Se muestra pop-up del formato correcto
        3) u // Nombre ya ocupado. Se muestra
        4) f // sala de espera ya se encuentra llena
        5) o // Partida ya se encuentra en curso
        '''
        print('Isadmin', is_admin)
        # TODO: implementar partida en curso
        print(f'RECEIVED VERIFICATION {username} status {status}\n')
        if status == 'a':
            self.signal_login_succesful.emit(username)
            self.username = username
            if is_admin:
                self.signal_set_admin.emit()
        elif status == 'i':
            self.signal_login_error.emit('El nombre debe tener entre ' +
            '1 y 10 caracteres alfanumericos')
        elif status == 'u':
            self.signal_login_error.emit(f'El nombre "{username}" se encuentra ocupado')
        elif status == 'f':
            self.signal_login_error.emit('Se ha alcanzado el maximo de jugadores')
        elif status == 'o':
            self.signal_login_error.emit('Partida se encuentra en curso')

    def generate_member_stats(self, pieces_list, users_colors):
        '''
        Genera estadisticas de los miembros para mostrar durante el juego
        '''
        members = []
        turn = 1
        for color in users_colors:
            member_dict = {
                'username' : users_colors[color],
                'color' : color,
                'turn' : turn,
                'based' : 0,
                'near' : 0,
                'done' : 0
            }
            turn += 1
            for piece in filter(lambda piece : piece['color'].strip('e') == color, pieces_list):
                print(color, piece['position'], piece['in_start'])
                if piece['in_start']:
                    member_dict['based'] += int(piece['is_double']) + 1
                elif piece['in_color']:
                    member_dict['near'] += int(piece['is_double']) + 1
                elif piece['in_victory']:
                    member_dict['done'] += int(piece['is_double']) + 1
            members.append(member_dict)
            self.signal_update_member_stats.emit(members)
        
    def start(self):
        '''nose'''
        self.client.send_message({'command' : 'start'})

    def send_roll(self):
        '''
        Envia al server comando para tirar dado
        '''
        if self.turn:
            self.client.send_message({'command' : 'roll', 'username' : self.username})

        