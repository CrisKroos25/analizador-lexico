# analisis_sintactico.py

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)        # [(tok, tipo)]
        self.pos = 0
        self.errores = []
        self.calls = []                   # registro de llamadas: [(nombre, argc)]
        self.funcion_actual = None        # nombre de la función en la que estamos (o None)

    # utilidades
    def token_actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("EOF", "EOF")

    def avanzar(self):
        self.pos += 1

    def coincidir(self, esperado):
        tok, tipo = self.token_actual()
        if tok == esperado or tipo == esperado:
            self.avanzar()
            return True
        self.errores.append(f"Error sintáctico: se esperaba '{esperado}', se encontró '{tok}'")
        self.avanzar()
        return False

    # entrada
    def analizar(self):
        while self.token_actual()[0] != "EOF":
            self.instruccion()
        return self.errores

    # gramática
    def instruccion(self):
        tok, tipo = self.token_actual()

        if tok == "funcion":
            self.declaracion_funcion()
        elif tok == "si":
            self.if_statement()
        elif tok == "retornar":
            self.return_statement()
        elif tipo == "Palabra Reservada" and tok in ["entero", "decimal", "booleano", "cadena"]:
            self.declaracion()
        elif tipo == "Identificador":
            self.asignacion_o_llamada()
        elif tok == "hacer":
            self.coincidir("hacer")

        else:
            self.errores.append(f"Instrucción no válida en '{tok}'")
            self.avanzar()

    def bloque(self):
        self.coincidir("{")
        while self.token_actual()[0] not in {"}", "EOF"}:
            self.instruccion()
        self.coincidir("}")

    def declaracion_funcion(self):
        self.coincidir("funcion")
        # nombre
        nombre = self.token_actual()[0]
        self.coincidir("Identificador")
        self.funcion_actual = nombre

        # parámetros
        self.coincidir("(")
        count = self.parametros()
        self.coincidir(")")
        if count < 2:
            self.errores.append("Función debe tener mínimo 2 parámetros")

        # cuerpo
        self.bloque()

        # salir de función
        self.funcion_actual = None

    def parametros(self):
        count = 0
        tok, tipo = self.token_actual()
        if tipo == "Identificador":
            count += 1
            self.avanzar()
            while self.token_actual()[0] == ",":
                self.avanzar()
                self.coincidir("Identificador")
                count += 1
        return count

    def argumentos(self):
        argc = 0
        tok, tipo = self.token_actual()
        if tipo in ["Identificador", "Número", "Cadena"] or tok in {"(", "verdadero", "falso"}:
            self.expresion()
            argc += 1
            while self.token_actual()[0] == ",":
                self.avanzar()
                self.expresion()
                argc += 1
        return argc

    def llamada_funcion_stmt(self):
        nombre = self.token_actual()[0]
        self.coincidir("Identificador")
        self.coincidir("(")
        argc = self.argumentos()
        self.coincidir(")")
        self.calls.append((nombre, argc))
        self.coincidir(";")

    def asignacion_o_llamada(self):
        # ¿identificador seguido de "("?
        if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == "(":
            self.llamada_funcion_stmt()
        else:
            self.asignacion()

    def declaracion(self):
        # tipo
        self.avanzar()
        # identificador = expresión ;
        self.coincidir("Identificador")
        self.coincidir("=")
        self.expresion()
        self.coincidir(";")

    def asignacion(self):
        self.coincidir("Identificador")
        self.coincidir("=")
        self.expresion()
        self.coincidir(";")

    def if_statement(self):
        self.coincidir("si")
        self.coincidir("(")
        self.expresion()
        self.coincidir(")")
        self.bloque()
        # opcional sino
        if self.token_actual()[0] == "sino":
            self.avanzar()
            self.bloque()

    def return_statement(self):
        if self.funcion_actual is None:
            self.errores.append("Uso de 'retornar' fuera de función")
        self.coincidir("retornar")
        # retorno opcional con expresión
        if self.token_actual()[0] != ";":
            self.expresion()
        self.coincidir(";")

    # expresiones con relacionales
    def expresion(self):
        self.relacional()

    def relacional(self):
        self.aditiva()
        while self.token_actual()[0] in ["==", "!=", "<", ">", "<=", ">="]:
            self.avanzar()
            self.aditiva()

    def aditiva(self):
        self.termino()
        while self.token_actual()[0] in ["+", "-"]:
            self.avanzar()
            self.termino()

    def termino(self):
        self.factor()
        while self.token_actual()[0] in ["*", "/", "%"]:
            self.avanzar()
            self.factor()

    def factor(self):
        tok, tipo = self.token_actual()

        # booleanos
        if tok in {"verdadero", "falso"}:
            self.avanzar()
            return

        # llamada como factor: f(...)
        if tipo == "Identificador" and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == "(":
            # registrar la llamada también cuando aparece en expresiones
            nombre = self.token_actual()[0]
            self.coincidir("Identificador")
            self.coincidir("(")
            argc = self.argumentos()
            self.coincidir(")")
            self.calls.append((nombre, argc))
            return

        if tipo in ["Número", "Identificador", "Cadena"]:
            self.avanzar()
        elif tok == "(":
            self.coincidir("(")
            self.expresion()
            self.coincidir(")")
        else:
            self.errores.append(f"Factor inválido '{tok}'")
            self.avanzar()
