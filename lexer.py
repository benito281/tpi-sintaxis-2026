from sly import Lexer


class SmartHomeLexer(Lexer):

    # -------------------------------------------------------------------------
    # Lista completa de tokens
    # -------------------------------------------------------------------------
    tokens = {
        # Palabras reservadas de control
        WHEN, DO, END, EVERY, IF, THEN, ELSE,
        # Operadores lógicos
        AND, OR, NOT,
        # Literales booleanos y de estado
        ON, OFF, TRUE, FALSE,
        # Valores discretos del aire acondicionado
        FRIO, CALOR, VENT,
        # Identificadores
        ID_SENSOR, ID_ACTUADOR, ATRIBUTO,
        # Literales con unidad (tokens compuestos)
        VAL_TEMPERATURA, VAL_PORCENTAJE, VAL_TIEMPO,
        VAL_LUX, VAL_HORA, VAL_FECHA, VAL_EMAIL, VAL_TEXTO,
        # Operadores de comparación
        OP_EQ, OP_NEQ, OP_GTE, OP_LTE, OP_GT, OP_LT,
        # Operador de asignación
        OP_ASIG,
    }

    # Delimitadores simples (un solo carácter, no generan token nombrado)
    literals = { '.', '(', ')' }

    # -------------------------------------------------------------------------
    # Ignorados: espacios, tabs, saltos de línea
    # -------------------------------------------------------------------------
    ignore = ' \t\r\n'

    # -------------------------------------------------------------------------
    # Comentarios — descartados, no generan tokens
    # -------------------------------------------------------------------------

    # Comentario de bloque: /** ... */ o /* ... */
    @_(r'/\*\*[\s\S]*?\*/', r'/\*[\s\S]*?\*/')
    def COMENTARIO_BLOQUE(self, t):
        self.lineno += t.value.count('\n')
        # no retorna nada → el token es descartado

    # Comentario de línea: // ... hasta fin de línea
    @_(r'//[^\n]*')
    def COMENTARIO_LINEA_DOBLE(self, t):
        pass  # descartado

    # Comentario de línea: @ ... hasta fin de línea
    @_(r'@[^\n]*')
    def COMENTARIO_LINEA_ARROBA(self, t):
        pass  # descartado

    # -------------------------------------------------------------------------
    # Operadores de comparación (van ANTES que los de un carácter)
    # -------------------------------------------------------------------------
    OP_EQ   = r'=='
    OP_NEQ  = r'!='
    OP_GTE  = r'>='
    OP_LTE  = r'<='
    OP_GT   = r'>'
    OP_LT   = r'<'
    OP_ASIG = r'='

    # -------------------------------------------------------------------------
    # Literales con unidad
    # Deben ir ANTES que los identificadores para que el lexer no consuma
    # solo el número dejando la unidad suelta.
    # -------------------------------------------------------------------------

    # VAL_TEMPERATURA  Ej: 26°C  -5°C
    @_(r'-?\d+(\.\d+)?°[Cc]')
    def VAL_TEMPERATURA(self, t):
        return t

    # VAL_PORCENTAJE  Ej: 80%  100%
    @_(r'\d{1,3}%')
    def VAL_PORCENTAJE(self, t):
        return t

    # VAL_LUX  Ej: 250lux  (va antes que VAL_TIEMPO para no confundir con 'l')
    @_(r'\d+lux')
    def VAL_LUX(self, t):
        return t

    # VAL_TIEMPO  Ej: 30m  10s  1h
    @_(r'\d+[smh]')
    def VAL_TIEMPO(self, t):
        return t

    # VAL_HORA  Ej: 22:00  06:30  formato HH:MM 24 hs
    @_(r'([01]\d|2[0-3]):[0-5]\d')
    def VAL_HORA(self, t):
        return t

    # VAL_FECHA  Ej: 21/04/2026  formato DD/MM/AAAA
    # Año: 1900-2099 | Mes: 01-12 | Día: 01-31
    @_(r'(0?[1-9]|[12]\d|3[01])/(0?[1-9]|1[0-2])/(19|20)\d{2}')
    def VAL_FECHA(self, t):
        return t

    # VAL_EMAIL  Ej: felipe@smart-home.com.ar
    # Va ANTES que los identificadores
    @_(r'[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9_.+\-]+\.[a-zA-Z]{2,4}')
    def VAL_EMAIL(self, t):
        return t

    # VAL_TEXTO  Ej: "Son las 22hs"  — cadena entre comillas dobles
    @_(r'"[^"]*"')
    def VAL_TEXTO(self, t):
        return t

    # -------------------------------------------------------------------------
    # Identificadores y palabras reservadas
    # sly resuelve las palabras reservadas dentro de la función del
    # identificador genérico reasignando t.type.
    # -------------------------------------------------------------------------

    # Tabla de palabras reservadas (minúsculas — el lenguaje es case-insensitive)
    PALABRAS_RESERVADAS = {
        'when', 'do', 'end', 'every',
        'if', 'then', 'else',
        'and', 'or', 'not',
        'on', 'off', 'true', 'false',
        'frio', 'calor', 'vent',
    }

    # Prefijos de sensores
    PREFIJOS_SENSOR = ('sensor_',)

    # Prefijos de actuadores
    PREFIJOS_ACTUADOR = (
        'foco_', 'aire_', 'persiana_',
        'cerradura_', 'reloj_', 'altavoz_', 'alarma_',
    )

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def IDENTIFICADOR(self, t):
        valor = t.value.lower()  # normalizar para case-insensitive

        # ¿Es palabra reservada?
        if valor in self.PALABRAS_RESERVADAS:
            t.type  = valor.upper()   # WHEN, IF, AND, ON, FRIO, etc.
            t.value = valor
            return t

        # ¿Es un id de sensor?
        for prefijo in self.PREFIJOS_SENSOR:
            if valor.startswith(prefijo):
                t.type  = 'ID_SENSOR'
                t.value = valor
                return t

        # ¿Es un id de actuador?
        for prefijo in self.PREFIJOS_ACTUADOR:
            if valor.startswith(prefijo):
                t.type  = 'ID_ACTUADOR'
                t.value = valor
                return t

        # Si ningún caso anterior aplica: es un atributo (viene después del punto)
        t.type  = 'ATRIBUTO'
        t.value = valor
        return t

    # -------------------------------------------------------------------------
    # Error léxico
    # -------------------------------------------------------------------------
    def error(self, t):
        print(f"  [ERROR LÉXICO] Línea {self.lineno}: "
              f"carácter no reconocido '{t.value[0]}'")
        self.index += 1


