from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget)
from home import Home

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Compilador")
        self.setGeometry(200, 100, 750, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # --- Layout principal ---

        self.main_layout = QHBoxLayout(self)
        central_widget.setLayout(self.main_layout)

        self.main_layout.addWidget(Home())



