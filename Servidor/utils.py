from base64 import encode
import json
from msilib import sequence
import os



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

def cbs(seq):
    '''
    Calcula suma de bytes centrales
    '''
    if len(seq) == 1:
        return seq[0]
    if len(seq) % 2 == 0:
        median = len(seq) // 2
        csum = seq[median - 1] + seq[median]
    else:
        median = (len(seq) - 1) // 2
        csum = seq[median] + (seq[median + 1] + seq[median - 1]) / 2
    return csum

def encryption(message):
    '''
    Toma un mensaje y lo encripta en una serie de bytes
    '''
    message_bytes = json.dumps(message).encode('utf-8')

    part_a = b''
    part_b = b''

    seq = 0
    cur = 0
    while len(part_a) + len(part_b) < len(message_bytes):
        if seq % 4 == 0:
            part_a += message_bytes[cur : cur + 1]
            cur += 1
        elif seq % 4 == 1:
            part_b += message_bytes[cur : cur + 1]
            cur += 1
        elif seq % 4 == 2:
            if len(message_bytes) - cur > 1:
                part_a += message_bytes[cur : cur + 2]
                cur += 2
            else:
                part_a += message_bytes[cur :]
        else:
            if len(message_bytes) - cur > 1:
                part_b += message_bytes[cur : cur + 2]
                cur += 2
            else:
                part_b += message_bytes[cur :]
        seq += 1

    if cbs(part_a) > cbs(part_b):
        return bytes([0]) + part_b + part_a
    else:
        return bytes([1]) + part_a + part_b

def encoding(bytes_message):
    '''
    Toma una serie de bytes y la codifica
    '''
    len_bytes = len(bytes_message)
    transformed = bytearray()
    counter = 0
    while len(transformed) < len_bytes:
        transformed += counter.to_bytes(4, byteorder='big')
        len_bytes += 4
        if len_bytes - len(transformed) >= 20:
            transformed += b'\x01' + (bytes([20]) 
            + bytes_message[counter * 20 : (counter + 1) * 20])
            len_bytes += 2
        else:
            transformed += b'\x00' + (bytes([len(bytes_message[counter * 20 :])])
            + bytes_message[counter * 20 :])
            len_bytes += 2
        counter += 1
    return counter.to_bytes(4, byteorder='little') + bytes(transformed)

def decoding(bytes_message):
    byte_sequence = bytearray()

    number_of_blocks = int.from_bytes(bytes_message[: 4], byteorder='little')
    cur = 9
    print(number_of_blocks)
    for i in range(number_of_blocks):
        number_of_bytes = bytes_message[cur]
        byte_sequence += bytes_message[cur + 1 : cur + 1 + number_of_bytes]
        cur += 4 + number_of_bytes

    return bytes(byte_sequence)

def decryption(byte_seq):
    '''
    Toma una serie de bytes y le aplica decripcion
    '''
    if byte_seq[0] == 1:
        cur = 3
        if len(byte_seq) <= 5:
            cur = 2
        print('seq1')
        while True:
            print(byte_seq[1 : cur])
            print(byte_seq[cur :])
            if (cbs(byte_seq[1 : cur]) <= cbs(byte_seq[cur :])
            and len(byte_seq[1 : cur]) - len(byte_seq[cur :]) <= 2):
                break
            cur += 1
        part_a = byte_seq[1 : cur]
        part_b = byte_seq[cur :]
        original_bytes = bytearray()
    else:
        cur = 3
        if len(byte_seq) <= 5:
            cur = 2
        print('seq2')
        while True:
            print(byte_seq[1 : cur])
            print(byte_seq[cur :])
            if (cbs(byte_seq[1 : cur]) < cbs(byte_seq[cur :])
            and len(byte_seq[1 : cur]) - len(byte_seq[cur :]) <= 2):
                break
            cur += 1
        part_b = byte_seq[1 : cur]
        part_a = byte_seq[cur :]
        original_bytes = bytearray()
    seq = 0
    cur_a = 0
    cur_b = 0
    while len(original_bytes) < len(part_a) + len(part_b):
        if seq % 4 == 0:
            original_bytes += part_a[cur_a : cur_a + 1]
            cur_a += 1
        elif seq % 4 == 1:
            original_bytes += part_b[cur_b : cur_b + 1]
            cur_b += 1
        elif seq % 4 == 2:
            original_bytes += part_a[cur_a : cur_a + 2]
            cur_a += 2
        else:
            original_bytes += part_b[cur_b : cur_b + 2]
            cur_b += 2
        seq += 1
    return bytes(original_bytes)
