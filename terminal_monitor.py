import sys
import psutil
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, 
                             QTabWidget, QTextEdit, QLineEdit)
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QProcess

class TerminalWidget(QWidget):
    command_executed = pyqtSignal(str, str)  # Signal for command output (stdout, stderr)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = QProcess(self)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

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

        # Set up QProcess
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

        # Initial prompt
        self.output_text.append("Windows Terminal\n")
        self.output_text.append(f"{self.get_current_path()}> ")

    def execute_command(self):
        command = self.input_line.text().strip()
        self.output_text.append(f"{self.get_current_path()}> {command}\n")
        self.input_line.clear()

        if command.lower() == "exit":
            self.parent().close()
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

class PCMonitorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.cpu_label = QLabel("CPU Usage: ")
        self.memory_label = QLabel("Memory Usage: ")
        self.disk_label = QLabel("Disk Usage: ")
        self.network_label = QLabel("Network Usage: ")
        self.temp_label = QLabel("CPU Temperature: ")

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.disk_label)
        layout.addWidget(self.network_label)
        layout.addWidget(self.temp_label)

        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()

    def update_stats(self):
        # CPU Usage
        cpu_percent = psutil.cpu_percent()
        self.cpu_label.setText(f"CPU Usage: {cpu_percent:.1f}%")

        # Memory Usage
        memory = psutil.virtual_memory()
        self.memory_label.setText(f"Memory Usage: {memory.percent:.1f}%")

        # Disk Usage
        disk = psutil.disk_usage('/')
        self.disk_label.setText(f"Disk Usage: {disk.percent:.1f}%")

        # Network Usage
        current_net_io = psutil.net_io_counters()
        current_net_time = time.time()
        
        duration = current_net_time - self.last_net_time
        bytes_sent = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / duration
        bytes_recv = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / duration

        self.network_label.setText(f"Network: ↑ {bytes_sent/1024:.1f} KB/s, ↓ {bytes_recv/1024:.1f} KB/s")

        self.last_net_io = current_net_io
        self.last_net_time = current_net_time

        # CPU Temperature (if available)
        try:
            temp = psutil.sensors_temperatures()['coretemp'][0].current
            self.temp_label.setText(f"CPU Temperature: {temp:.1f}°C")
        except:
            self.temp_label.setText("CPU Temperature: Not available")

class CombinedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PC Monitor & Terminal")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create and add PC Monitor tab
        self.pc_monitor = PCMonitorWidget()
        self.tab_widget.addTab(self.pc_monitor, "PC Monitor")

        # Create and add Terminal tab
        self.terminal = TerminalWidget()
        self.tab_widget.addTab(self.terminal, "Terminal")

        # Set up timer for updating PC Monitor stats
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.pc_monitor.update_stats)
        self.timer.start(1000)  # Update every 1 second

        # Set dark theme colors
        self.set_dark_theme()

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

    def closeEvent(self, event):
        self.terminal.process.kill()
        event.accept()