# =============================================================================
#  Función auxiliar para mostrar los tokens de forma prolija
# =============================================================================

def analizar(codigo: str):
    lexer  = SmartHomeLexer()
    tokens = list(lexer.tokenize(codigo))

    ancho_tipo  = max(len(t.type)  for t in tokens) if tokens else 10
    ancho_valor = max(len(str(t.value)) for t in tokens) if tokens else 10

    print(f"\n{'LÍNEA':>5}  {'TIPO':<{ancho_tipo}}  {'VALOR'}")
    print('-' * (8 + ancho_tipo + ancho_valor))

    for t in tokens:
        print(f"  {t.lineno:>3}  {t.type:<{ancho_tipo}}  {t.value}")

    print(f"\nTotal: {len(tokens)} token(s)\n")


# =============================================================================
#  Pruebas con el archivo de ejemplo de la consigna
# =============================================================================

if __name__ == '__main__':

    pruebas = [

        ("Comentarios (deben ignorarse)", """
// El sensor de luz activa el foco
/* comentario de
   varias líneas */
/** encabezado */
@ otro comentario de línea
"""),

        ("Bloque WHEN simple", """
WHEN sensor_luz < 250lux DO
    foco_entrada.estado = ON
    foco_entrada.brillo = 80%
    foco_patio.color = blue
END
"""),

        ("Bloque WHEN con IF anidado", """
WHEN sensor_movimiento == TRUE DO
    IF sensor_temp_int > 26°C THEN
        aire_acondicionado.estado = ON
        aire_acondicionado.modo = frio
        aire_acondicionado.temp_objetivo = 22°C
    ELSE
        aire_acondicionado.estado = OFF
    END
END
"""),

        ("Bloque EVERY con condicion compuesta", """
EVERY 30m DO
    IF reloj_sala.hora > 22:00 AND alarma_casa.estado == OFF THEN
        persiana_sala.posicion = 0%
        cerradura_principal.estado = ON
        altavoz_comedor.volumen = 0%
        altavoz_comedor.mensaje = "Son las 22hs, hora de dormir"
        altavoz_comedor.email_notif = felipe@smart-home.com.ar
    END
END
"""),

        ("IF con AND — humo + estado actuador", """
IF sensor_humo == TRUE AND aire_acondicionado.estado == OFF THEN
    aire_acondicionado.estado = ON
    aire_acondicionado.modo = frio
    cerradura_principal.estado = OFF
    persiana_comedor.posicion = 100%
    altavoz_comedor.mensaje = "PELIGRO. HUMO DETECTADO"
    altavoz_comedor.email_notif = bomberos@smart-home.com.ar
END
"""),

        ("VAL_FECHA y VAL_HORA sueltos", """
reloj_sala.fecha = 21/04/2026
reloj_sala.hora  = 06:00
"""),

        ("Error léxico — carácter no reconocido", """
sensor_luz < 250lux DO
    foco_entrada.estado = ON $$$
END
"""),
    ]

    for titulo, codigo in pruebas:
        print('=' * 60)
        print(f'  PRUEBA: {titulo}')
        print('=' * 60)
        analizar(codigo)