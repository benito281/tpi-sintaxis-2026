import ply.lex as lex


class LexerTokens:

    # Palabras reservadas 
    reserved = {
        'when': 'WHEN', 'do': 'DO', 'end': 'END', 'if': 'IF',
        'then': 'THEN', 'else': 'ELSE', 'every': 'EVERY',
        'and': 'AND', 'or': 'OR', 'not': 'NOT',
        'true': 'TRUE', 'false': 'FALSE', 'on': 'ON', 'off': 'OFF',
        'frio': 'FRIO', 'calor': 'CALOR', 'vent': 'VENT',
        'blanco': 'BLANCO', 'rojo': 'ROJO', 'azul': 'AZUL',
    }

    # Atributos
    atributos = {
        'estado':       'ATTR_ESTADO',
        'brillo':       'ATTR_BRILLO',
        'color':        'ATTR_COLOR',
        'modo':         'ATTR_MODO',
        'temp_obj':     'ATTR_TEMP_OBJ',
        'temp_act':     'ATTR_TEMP_ACT',
        'posicion':     'ATTR_POSICION',
        'hora':         'ATTR_HORA',
        'fecha':        'ATTR_FECHA',
        'volumen':      'ATTR_VOLUMEN',
        'mute':         'ATTR_MUTE',
        'mensaje':      'ATTR_MENSAJE',
        'email_notif':  'ATTR_EMAIL_NOTIF',
        'activada':     'ATTR_ACTIVADA',
    }

    # tokens.
    tokens = [
        # Sensores 
        'ID_SENS_TEMP', 'ID_SENS_LUZ', 'ID_SENS_HUMEDAD', 'ID_SENS_BOOL',
        # Actuadores 
        'ID_FOCO', 'ID_AIRE', 'ID_PERSIANA', 'ID_CERRADURA',
        'ID_RELOJ', 'ID_ALTAVOZ', 'ID_ALARMA',
        # Literales con unidad 
        'VAL_TEMPERATURA', 'VAL_PORCENTAJE', 'VAL_TIEMPO',
        'VAL_FECHA', 'VAL_HORA', 'VAL_EMAIL', 'VAL_TEXTO',
        'VAL_LUX', 'NUM',
        # Operadores y puntuación
        'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE', 'ASSIGN', 'DOT',
        'LPAREN', 'RPAREN',
    ] + list(set(atributos.values())) + list(reserved.values())

    # Operadores y delimitadores simples
  
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
    t_ignore = ' \t\r'

  
    # Comentarios 
    def t_COMENTARIO(self, t):
        r'/\*[\s\S]*?\*/|//[^\n]*|@[^\n]*'
        t.lexer.lineno += t.value.count('\n')
        pass
    # Salto de linea
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)



    def t_VAL_EMAIL(self, t):
        r'[a-zA-Z0-9_+\-]+(\.[a-zA-Z0-9_+\-]+)*@+[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,4}'

        if "@@" in t.value:
            print(f"Error léxico línea {t.lexer.lineno}: email con doble arroba en '{t.value}'")
            return None

        return t

    def t_VAL_FECHA(self, t):
        r'\d{1,2}/\d{1,2}/\d{4}'
        dia, mes, anio = (int(x) for x in t.value.split('/'))
        if not (1 <= dia <= 31):
            print(f"Error léxico línea {t.lexer.lineno}: día fuera de rango (1-31) en '{t.value}'")
            return None
        if not (1 <= mes <= 12):
            print(f"Error léxico línea {t.lexer.lineno}: mes fuera de rango (1-12) en '{t.value}'")
            return None
        if not (1900 <= anio <= 2099):
            print(f"Error léxico línea {t.lexer.lineno}: año fuera de rango (1900-2099) en '{t.value}'")
            return None
        return t

    def t_VAL_HORA(self, t):
        r'\d{2}:\d{2}'
        hh, mm = (int(x) for x in t.value.split(':'))
        if not (0 <= hh <= 23):
            print(f"Error léxico línea {t.lexer.lineno}: hora fuera de rango (00-23) en '{t.value}'")
            return None
        if not (0 <= mm <= 59):
            print(f"Error léxico línea {t.lexer.lineno}: minutos fuera de rango (00-59) en '{t.value}'")
            return None
        return t

    def t_VAL_TEMPERATURA(self, t):
        r'-?\d+(\.\d+)?°[Cc]'
        valor = float(t.value[:-2])  # quita °C
        if not (-10 <= valor <= 50):
            print(f"Error léxico línea {t.lexer.lineno}: temperatura fuera de rango (-10 a 50) en '{t.value}'")
            return None
        return t

    def t_VAL_PORCENTAJE(self, t):
        r'\d{1,3}%'
        valor = int(t.value[:-1])  # quita %
        if not (0 <= valor <= 100):
            print(f"Error léxico línea {t.lexer.lineno}: porcentaje fuera de rango (0-100) en '{t.value}'")
            return None
        return t

    def t_VAL_LUX(self, t):
        r'\d+lux'
        valor = int(t.value[:-3])  # quita 'lux'
        if not (0 <= valor <= 1000):
            print(f"Error léxico línea {t.lexer.lineno}: lux fuera de rango (0-1000) en '{t.value}'")
            return None
        return t

    def t_VAL_TIEMPO(self, t):
        r'\d+[smh]'
        return t

    def t_VAL_TEXTO(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        t.value = t.value[1:-1]
        return t

    def t_NUM(self, t):
        r'\d+'
        t.value = int(t.value)
        return t


    # Sensores
    def t_ID_SENS_TEMP(self, t):
        r'(?i:sensor_temp[a-zA-Z0-9_]*)'
        t.value = t.value.lower()
        return t

    def t_ID_SENS_LUZ(self, t):
        r'(?i:sensor_luz[a-zA-Z0-9_]*)'
        t.value = t.value.lower()
        return t

    def t_ID_SENS_HUMEDAD(self, t):
        r'(?i:sensor_humedad[a-zA-Z0-9_]*)'
        t.value = t.value.lower()
        return t

    def t_ID_SENS_BOOL(self, t):
        r'(?i:sensor_(movimiento|humo)[a-zA-Z0-9_]*)'
        t.value = t.value.lower()
        return t

    # Identificadores
    def t_ID_FOCO(self, t):
        r'(?i:foco_[a-zA-Z0-9_]+)'
        t.value = t.value.lower()
        return t

    def t_ID_AIRE(self, t):
        r'(?i:aire_[a-zA-Z0-9_]+)'
        t.value = t.value.lower()
        return t

    def t_ID_PERSIANA(self, t):
        r'(?i:persiana_[a-zA-Z0-9_]+)'
        t.value = t.value.lower()
        return t

    def t_ID_CERRADURA(self, t):
        r'(?i:cerradura_[a-zA-Z0-9_]+)'
        t.value = t.value.lower()
        return t

    def t_ID_RELOJ(self, t):
        r'(?i:reloj_[a-zA-Z0-9_]+)'
        t.value = t.value.lower()
        return t

    def t_ID_ALTAVOZ(self, t):
        r'(?i:altavoz_[a-zA-Z0-9_]+)'
        t.value = t.value.lower()
        return t

    def t_ID_ALARMA(self, t):
        r'(?i:alarma_[a-zA-Z0-9_]+)'
        t.value = t.value.lower()
        return t

    #Controlador de identificador general
    def t_IDENTIFICADOR(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        palabra = t.value.lower()

        # 1. ¿Es palabra reservada?
        if palabra in self.reserved:
            t.type = self.reserved[palabra]
            return t

        # 2. ¿Es un atributo conocido del dominio?
        if palabra in self.atributos:
            t.type = self.atributos[palabra]
            return t

        # Mensaje en caso de que encuentre algo fuera de lugar
        print(f"Error léxico línea {t.lexer.lineno}: identificador "
              f"desconocido '{t.value}' — no es palabra reservada, "
              f"atributo, sensor ni actuador válido")
        return None

   
    # Manejo de errores léxicos

    def t_error(self, t):
        last_cr = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
        line = t.lexer.lineno
        col = t.lexpos if last_cr < 0 else t.lexpos - last_cr - 1
        print(f"Caracter ilegal '{t.value[0]}' en línea {line}, columna {col}")
        t.lexer.skip(1)


    # Construcción del lexer

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)


    # Método de prueba — imprime cada token reconocido
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(f'Se encontro token del tipo {tok.type:<20} con valor {tok.value}')