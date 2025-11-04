# errores_formatter.py

def formatear_errores(lexicos, sintacticos, semanticos):
    out = []
    vistos = set()

    # léxicos
    for e in lexicos:
        if "token no válido" in e:
            tok = e.split("->")[-1].strip()
            msg = f"[LEX] Error: token inválido '{tok}'"
        else:
            msg = f"[LEX] {e}"
        if msg not in vistos:
            out.append(msg); vistos.add(msg)

    # sintácticos
    for e in sintacticos:
        msg = f"[SINTAX] {e}"
        if msg not in vistos:
            out.append(msg); vistos.add(msg)

    # semánticos
    for e in semanticos:
        if "Variable '" in e and "usada sin declarar" in e:
            var = e.split("'")[1]
            msg = f"[SEM] Variable '{var}' no declarada"
        else:
            msg = f"[SEM] {e}"
        if msg not in vistos:
            out.append(msg); vistos.add(msg)

    return out
