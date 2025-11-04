# home.py
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QFileDialog, QLabel, QMessageBox
from PyQt6 import QtWidgets
from analisis_lexico import analizar
from analisis_sintactico import Parser
from analisis_semantico import AnalizadorSemantico
from errores_formatter import formatear_errores

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/home.ui", self)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.seleccionar_archivo.clicked.connect(self.cargar_resultados)

        self.route = QLabel("")
        layout.addWidget(self.route)

        self.ruta_archivo = None

    def cargar_ruta(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo", "Articulos", "Archivos de texto (*.txt *.lenguaje)"
        )
        if not ruta:
            return None, None
        self.ruta_archivo = ruta
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            return ruta, contenido
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo:\n{e}")
            return None, None

    def cargar_resultados(self):
        ruta, contenido = self.cargar_ruta()
        if not ruta:
            return
        self.plainTextEdit_1.setPlainText(contenido)
        self.analizar(contenido)
        self.route.setText(os.path.basename(ruta))

    def analizar(self, contenido):
        # limpiar UI previo
        self.plainTextEdit_2.clear()
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        # 1) léxico
        tokens, conteo, errores_lex = analizar(contenido)

        # 2) sintáctico
        p = Parser(tokens)
        errores_sint = p.analizar()

        # 3) semántico
        sem = AnalizadorSemantico()
        errores_sem = sem.analizar(tokens, p.calls)

        # 4) formateo y presentación
        errores_finales = formatear_errores(errores_lex, errores_sint, errores_sem)
        if not errores_finales:
            self.plainTextEdit_2.appendPlainText("Sin errores.")
        else:
            for e in errores_finales:
                self.plainTextEdit_2.appendPlainText(e)

        # 5) tabla de tokens
        self.cargar_tabla_tokens(conteo)

    def cargar_tabla_tokens(self, conteo):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Token", "Tipo", "Cantidad"])
        for (token, tipo), cantidad in conteo.items():
            fila = self.tableWidget.rowCount()
            self.tableWidget.insertRow(fila)
            self.tableWidget.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(token)))
            self.tableWidget.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(tipo)))
            self.tableWidget.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(cantidad)))
