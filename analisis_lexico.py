import re

# Definición de tokens lo que reconoce el lexer
palabras_reservadas = {
    "entero", "decimal", "booleano", "cadena",
    "si", "sino", "mientras", "hacer", "verdadero", "falso"
}
operadores = {"+", "-", "*", "/", "%", "=", "==", "<", ">", ">=", "<="}
signos = {"{", "}", "(", ")", ";", '"'}

# Clasificador de tokens
def clasificar_token(token):
    if token in palabras_reservadas:
        return "Palabra Reservada"
    elif token in operadores:
        return "Operador"
    elif token in signos:
        return "Signo"
    elif re.fullmatch(r"\d+", token):
        return "Número"
    elif re.fullmatch(r"\"[^\"]*\"", token):
        return "Cadena"
    elif re.fullmatch(r"[a-zA-Z_]\w*", token):
        return "Identificador"
    else:
        return "Error Léxico"

# Analizador léxico
def analizar(texto):
    resultados = {}
    errores = []
    lineas = texto.split("\n")

    for num_linea, linea in enumerate(lineas, start=1):
        for token in re.findall(
    r"[a-zA-Z_]\w*"
            r"|\d+"
            r"|=="
            r"|>="
            r"|<="
            r"|[+\-*/%={}();<>]"
            r"|\"[^\"]*\""
            r"|\S", linea
        ):
            tipo = clasificar_token(token)
            resultados[(token, tipo)] = resultados.get((token, tipo), 0) + 1
            if tipo == "Error Léxico":
                errores.append(f"Error en línea {num_linea}: token no válido -> {token}")

    return resultados, errores
