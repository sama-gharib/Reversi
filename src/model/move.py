class Move:
    '''
        Represents a _valid_ move on board.
    '''

    def assert_bounds(v):
        if v < 0 or v > 7:
            raise ValueError('`Move` value should be between 0 and 7 (included).')

    def __init__(self, line = 0, column = 0):
        Move.assert_bounds(line)
        Move.assert_bounds(column)

        # Public attributes
        self.line = line
        self.column = column


    def to_compressed(self):
        '''
            Compresses self.line and self.column on 6 bits
        '''
        return (self.line << 3) + self.column

    def from_compressed(compressed):
        '''
            Reads from values from 6 bits 
        '''
        result = Move()
        result.line = compressed >> 3
        result.column = compressed - (result.line << 3)

        return result 

    def __repr__(self):
        return f"Token put at line {self.line} and column {self.column}"

if __name__ == '__main__':
    # Code de test

    c = Move(0, 7).to_compressed()
    m = Move.from_compressed(c)

    print(m)