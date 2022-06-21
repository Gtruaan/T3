'''
Contiene clase que guarda las casillas en orden como listas ligadas
'''


class Square():
    '''
    Casilla
    '''
    def __init__(self, col, row, next, is_color=False, is_victory=False, is_start=False):
        self.col = col
        self.row = row
        self.pos = (col, row)
        self.next = next
        self.is_color = is_color
        self.is_victory = is_victory
        self.is_start = is_start

    def get_end(self):
        current = self
        while current.next != None:
            current = current.next
        return current

class Board():
    '''
    Clase que ordena las casillas
    '''
    def __init__(self):
        '''
        pep8 goes brrrrrr
        '''
        self.blue_route = Square(0, 0, Square(1, 0, Square(2, 0, Square(3, 0, Square(4, 0, 
        Square(5, 0, Square(5, 1, Square(5, 2, Square(5, 3, Square(5, 4, Square(5, 5, 
        Square(4, 5, Square(3, 5, Square(2, 5, Square(1, 5, Square(0, 5, Square(0, 4, 
        Square(0, 3, Square(0, 2, Square(0, 1, Square(1, 1, Square(2, 1, Square(3, 1, None,
        is_victory=True), is_color=True), is_color=True)))))))))))))))))))), is_start=True)

        self.red_route = Square(0, 5, Square(0, 4, Square(0, 3, Square(0, 2, Square(0, 1, 
        Square(0, 0, Square(1, 0, Square(2, 0, Square(3, 0, Square(4, 0, Square(5, 0, 
        Square(5, 1, Square(5, 2, Square(5, 3, Square(5, 4, Square(5, 5, Square(4, 5, 
        Square(3, 5, Square(2, 5, Square(1, 5, Square(1, 4, Square(1, 3, Square(1, 2, None,
        is_victory=True), is_color=True), is_color=True)))))))))))))))))))), is_start=True)

        self.green_route = Square(5, 5, Square(4, 5, Square(3, 5, Square(2, 5, Square(1, 5, 
        Square(0, 5, Square(0, 4, Square(0, 3, Square(0, 2, Square(0, 1, Square(0, 0, 
        Square(1, 0, Square(2, 0, Square(3, 0, Square(4, 0, Square(5, 0, Square(5, 1, 
        Square(5, 2, Square(5, 3, Square(5, 4, Square(4, 4, Square(3, 4, Square(2, 4, None,
        is_victory=True), is_color=True), is_color=True)))))))))))))))))))), is_start=True)
        
        self.yellow_route = Square(5, 0, Square(5, 1, Square(5, 2, Square(5, 3, Square(5, 4, 
        Square(5, 5, Square(4, 5, Square(3, 5, Square(2, 5, Square(1, 5, Square(0, 5, 
        Square(0, 4, Square(0, 3, Square(0, 2, Square(0, 1, Square(0, 0, Square(1, 0, 
        Square(2, 0, Square(3, 0, Square(4, 0, Square(4, 1, Square(4, 2, Square(4, 3, None,
        is_victory=True), is_color=True), is_color=True)))))))))))))))))))), is_start=True)

    def color_start(self, color):
        '''
        Recibe un color y entrega la celda final
        '''
        if color == 'azul':
            return self.blue_route
        if color == 'roja':
            return self.red_route
        if color == 'verde':
            return self.green_route
        if color == 'amarilla':
            return self.yellow_route

    def color_end(self, color):
        '''
        Recibe un color y entrega la celda final
        '''
        if color == 'azul':
            return self.blue_route.get_end()
        if color == 'roja':
            return self.red_route.get_end()
        if color == 'verde':
            return self.green_route.get_end()
        if color == 'amarilla':
            return self.yellow_route.get_end()