from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtCore import Qt, pyqtSignal, QProcess

class TerminalWindow(QMainWindow):
    command_executed = pyqtSignal(str, str)  # Signal for command output (stdout, stderr)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Windows Terminal")
        self.setGeometry(100, 100, 600, 400)
        self.process = QProcess(self)
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Output text area
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.output_text)

        # Input line
        self.input_line = QLineEdit(self)
        self.input_line.setFont(QFont("Consolas", 10))
        self.input_line.returnPressed.connect(self.execute_command)
        layout.addWidget(self.input_line)

        # Set dark theme colors
        self.set_dark_theme()

        # Set up QProcess
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

        # Initial prompt
        self.output_text.append("Windows Terminal\n")
        self.output_text.append(f"{self.get_current_path()}> ")

    def set_dark_theme(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Base, QColor(15, 15, 15))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Button, QColor(60, 60, 60))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
        self.setPalette(palette)

    def execute_command(self):
        command = self.input_line.text().strip()
        self.output_text.append(f"{self.get_current_path()}> {command}\n")
        self.input_line.clear()

        if command.lower() == "exit":
            self.close()
        else:
            self.process.start("cmd.exe", ["/c", command])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output_text.append(data)
        self.command_executed.emit(data, "")

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output_text.append(data)
        self.command_executed.emit("", data)

    def process_finished(self, exit_code, exit_status):
        self.output_text.append(f"\n{self.get_current_path()}> ")

    def get_current_path(self):
        process = QProcess()
        process.start("cmd.exe", ["/c", "cd"])
        process.waitForFinished()
        path = process.readAllStandardOutput().data().decode().strip()
        return path

    def closeEvent(self, event):
        self.process.kill()
        event.accept()