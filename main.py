import sys
import subprocess
import os
from PyQt6.QtWidgets import QApplication
from chat_app import MinimalistChatApp

# Get the home directory dynamically
home_dir = os.path.expanduser("~")
ollama_executable = os.path.join(home_dir, "AppData", "Local", "Programs", "Ollama", "ollama app.exe")

# Use subprocess.Popen to run the executable without blocking
subprocess.Popen([ollama_executable], shell=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MinimalistChatApp()
    ex.show()
    sys.exit(app.exec())
