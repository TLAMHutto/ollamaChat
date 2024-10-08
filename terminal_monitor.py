import sys
import os
import psutil
import time
import platform
import GPUtil
import datetime
import socket
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, 
                             QTabWidget, QTextEdit, QLineEdit, QHBoxLayout, QGroupBox,
                             QProgressBar, QFileDialog, QListView, QScrollArea, QFrame)
from PyQt6.QtGui import QColor, QPalette, QFont, QTextCursor
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QProcess, QStringListModel

class NetworkWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.updateNetworkStats()

    def initUI(self):
        # Set up the layout
        self.layout = QVBoxLayout()

        # Labels to show the hostname, IP, and network stats
        self.hostname_label = QLabel("Hostname: ")
        self.ip_address_label = QLabel("IP Address: ")
        self.network_stats_label = QLabel("Network Stats: ")

        # Add the labels to the main layout
        self.layout.addWidget(self.hostname_label)
        self.layout.addWidget(self.ip_address_label)
        self.layout.addWidget(self.network_stats_label)

        # Create two scroll areas, one for Open Ports and one for In Use Ports
        self.open_ports_scroll_area = QScrollArea()
        self.open_ports_scroll_area.setWidgetResizable(True)

        self.in_use_ports_scroll_area = QScrollArea()
        self.in_use_ports_scroll_area.setWidgetResizable(True)

        # Create containers for both open and in-use ports
        self.open_ports_container = QFrame()
        self.open_ports_layout = QVBoxLayout()
        self.open_ports_container.setLayout(self.open_ports_layout)

        self.in_use_ports_container = QFrame()
        self.in_use_ports_layout = QVBoxLayout()
        self.in_use_ports_container.setLayout(self.in_use_ports_layout)

        # Set widgets for scroll areas
        self.open_ports_scroll_area.setWidget(self.open_ports_container)
        self.in_use_ports_scroll_area.setWidget(self.in_use_ports_container)

        # Create a layout for the labels (Open Ports and In Use Ports)
        labels_layout = QHBoxLayout()
        open_ports_label = QLabel("Open Ports:")
        in_use_ports_label = QLabel("In Use Ports:")

        labels_layout.addWidget(open_ports_label)
        labels_layout.addWidget(in_use_ports_label)

        # Align the "In Use Ports" label to the right
        in_use_ports_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Use QHBoxLayout to display the two scroll areas side by side
        ports_layout = QHBoxLayout()
        ports_layout.addWidget(self.open_ports_scroll_area)
        ports_layout.addWidget(self.in_use_ports_scroll_area)

        # Add the labels and the scrollable areas into the main layout
        self.layout.addLayout(labels_layout)  # Add the labels for the columns
        self.layout.addLayout(ports_layout)   # Add the scrollable areas

        # Set the layout for the widget
        self.setLayout(self.layout)

        # Set up a timer to periodically update network metrics
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateNetworkStats)
        self.timer.start(5000)  # Update every 5 seconds

    def updateNetworkStats(self):
        # Get and display the hostname
        hostname = socket.gethostname()
        self.hostname_label.setText(f"Hostname: {hostname}")

        # Get and display the IP address
        ip_address = self.get_ip_address()
        self.ip_address_label.setText(f"IP Address: {ip_address}")

        # Get and display network stats
        network_stats = self.get_network_stats()
        self.network_stats_label.setText(f"Network Stats: {network_stats}")

        # Update the open and in-use ports
        self.update_ports()

    def update_ports(self):
        """Update the lists of open and in-use ports."""
        # Clear the current contents of the layouts
        self.clear_layout(self.open_ports_layout)
        self.clear_layout(self.in_use_ports_layout)

        # Get the open and in-use ports
        open_ports, in_use_ports = self.get_ports()

        # Display each open port in the open ports scroll area
        for port in open_ports:
            open_port_label = QLabel(f"Port: {port}")
            self.open_ports_layout.addWidget(open_port_label)

        # Display each in-use port in the in-use ports scroll area
        for port in in_use_ports:
            in_use_port_label = QLabel(f"Port: {port}")
            self.in_use_ports_layout.addWidget(in_use_port_label)

    def clear_layout(self, layout):
        """Helper function to clear the contents of a layout."""
        for i in reversed(range(layout.count())):
            widget_to_remove = layout.itemAt(i).widget()
            layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

    def get_ip_address(self):
        """Get the IP address of the machine."""
        try:
            ip_address = socket.gethostbyname(socket.gethostname())
            return ip_address
        except socket.error as e:
            return f"Error: {str(e)}"

    def get_ports(self):
        """Get lists of open and in-use ports."""
        connections = psutil.net_connections()

        # Open ports (ports in 'LISTEN' state)
        open_ports = [conn.laddr.port for conn in connections if conn.status == 'LISTEN']

        # In-use ports (ports in 'ESTABLISHED' state)
        in_use_ports = [conn.laddr.port for conn in connections if conn.status == 'ESTABLISHED']

        return open_ports, in_use_ports

    def get_network_stats(self):
        """Get some basic network stats."""
        stats = psutil.net_if_stats()
        network_info = []
        for iface, stat in stats.items():
            if stat.isup:
                network_info.append(f"{iface}: {'UP' if stat.isup else 'DOWN'}")
        return ', '.join(network_info)


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
        self.current_path = os.getcwd()  # Initialize current working directory
        self.command_history = []
        self.history_index = -1  # Track history index
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

        # File list view
        self.file_view = QListView(self)
        self.file_view.setFixedHeight(200)  # Set a fixed height for the file view
        layout.addWidget(self.file_view)

        # Set up QProcess
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

        # Initial output
        self.output_text.append("Windows Terminal")
        self.update_file_list()  # Initialize the file list
        self.show_prompt()  # Show initial prompt

    def show_prompt(self):
        self.output_text.append(f"\n{self.current_path}> ")
        self.output_text.moveCursor(QTextCursor.MoveOperation.End)

    def execute_command(self):
        command = self.input_line.text().strip()
        if command:
            self.command_history.append(command)
            self.history_index = len(self.command_history)

            self.output_text.moveCursor(QTextCursor.MoveOperation.End)
            self.output_text.insertPlainText(command)  # Add the command to the current line
            self.output_text.append("")  # Move to the next line

            if command.startswith("cd "):
                path = command[3:].strip()
                self.change_directory(path)
            else:
                self.process.start("cmd.exe", ["/c", command])

            self.input_line.clear()

    def change_directory(self, path):
        try:
            if os.path.isdir(path):
                os.chdir(path)
                self.current_path = os.getcwd()
                self.update_file_list()
            else:
                self.output_text.append(f"'{path}' is not a valid directory.")
        except Exception as e:
            self.output_text.append(f"Error changing directory: {str(e)}")
        self.show_prompt()

    def update_file_list(self):
        try:
            files = os.listdir(self.current_path)
            model = QStringListModel(files)
            self.file_view.setModel(model)
        except Exception as e:
            self.output_text.append(f"Error listing files: {str(e)}")

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output_text.insertPlainText(data)
        self.command_executed.emit(data, "")

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output_text.insertPlainText(data)
        self.command_executed.emit("", data)

    def process_finished(self, exit_code, exit_status):
        self.show_prompt()

    def get_current_path(self):
        return self.current_path

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            if self.history_index > 0:
                self.history_index -= 1
                self.input_line.setText(self.command_history[self.history_index])
        elif event.key() == Qt.Key.Key_Down:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.input_line.setText(self.command_history[self.history_index])
            else:
                self.history_index = len(self.command_history)
                self.input_line.clear()

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
        
        self.terminal = NetworkWidget()
        self.tab_widget.addTab(self.terminal, "Network")

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