import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    w = MainWindow()
    w.setMinimumWidth(520)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
