import sys
import subprocess
from PyQt6.QtWidgets import QApplication
from chat_app import MinimalistChatApp

# Use subprocess.Popen to run the executable without blocking
subprocess.Popen([r"C:\Users\keaton\AppData\Local\Programs\Ollama\ollama app.exe"], shell=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MinimalistChatApp()
    ex.show()
    sys.exit(app.exec())
