# analisis_semantico.py

class AnalizadorSemantico:
    def __init__(self):
        self.variables = {}     # variables visibles (reinicia al cerrar función)
        self.funciones = {}     # nombre -> aridad
        self.errores = []

        # seguimiento de función actual y ámbito
        self._funcion_actual = None
        self._en_header = False
        self._leyendo_nombre = False
        self._params_tmp = []
        self._en_funcion_body = False
        self._brace_depth = 0

    def analizar(self, tokens, calls):
        """
        tokens: [(tok, tipo)] ordenados
        calls:  [(nombre, argc)] recolectados por el parser
        """
        ultimo_tipo = None
        i = 0
        n = len(tokens)

        while i < n:
            tok, tipo = tokens[i]

            # inicio cabecera función
            if tok == "funcion":
                self._en_header = True
                self._leyendo_nombre = True
                self._params_tmp = []
                i += 1
                continue

            # nombre de función
            if self._en_header and self._leyendo_nombre and tipo == "Identificador":
                self._funcion_actual = tok
                self._leyendo_nombre = False
                i += 1
                continue

            # parámetros de función (entre paréntesis)
            if self._en_header and tok == "(":
                i += 1
                while i < n and tokens[i][0] != ")":
                    tpar, tipopar = tokens[i]
                    if tipopar == "Identificador":
                        self._params_tmp.append(tpar)
                        self.variables[tpar] = "parametro"
                    i += 1
                # cerrar ')'
                self._en_header = False
                # siguiente debería ser '{' -> al entrar al body registramos la función
                i += 1
                continue

            # entrar al cuerpo de función
            if self._funcion_actual and tokens[i-1][0] == ")" and tok == "{":
                self._en_funcion_body = True
                self._brace_depth = 1
                # registrar función y su aridad
                if len(self._params_tmp) < 2:
                    self.errores.append(f"Función '{self._funcion_actual}' debe tener mínimo 2 parámetros")
                self.funciones[self._funcion_actual] = len(self._params_tmp)
                i += 1
                continue

            # control de llaves dentro de función
            if self._en_funcion_body:
                if tok == "{":
                    self._brace_depth += 1
                elif tok == "}":
                    self._brace_depth -= 1
                    if self._brace_depth == 0:
                        # salir de función: limpiar variables locales/params
                        self._en_funcion_body = False
                        self._funcion_actual = None
                        self.variables = {}
                # seguimos procesando normalmente

            # declaración de variable
            if tipo == "Palabra Reservada" and tok in ["entero", "decimal", "booleano", "cadena"]:
                ultimo_tipo = tok
                i += 1
                continue

            # id tras tipo -> registrar variable
            if ultimo_tipo and tipo == "Identificador":
                self.variables[tok] = ultimo_tipo
                ultimo_tipo = None
                i += 1
                continue

            # usar identificador como variable (si no es función conocida)
            if tipo == "Identificador" and tok not in self.variables and tok not in self.funciones:
                self.errores.append(f"Variable '{tok}' usada sin declarar")
                i += 1
                continue

            # retornar válido solo dentro de función
            if tok == "retornar":
                if not self._en_funcion_body:
                    self.errores.append("Uso de 'retornar' fuera de una función")
                i += 1
                continue

            i += 1

        # validar llamadas recolectadas por el parser
        for nombre, argc in calls:
            if nombre not in self.funciones:
                self.errores.append(f"Función '{nombre}' no declarada")
            else:
                aridad = self.funciones[nombre]
                if argc != aridad:
                    self.errores.append(
                        f"Función '{nombre}' esperaba {aridad} argumento(s) y recibió {argc}"
                    )

        return self.errores
