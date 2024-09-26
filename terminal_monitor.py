import sys
import psutil
import time
import platform
import GPUtil
import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, 
                             QTabWidget, QTextEdit, QLineEdit, QHBoxLayout, QGroupBox,
                             QProgressBar)
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QProcess

class DiskUsageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.bars = {}

    def update_usage(self):
        # Fetch the list of partitions
        partitions = psutil.disk_partitions()

        # Create or update progress bars for each partition
        for partition in partitions:
            try:
                # Skip drives that are not ready (e.g., CD drives or unmounted drives)
                if 'cdrom' in partition.opts or not partition.fstype:
                    continue

                # Attempt to get disk usage for the partition
                usage = psutil.disk_usage(partition.mountpoint)
                
                # Check if this partition's bar already exists, otherwise create it
                if partition.device not in self.bars:
                    bar = QProgressBar(self)
                    bar.setRange(0, 100)
                    self.layout.addWidget(bar)
                    self.bars[partition.device] = bar

                # Update the progress bar's value and label
                bar = self.bars[partition.device]
                bar.setValue(int(usage.percent))  # Cast to int for QProgressBar
                
                # Format the label with drive, used space, total space, and percentage
                used_gb = usage.used / (1024 ** 3)
                total_gb = usage.total / (1024 ** 3)
                bar.setFormat(f"{partition.device}: {used_gb:.2f} GB / {total_gb:.2f} GB ({int(usage.percent)}%)")
                
            except PermissionError:
                print(f"Permission denied for {partition.device}. Skipping.")
                continue
            except OSError as e:
                if e.winerror == 21:  # WinError 21: The device is not ready
                    print(f"Drive {partition.device} is not ready. Skipping.")
                else:
                    print(f"Error for {partition.device}: {e}")
                continue

        # Remove bars that are no longer relevant (e.g., if a device was disconnected)
        for device in list(self.bars.keys()):
            if device not in [partition.device for partition in partitions]:
                bar = self.bars.pop(device)
                self.layout.removeWidget(bar)
                bar.deleteLater()




class PCMonitorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        # Left column - Dynamic metrics
        left_group = QGroupBox("System Metrics")
        left_layout = QVBoxLayout(left_group)

        self.cpu_label = QLabel("CPU Usage: ")
        self.memory_label = QLabel("Memory Usage: ")
        self.network_label = QLabel("Network Usage: ")
        self.uptime_label = QLabel("System Uptime: ")
        self.boot_time_label = QLabel("Boot Time: ")  # Initialize boot_time_label

        left_layout.addWidget(self.cpu_label)
        left_layout.addWidget(self.memory_label)
        left_layout.addWidget(self.network_label)
        left_layout.addWidget(self.uptime_label)
        left_layout.addWidget(self.boot_time_label)  # Add boot_time_label to the layout
        
        # Add disk usage widget
        self.disk_usage_widget = DiskUsageWidget()
        left_layout.addWidget(QLabel("Storage Usage:"))
        left_layout.addWidget(self.disk_usage_widget)

        left_layout.addStretch()

        # Right column - Hardware specs
        right_group = QGroupBox("Hardware Specifications")
        right_layout = QVBoxLayout(right_group)

        self.cpu_info = QLabel("CPU: ")
        self.gpu_info = QLabel("GPU: ")
        self.ram_info = QLabel("RAM: ")

        right_layout.addWidget(self.cpu_info)
        right_layout.addWidget(self.gpu_info)
        right_layout.addWidget(self.ram_info)
        right_layout.addStretch()

        layout.addWidget(left_group)
        layout.addWidget(right_group)

        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()

        # Initialize hardware specs
        self.update_hardware_specs()

    def update_hardware_specs(self):
        # CPU Info
        cpu_info = platform.processor()
        self.cpu_info.setText(f"CPU: {cpu_info}")

        # GPU Info
        try:
            gpus = GPUtil.getGPUs()
            gpu_info = gpus[0].name if gpus else "N/A"
        except:
            gpu_info = "Unable to retrieve GPU info"
        self.gpu_info.setText(f"GPU: {gpu_info}")

        # RAM Info
        ram = psutil.virtual_memory()
        ram_total = ram.total / (1024 ** 3)  # Convert to GB
        self.ram_info.setText(f"RAM: {ram_total:.2f} GB")

    def update_stats(self):
        # CPU Usage
        cpu_percent = psutil.cpu_percent()
        self.cpu_label.setText(f"CPU Usage: {cpu_percent:.1f}%")

        # Memory Usage
        memory = psutil.virtual_memory()
        self.memory_label.setText(f"Memory Usage: {memory.percent:.1f}%")

        # Network Usage
        current_net_io = psutil.net_io_counters()
        current_net_time = time.time()

        duration = current_net_time - self.last_net_time
        bytes_sent = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / duration
        bytes_recv = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / duration

        self.network_label.setText(f"Network: ↑ {bytes_sent / 1024:.1f} KB/s, ↓ {bytes_recv / 1024:.1f} KB/s")

        self.last_net_io = current_net_io
        self.last_net_time = current_net_time

        # System Uptime
        uptime = int(time.time() - psutil.boot_time())

        # Convert uptime to days, hours, minutes, seconds
        days, remainder = divmod(uptime, 86400)  # 86400 seconds in a day
        hours, remainder = divmod(remainder, 3600)  # 3600 seconds in an hour
        minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute

        # Update the uptime label
        self.uptime_label.setText(f"System Uptime: {days}d {hours}h {minutes}m {seconds}s")

        # Get the boot time and convert it to local datetime
        boot_time = psutil.boot_time()
        boot_time_dt = datetime.datetime.fromtimestamp(boot_time)  # Convert to local time

        # Format the boot time for display
        boot_time_str = boot_time_dt.strftime("%Y-%m-%d %H:%M:%S")  # Example format: "2024-09-26 15:30:00"

        # Update the boot time label
        self.boot_time_label.setText(f"Boot Time: {boot_time_str}")

        # Update Disk Usage
        self.disk_usage_widget.update_usage()

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

class CombinedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PC Monitor & Terminal")
        self.setGeometry(100, 100, 900, 600)  # Increased window size
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