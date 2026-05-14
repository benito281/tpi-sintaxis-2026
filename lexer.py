import ply.lex as lex


class LexerTokens:
    reserved = {
        'when': 'WHEN', 'do': 'DO', 'end': 'END', 'if': 'IF',
        'then': 'THEN', 'else': 'ELSE', 'every': 'EVERY',
        'and': 'AND', 'or': 'OR', 'not': 'NOT',
        'true': 'TRUE', 'false': 'FALSE', 'on': 'ON', 'off': 'OFF',
        'send_email': 'SEND_EMAIL', 'to': 'TO'
    }

    tokens = [
        'ID_SENSOR', 'ID_ACTUADOR', 'ATRIBUTO', 
        'VAL_TEMPERATURA', 'VAL_PORCENTAJE', 'VAL_TIEMPO', 
        'VAL_FECHA', 'VAL_HORA', 'VAL_EMAIL', 'VAL_TEXTO', 'VAL_LUX', 'NUM',
        'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE', 'ASSIGN', 'DOT',
        'LPAREN', 'RPAREN'
    ] + list(reserved.values())

    # Operadores y Puntuación
    t_EQ     = r'=='
    t_NEQ    = r'!='
    t_GTE    = r'>='
    t_LTE    = r'<='
    t_GT     = r'>'
    t_LT     = r'<'
    t_ASSIGN = r'='
    t_DOT    = r'\.'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ignore = ' \t'

    def t_COMENTARIO(self, t):
        r'//.*'
        pass

    def t_VAL_EMAIL(self, t):
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'
        print('\n-> Token específico encontrado: EMAIL')
        return t

    def t_VAL_FECHA(self, t):
        r'\d{1,2}/\d{1,2}/\d{4}'
        print('\n-> Token específico encontrado: FECHA')
        return t

    def t_VAL_HORA(self, t):
        r'\d{2}:\d{2}'
        print('\n-> Token específico encontrado: HORA')
        return t

    def t_VAL_TEMPERATURA(self, t):
        r'-?\d+°C'
        print('\n-> Token específico encontrado: TEMPERATURA')
        return t

    def t_VAL_PORCENTAJE(self, t):
        r'\d+%'
        print('\n-> Token específico encontrado: PORCENTAJE')
        return t

    def t_VAL_LUX(self, t):
        r'\d+lux'
        print('\n-> Token específico encontrado: LUMINOSIDAD')
        return t

    def t_VAL_TIEMPO(self, t):
        r'\d+[smh]'
        print('\n-> Token específico encontrado: TIEMPO')
        return t

    def t_VAL_TEXTO(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        t.value = t.value[1:-1]
        print('\n-> Token específico encontrado: TEXTO')
        return t

    def t_NUM(self, t):
        r'\d+'
        t.value = int(t.value)
        print('\n-> Token específico encontrado: NUM')
        return t

    def t_ID_SENSOR(self, t):
        r'sensor_[a-zA-Z0-9_]+'
        print('\n-> Token específico encontrado: ID_SENSOR')
        return t

    def t_ID_ACTUADOR(self, t):
        r'(foco_|aire_|persiana_|cerradura_|altavoz_|alarma_)[a-zA-Z0-9_]*'
        print('\n-> Token específico encontrado: ID_ACTUADOR')
        return t

    def t_ATRIBUTO(self, t): 
        r'[a-zA-Z][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value.lower(), 'ATRIBUTO')
        print('\n-> Token específico encontrado: ATRIBUTO o RESERVADA')
        return t

    # Manejo de errores.
    def t_error(self, t):
        last_cr = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
        line = t.lexer.lineno
        col = t.lexpos if last_cr < 0 else t.lexpos - last_cr - 1
        print(f"Caracter ilegal '{t.value[0]}' en línea {line}, columna {col}")
        t.lexer.skip(1)

    # Construir el lexer.
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Método de prueba.
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(f'---> Token simple encontrado: {tok.type}')
