import json
import socket
import threading
import utils
from logic import Logic

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.logic = Logic(self)  
        self.client_id = 0
        print('=' * 20 + '\nIniciando servidor...\n' + '=' * 20)
        self.start_server()

    def start_server(self):
        '''
        Instancia socket
        '''
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.running = True
        print(f'[i] Servidor conectado en puerto <{self.port}> y host <{self.host}>')
        self.start_accepting()

    def start_accepting(self):
        '''
        Inicia thread que acepta a clientes
        '''
        accepting_thread = threading.Thread(target=self.accept_loop, daemon=True)
        accepting_thread.start()

    def accept_loop(self):
        '''
        Ciclo principal del servidor. Corre como thread y acepta 
        conexiones de clientes
        '''
        while self.running:
            try:
                client_sock, ip_adr = self.server_socket.accept()
                print(f'Se conecta cliente desde direccion {ip_adr}')
                client_manage_thread = threading.Thread(target=self.client_connection, 
                args=(self.client_id, client_sock), daemon=True)
                client_manage_thread.start()
                self.client_id += 1
            except Exception as e:
                print('( ! ) Ha ocurrido un error en la conexion:\n', e)

    def client_connection(self, id, sock):
        '''
        Maneja ciclo de conexion con un cliente. Corre como thread
        e intercambia datos :)
        '''
        print(f'[i] Estableciendo conexion con cliente {id}')
        try:
            self.send_message({'command':'pong', 'id' : id}, sock)
            while self.running:
                message = self.receive_message(sock)
                if not message:
                    raise ConnectionResetError
                self.logic.parse_message(message, sock)
        except (ConnectionError, ConnectionResetError) as error:
            print(f'( ! ) Se ha perdido la conexion con el cliente {id}')
            self.logic.delete_client(id)
    
    def receive_message(self, sock):
        '''
        Aplica decodificacion y entrega dict
        '''
        message_bytes = bytearray()
        len_message = int.from_bytes(sock.recv(4), byteorder='little')
        while len_message > len(message_bytes):
            message_bytes += sock.recv(min(64, len_message - len(message_bytes)))
        return utils.decode_message(message_bytes)

    def send_message(self, message, sock):
        '''
        Aplica encoding en un dict y lo envia
        '''
        # TODO: Falta basicamente todo lo que tiene que ver con encriptacion y codificacion
        answer_bytes = utils.message_to_bytes(message)
        len_answer_bytes = len(answer_bytes).to_bytes(4, byteorder='little')
        sock.sendall(len_answer_bytes + answer_bytes)

    def send_to_list(self, message, connected_users_list):
        '''
        Me da flojera escribir esto una y otra vez. Manda un mensaje a todos los clientes
        '''
        for sock in map(lambda user : user['sock'], connected_users_list):
            self.send_message(message, sock)

