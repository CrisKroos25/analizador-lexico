import os
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QFileDialog, QLabel, QMessageBox
)
from analisis_lexico import analizar

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/home.ui", self)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.seleccionar_archivo.clicked.connect(self.cargar_archivo)

        # QLabel para ruta
        self.route = QLabel("")
        layout.addWidget(self.route)

        self.ruta_archivo = None

    def cargar_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "Articulos",
            "Archivos de texto (*.txt)"
        )

        if ruta:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                self.plainTextEdit_1.setPlainText(contenido)
                self.analizar(contenido)
                self.route.setText(os.path.basename(ruta))

    def analizar(self, contenido):
        resultados, errores = analizar(contenido)

        self.plainTextEdit_2.clear()
        self.plainTextEdit_2.appendPlainText("TOKEN - TIPO - CANTIDAD")

        # Tokens
        for (token, tipo), cantidad in resultados.items():
            linea = f"{token:<10} {tipo:<20} {cantidad}"
            self.plainTextEdit_2.appendPlainText(linea)

        # Errores
        if errores:
            self.plainTextEdit_2.appendPlainText("\n--- ERRORES LÉXICOS ---")
            for err in errores:
                self.plainTextEdit_2.appendPlainText(err)
