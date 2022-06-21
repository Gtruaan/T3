from turtle import update
from utils import params
import random
from board import Board


class Logic:

    def __init__(self, server):
        self.server = server
        self.colors = ['roja', 'amarilla', 'verde', 'azul']
        self.board = Board()
        self.connected_users = []
        self.pieces = {}
        self.current_turn = 0
        self.last_roll = 0
        self.ongoing = False
        self.winner = None
        self.users_colors = None

    def parse_message(self, message, sock):
        '''
        Esta funcion toma un mensaje en forma de diccionario, revisa que tipo de mensaje es y
        procesa la informacion. Debe retornar un mensaje para enviarse.
        '''
        if message['command'] == 'vfu':
            self.process_username(message['username'], message['client_id'], sock)
        if message['command'] == 'start':
            if len(self.connected_users) >= params('MIN_JUGADORES'):
                self.start_game()
        if message['command'] == 'roll':
            if message['username'] == self.connected_users[self.current_turn]['username']:
                self.move()

    def process_username(self, username, id, sock):
        '''
        Procesa validez del username
        '''
        print(username, id)
        verification_dict = {
            'command' : 'vfu',
            'username' : username,
            'is_admin' : False
        }
        if username.lower() in map(lambda user : user['username'].lower(), self.connected_users):
            verification_dict['status'] = 'u'
            self.server.send_message(verification_dict, sock)
        elif len(username) not in range(1, 11) or not username.isalnum():
            verification_dict['status'] = 'i'
            self.server.send_message(verification_dict, sock)
            print(f'[i] Cliente {id} ha tratado de ingresar un nombre en formato incorrecto')
        elif len(self.connected_users) == params('MAX_JUGADORES'):
            verification_dict['status'] = 'f'
            self.server.send_message(verification_dict, sock)
            print(f'[i] Cliente {id} ha tratado de ingresar a una sala llena')
        elif self.ongoing:
            verification_dict['status'] = 'o'
            self.server.send_message(verification_dict, sock)
            print(f'[i] Cliente {id} ha tratado de ingresar a una partida ya iniciada')
        else: # Asigns random color
            verification_dict['status'] = 'a'
            random.shuffle(self.colors)
            user = {'sock' : sock,
                    'username' : username,
                    'id' : id,
                    'color' : self.colors.pop(random.randint(0, len(self.colors) - 1)),
                }
            print(f'[i] Cliente {id} ha entrado a la sala de espera. Nombre de usuario: {username}')
            if not any(map(lambda user : user['is_admin'], self.connected_users)):
                # TODO: Mecanismo para transferir admin
                user['is_admin'] = True
                verification_dict['is_admin'] = True
                print(f'[i] Cliente {id} ha recibido privilegios de administrador')
            else:
                user['is_admin'] = False
            self.connected_users.append(user)
            self.server.send_message(verification_dict, sock)
            wait_room = {'command' : 'udm', 'users' : []}
            for i, user in enumerate(self.connected_users):
                wait_room['users'].append({'username' : user['username'], 'color' : user['color']})
            self.server.send_to_list(wait_room, self.connected_users)
            if len(self.connected_users) == params('MAX_JUGADORES'):
                self.start_game()
            
    def start_game(self):
        '''
        Coloca piezas en las posiciones iniciales y inicia estadisticas de cada jugador
        '''
        print('<#> Se ha iniciado una partida. Jugadores:')
        
        self.ongoing = True
        self.users_colors = {}
        for user in self.connected_users:
            print(user['username'], end=' ')
            color = user['color']
            self.pieces[color] = [self.board.color_start(color), self.board.color_start(color)]
            self.users_colors[color] = user['username']
        print()
        current_turn = self.connected_users[self.current_turn]['username']
        print(f'<#> Turno de {current_turn}')
        game_update = {
            'command' : 'gud',
            'list' : self.pack_pieces(),
            'current_turn' : current_turn,
            'users_colors' : self.users_colors,
            'last_roll' : self.last_roll,
            'winner' : self.winner
        }
        self.server.send_to_list(game_update, self.connected_users)
    
    def pack_pieces(self):
        '''
        Ordena los estados de las piezas para mandarlo como una lista al cliente
        '''
        piece_list = []
        for color in self.pieces:
            if self.pieces[color][0].pos == self.pieces[color][1].pos:
                isvictory = self.pieces[color][0].is_victory
                isstart = self.pieces[color][0].is_start
                iscolor = self.pieces[color][0].is_start
                if color == 'azul':
                    piece_list.append({'color' : 'azule', 
                    'position' : self.pieces[color][0].pos,
                    'is_double' : True, 'in_start' : isstart, 
                    'in_color' : iscolor, 'in_victory' : isvictory})
                else:
                    piece_list.append({'color' : color, 
                    'position' : self.pieces[color][0].pos,
                    'is_double' : True, 'in_start' : isstart, 
                    'in_color' : iscolor, 'in_victory' : isvictory})
            else:
                isvictory = self.pieces[color][0].is_victory
                isstart = self.pieces[color][0].is_start
                iscolor = self.pieces[color][0].is_start
                piece_list.append({'color' : color, 
                    'position' : self.pieces[color][0].pos,
                    'is_double' : False, 'in_start' : isstart, 
                    'in_color' : iscolor, 'in_victory' : isvictory})
                isvictory = self.pieces[color][1].is_victory
                isstart = self.pieces[color][1].is_start
                iscolor = self.pieces[color][1].is_start
                piece_list.append({'color' : color, 
                    'position' : self.pieces[color][1].pos,
                    'is_double' : False, 'in_start' : isstart, 
                    'in_color' : iscolor, 'in_victory' : isvictory})
        return piece_list
    
    def move(self):
        roll = random.randint(1, 3)
        current_user = self.connected_users[self.current_turn]
        print(f'<#> {current_user["username"]} lanza el dado, ' + 
        f'obtiene un {roll}, avanza esa cantidad de pasos')
        color = current_user['color']
        if not self.pieces[color][0].is_victory:
            old_position = self.pieces[color][0]
            for i in range(roll):
                self.pieces[color][0] = self.pieces[color][0].next
                if i + 1 != roll and self.pieces[color][0].is_victory:
                    self.pieces[color][0] = old_position
                    print(f'<#> {current_user["username"]} choca con el final y se queda donde estaba')
                    break
            for other_color in filter(lambda other_color : other_color != color, self.pieces):
                for j in range(len(self.pieces[other_color])):
                    if self.pieces[other_color][j].pos == self.pieces[color][0].pos:
                        self.pieces[other_color][j] = self.board.color_start(other_color)
                        print(f'<#> {current_user["username"]} se come una pieza de color {other_color}')
        elif not self.pieces[color][1].is_victory:
            old_position = self.pieces[color][1]
            for i in range(roll):
                self.pieces[color][1] = self.pieces[color][1].next
                if i + 1 != roll and self.pieces[color][1].is_victory:
                    self.pieces[color][1] = old_position
                    print(f'<#> {current_user["username"]} choca con el final y se queda donde estaba')
                    break
            for other_color in filter(lambda other_color : other_color != color, self.pieces):
                for j in range(len(self.pieces[other_color])):
                    if self.pieces[other_color][j].pos == self.pieces[color][1].pos:
                        self.pieces[other_color][j] = self.board.color_start(other_color)
                        print(f'<#> {current_user["username"]} se come una pieza de color {other_color}')
        self.last_roll = roll
        if self.pieces[color][1].is_victory:
            self.winner = color
            print(f'<#> {self.winner} ha ganado!')
        self.current_turn += 1
        self.current_turn %= len(self.connected_users)
        game_update = {
            'command' : 'gud',
            'list' : self.pack_pieces(),
            'current_turn' : self.connected_users[self.current_turn]['username'],
            'users_colors' : self.users_colors,
            'last_roll' : self.last_roll,
            'winner' : self.winner
        }
        print(f'<#> Turno de {self.connected_users[self.current_turn]["username"]}')
        self.server.send_to_list(game_update, self.connected_users)
    
    def delete_client(self, id):
        '''
        Elimina cliente y transfiere admin a otro de ser necesario
        '''
        for user in self.connected_users:
            if user['id'] == id:
                user_is_admin = user['is_admin']
                self.colors.append(user['color'])
                self.connected_users.remove(user)
                if len(self.connected_users) == 1:
                        self.winner = self.connected_users[0]
                        if self.ongoing:
                            update_message = {
                                'command' : 'gud',
                                'list' : self.pack_pieces(),
                                'current_turn' : self.connected_users[self.current_turn]['username'],
                                'users_colors' : self.users_colors,
                                'last_roll' : self.last_roll,
                                'winner' : self.winner
                            }
                            self.server.send_message(update_message, self.connected_users[0]['sock'])
                if user_is_admin:
                    self.connected_users[0]['is_admin'] = True
                    self.server.send_to_list({'command' : 'nad', 
                    'username' : self.connected_users[0]['username']}, self.connected_users)
                if self.ongoing:
                    update_message = {
                        'command' : 'gud',
                        'list' : self.pack_pieces(),
                        'current_turn' : self.connected_users[self.current_turn]['username'],
                        'users_colors' : self.users_colors,
                        'last_roll' : self.last_roll,
                        'winner' : self.winner
                    }
                else:
                    update_message = {'command' : 'udm', 'users' : []}
                    for i, user in enumerate(self.connected_users):
                        update_message['users'].append({'username' : user['username'], 'color' : user['color']})
                self.server.send_to_list(update_message, self.connected_users)
                    


                





