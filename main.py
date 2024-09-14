
import sys
from PyQt6.QtWidgets import QApplication
from chat_app import MinimalistChatApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MinimalistChatApp()
    ex.show()
    sys.exit(app.exec())
