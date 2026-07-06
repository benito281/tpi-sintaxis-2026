import ply.yacc as yacc
from lexer import LexerTokens
import html as htmlutils

class SmartHomeParser:

    def __init__(self):
        self._lexer_obj = LexerTokens()
        self._lexer_obj.build()
        self.tokens = LexerTokens.tokens
        self.errores = []
        self.parser = yacc.yacc(module=self, debug=False, write_tables=False)

    # Programa home(sigma)
    def p_programa_home(self, p):
        '''programa_home : list_instrucciones'''
        html_base = f"""<!DOCTYPE html>
            <html lang='es'>
            <head>
            <meta charset='UTF-8'>
            <title>Dashboard Smart-Home</title>
            </head>
            <body style='font-family:Arial; padding:20px;'>
            <h1 style='text-align:center;'>🏠 SMART-HOME</h1>
            {p[1]}
            </body>
            </html>"""
        p[0] = html_base

    # Lista de instrucciones
    def p_list_instrucciones_multiple(self, p):
        '''list_instrucciones : list_instrucciones instruccion'''
        p[0] = p[1] + "\n" + p[2]

    def p_list_instrucciones_una(self, p):
        '''list_instrucciones : instruccion'''
        p[0] = p[1]

    def p_instruccion(self, p):
        '''instruccion : asignacion
                       | bloque_cuando
                       | bloque_cada
                       | condicional'''
        p[0] = p[1]

    # Bloques de control
    def p_bloque_cuando(self, p):
        '''bloque_cuando : WHEN condicion DO list_instrucciones END'''
        p[0] = p[2] + "\n" + p[4]

    def p_bloque_cada(self, p):
        '''bloque_cada : EVERY VAL_TIEMPO DO list_instrucciones END'''
        p[0] = p[4]

    def p_condicional_con_else(self, p):
        '''condicional : IF condicion THEN list_instrucciones ELSE list_instrucciones END'''
        p[0] = p[2] + "\n" + p[4] + "\n" + p[6]

    def p_condicional_sin_else(self, p):
        '''condicional : IF condicion THEN list_instrucciones END'''
        p[0] = p[2] + "\n" + p[4]

    # Logica
    def p_condicion_or(self, p):
        '''condicion : condicion OR ter_logico'''
        p[0] = p[1] + "\n" + p[3]

    def p_condicion_simple(self, p):
        '''condicion : ter_logico'''
        p[0] = p[1]

    def p_ter_logico_and(self, p):
        '''ter_logico : ter_logico AND fac_logico'''
        p[0] = p[1] + "\n" + p[3]

    def p_ter_logico_simple(self, p):
        '''ter_logico : fac_logico'''
        p[0] = p[1]

    def p_fac_logico_not(self, p):
        '''fac_logico : NOT fac_logico'''
        p[0] = p[2]

    def p_fac_logico_parentesis(self, p):
        '''fac_logico : LPAREN condicion RPAREN'''
        p[0] = p[2]

    def p_fac_logico_comparacion(self, p):
        '''fac_logico : comparacion'''
        p[0] = p[1]

    #Asignaciones
    def p_asignacion(self, p):
        '''asignacion : asig_estado
                      | asig_porcent
                      | asig_temp
                      | asig_color
                      | asig_modo
                      | asig_texto
                      | asig_email'''
        p[0] = p[1]

    def construir_div_actuador(self, id_actuador, atributo, valor, es_email=False):
        html = f"""
  <div style='background: #ffffff; border: 1px solid #d1d5db; padding: 20px; margin-bottom: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); font-family: sans-serif;'>
    <h3 style='margin: 0 0 10px 0; color: #374151; font-size: 1.2em;'>
        Dispositivo: <span style='color: #2563eb;'>{id_actuador}</span>
    </h3>
    <ul style='list-style: none; padding-left: 0; margin: 0;'>"""
        
        if es_email:
            nombre = str(valor).split('@')[0]
            html += f"\n      <li style='padding: 5px 0; color: #4b5563;'>{atributo}: <a href='mailto:{valor}' style='color: #3b82f6; text-decoration: none;'>Contactar a {nombre}</a></li>"
        else:
            html += f"\n      <li style='padding: 5px 0; color: #4b5563;'>{atributo}: <b style='color: #111827;'>{valor}</b></li>"
        
        html += "\n    </ul>\n  </div>"
        return html

    def construir_div_sensor(self, sensor, operador, valor):
        return f"""
  <div style='background: #f0fdf4; border: 1px solid #22c55e; padding: 20px; margin-bottom: 20px; border-radius: 10px; font-family: sans-serif;'>
    <p style='margin: 0; color: #065f46; font-size: 1.1em;'>
        Sensor: <span style='font-weight: bold; color: #064e3b;'>{sensor}</span> evaluado con: 
        <span style='background: #dcfce7; padding: 2px 6px; border-radius: 4px;'>{htmlutils.escape(str(operador))} {htmlutils.escape(str(valor))}</span>
    </p>
  </div>"""

    def p_asig_estado(self, p):
        '''asig_estado : ID_FOCO      DOT ATTR_ESTADO   ASSIGN valor_estado
                       | ID_AIRE      DOT ATTR_ESTADO   ASSIGN valor_estado
                       | ID_CERRADURA DOT ATTR_ESTADO   ASSIGN valor_estado
                       | ID_ALARMA    DOT ATTR_ESTADO   ASSIGN valor_estado
                       | ID_ALARMA    DOT ATTR_ACTIVADA ASSIGN valor_estado
                       | ID_ALTAVOZ   DOT ATTR_MUTE     ASSIGN valor_estado'''
        p[0] = self.construir_div_actuador(p[1], p[3], p[5])

    def p_asig_porcent_brillo(self, p):
        '''asig_porcent : ID_FOCO DOT ATTR_BRILLO ASSIGN VAL_PORCENTAJE'''
        p[0] = self.construir_div_actuador(p[1], p[3], f"{p[5]}")

    def p_asig_porcent_posicion(self, p):
        '''asig_porcent : ID_PERSIANA DOT ATTR_POSICION ASSIGN VAL_PORCENTAJE'''
        p[0] = self.construir_div_actuador(p[1], p[3], f"{p[5]}")

    def p_asig_porcent_volumen(self, p):
        '''asig_porcent : ID_ALTAVOZ DOT ATTR_VOLUMEN ASSIGN VAL_PORCENTAJE'''
        p[0] = self.construir_div_actuador(p[1], p[3], f"{p[5]}")

    def p_asig_temp(self, p):
        '''asig_temp : ID_AIRE DOT ATTR_TEMP_OBJ ASSIGN VAL_TEMPERATURA'''
        p[0] = self.construir_div_actuador(p[1], p[3], f"{p[5]}")

    def p_asig_color(self, p):
        '''asig_color : ID_FOCO DOT ATTR_COLOR ASSIGN valor_color'''
        p[0] = self.construir_div_actuador(p[1], p[3], p[5])

    def p_asig_modo(self, p):
        '''asig_modo : ID_AIRE DOT ATTR_MODO ASSIGN valor_modo'''
        p[0] = self.construir_div_actuador(p[1], p[3], p[5])

    def p_asig_texto(self, p):
        '''asig_texto : ID_ALTAVOZ DOT ATTR_MENSAJE ASSIGN VAL_TEXTO'''
        p[0] = self.construir_div_actuador(p[1], p[3], htmlutils.escape(str(p[5])))

    def p_asig_email(self, p):
        '''asig_email : ID_ALTAVOZ DOT ATTR_EMAIL_NOTIF ASSIGN VAL_EMAIL'''
        p[0] = self.construir_div_actuador(p[1], p[3], p[5], es_email=True)

    # Sensores y comparaciones
    def p_comparacion(self, p):
        '''comparacion : comp_temp
                       | comp_lux
                       | comp_porcent
                       | comp_bool
                       | comp_tiempo
                       | comp_fecha'''
        p[0] = p[1]

   

    def p_comp_temp(self, p):
        '''comp_temp : exp_temp op_comp VAL_TEMPERATURA'''
        p[0] = self.construir_div_sensor(p[1], p[2], f"{p[3]}")

    def p_exp_temp_sensor(self, p):
        '''exp_temp : ID_SENS_TEMP'''
        p[0] = p[1]

    def p_exp_temp_act(self, p):
        '''exp_temp : ID_AIRE DOT ATTR_TEMP_ACT'''
        p[0] = f"{p[1]}.{p[3]}"

    def p_exp_temp_obj(self, p):
        '''exp_temp : ID_AIRE DOT ATTR_TEMP_OBJ'''
        p[0] = f"{p[1]}.{p[3]}"

    def p_comp_lux(self, p):
        '''comp_lux : ID_SENS_LUZ op_comp VAL_LUX'''
        p[0] = self.construir_div_sensor(p[1], p[2], f"{p[3]}")

    def p_comp_porcent(self, p):
        '''comp_porcent : exp_porcent op_comp VAL_PORCENTAJE'''
        p[0] = self.construir_div_sensor(p[1], p[2], f"{p[3]}")

    def p_exp_porcent_brillo(self, p):
        '''exp_porcent : ID_FOCO DOT ATTR_BRILLO'''
        p[0] = f"{p[1]}.{p[3]}"

    def p_exp_porcent_posicion(self, p):
        '''exp_porcent : ID_PERSIANA DOT ATTR_POSICION'''
        p[0] = f"{p[1]}.{p[3]}"

    def p_exp_porcent_volumen(self, p):
        '''exp_porcent : ID_ALTAVOZ DOT ATTR_VOLUMEN'''
        p[0] = f"{p[1]}.{p[3]}"

    def p_exp_porcent_humedad(self, p):
        '''exp_porcent : ID_SENS_HUMEDAD'''
        p[0] = p[1]

    def p_comp_bool_sensor(self, p):
        '''comp_bool : ID_SENS_BOOL EQ valor_sensor_bool
                     | ID_SENS_BOOL NEQ valor_sensor_bool'''
        p[0] = self.construir_div_sensor(p[1], p[2], p[3])

    def p_comp_bool_estado(self, p):
        '''comp_bool : ID_FOCO      DOT ATTR_ESTADO   EQ  valor_estado
                     | ID_FOCO      DOT ATTR_ESTADO   NEQ valor_estado
                     | ID_AIRE      DOT ATTR_ESTADO   EQ  valor_estado
                     | ID_AIRE      DOT ATTR_ESTADO   NEQ valor_estado
                     | ID_CERRADURA DOT ATTR_ESTADO   EQ  valor_estado
                     | ID_CERRADURA DOT ATTR_ESTADO   NEQ valor_estado
                     | ID_ALARMA    DOT ATTR_ESTADO   EQ  valor_estado
                     | ID_ALARMA    DOT ATTR_ESTADO   NEQ valor_estado
                     | ID_ALARMA    DOT ATTR_ACTIVADA EQ  valor_estado
                     | ID_ALARMA    DOT ATTR_ACTIVADA NEQ valor_estado
                     | ID_ALTAVOZ   DOT ATTR_MUTE     EQ  valor_estado
                     | ID_ALTAVOZ   DOT ATTR_MUTE     NEQ valor_estado'''
        p[0] = self.construir_div_sensor(f"{p[1]}.{p[3]}", p[4], p[5])

    def p_comp_tiempo(self, p):
        '''comp_tiempo : ID_RELOJ DOT ATTR_HORA op_comp VAL_HORA'''
        p[0] = self.construir_div_sensor(f"{p[1]}.{p[3]}", p[4], p[5])

    def p_comp_fecha(self, p):
        '''comp_fecha : ID_RELOJ DOT ATTR_FECHA op_comp VAL_FECHA'''
        p[0] = self.construir_div_sensor(f"{p[1]}.{p[3]}", p[4], p[5])

    #Operadores y valores
    def p_op_comp(self, p):
        '''op_comp : EQ
                   | NEQ
                   | GT
                   | LT
                   | GTE
                   | LTE'''
        p[0] = p[1]

    def p_valor_estado(self, p):
        '''valor_estado : ON
                        | OFF'''
        p[0] = p[1]

    def p_valor_sensor_bool(self, p):
        '''valor_sensor_bool : TRUE
                             | FALSE'''
        p[0] = p[1]

    def p_valor_color(self, p):
        '''valor_color : BLANCO
                       | ROJO
                       | AZUL'''
        p[0] = p[1]

    def p_valor_modo(self, p):
        '''valor_modo : FRIO
                      | CALOR
                      | VENT'''
        p[0] = p[1]

    # Manejo de errores
    def p_error(self, p):
        if p:
            self.errores.append((p.lineno, p.type, p.value))
        else:
            self.errores.append((None, None, 'EOF'))

    def analizar(self, codigo):
        self.errores = []
        self._lexer_obj.lexer.lineno = 1
        resultado = self.parser.parse(
            codigo,
            lexer=self._lexer_obj.lexer
        )
        return resultado