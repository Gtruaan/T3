import json
import os


def clean_layout(layout):
    '''
    Elimina todos los widgets de un layout
    '''
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        elif child.layout():
            clean_layout(child)

def params(key):
    '''
    Lee parametros.json y entrega el parametro asociado a la llave
    '''
    path = os.path.join('parameters.json')

    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data[key]

def message_to_bytes(message_dict):
    '''
    Aplica el encoding especial a un diccionario y lo retorna
    '''
    encoded_dict = json.dumps(message_dict).encode('utf-8')
    return encoded_dict

def decode_message(message_bytes):
    '''
    Decodifica el mensaje y retorna un diccionario
    '''
    decoded_dict = json.loads(message_bytes.decode('utf-8'))
    return decoded_dict