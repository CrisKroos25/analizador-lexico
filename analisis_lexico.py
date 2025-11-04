# analisis_lexico.py
import re

palabras_reservadas = {
    "entero", "decimal", "booleano", "cadena",
    "si", "sino", "mientras", "hacer", "verdadero", "falso",
    "funcion", "retornar"
}
operadores = {"+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", ">=", "<="}
signos = {"{", "}", "(", ")", ";", '"', ","}

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

def analizar(texto):
    tokens_ordenados = []
    conteo = {}
    errores = []
    lineas = texto.split("\n")

    for num_linea, linea in enumerate(lineas, start=1):
        for token in re.findall(
            r"[a-zA-Z_]\w*"
            r"|\d+"
            r"|==|!=|>=|<="
            r"|[+\-*/%={}();<>!,]"
            r"|\"[^\"]*\""
            r"|\S",
            linea
        ):
            tipo = clasificar_token(token)
            tokens_ordenados.append((token, tipo))
            conteo[(token, tipo)] = conteo.get((token, tipo), 0) + 1
            if tipo == "Error Léxico":
                errores.append(f"Error en línea {num_linea}: token no válido -> {token}")

    return tokens_ordenados, conteo, errores
