import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # Cargar estilo
    with open("styles/stylesdark.qss", "r") as f:
        qss = f.read()
        app.setStyleSheet(qss)

    w = MainWindow()
    w.setMinimumWidth(520)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
