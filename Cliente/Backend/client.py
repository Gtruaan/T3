import socket
import json
from threading import Thread
import utils
from Backend.logic import Logic

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.id = 0
        self.client_socket = None
        self.connected = False
        self.logic = Logic(self)
        self.start_client()

    def start_client(self):
        '''
        Instancia el socket del cliente y lo conecta
        '''
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            message_manage_thread = Thread(target=self.start_receiving, daemon=True)
            message_manage_thread.start()
        except (ConnectionError, ConnectionRefusedError) as e:
            print('Ha ocurrido un error:', e)
    
    def start_receiving(self):
        '''
        Inicia thread del cliente que recibe mensajes del servidor. Enviar se hace por separado
        '''
        try:
            while self.connected:
                message = self.receive_message()
                if message:
                    self.logic.parse_message(message)
        except (ConnectionError) as e:
            print('Ha ocurrido un error:', e)

    def receive_message(self):
        '''
        Aplica decodificacion y entrega dict
        '''
        message_bytes = bytearray()
        len_message = int.from_bytes(self.client_socket.recv(4), byteorder='little')
        while len_message > len(message_bytes):
            message_bytes += self.client_socket.recv(
                min(64, len_message - len(message_bytes)))
        return utils.decode_message(message_bytes)

    def send_message(self, message):
        '''
        Aplica encoding en un dict y lo envia
        '''
        # TODO: Falta basicamente todo lo que tiene que ver con encriptacion y codificacion
        answer_bytes = utils.message_to_bytes(message)
        len_answer_bytes = len(answer_bytes).to_bytes(4, byteorder='little')
        self.client_socket.sendall(len_answer_bytes + answer_bytes)

