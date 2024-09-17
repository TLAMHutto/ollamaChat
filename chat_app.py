from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QPixmap, QIcon
from chat_window import ChatWindow
from ocr import OCR
import threading
import tkinter as tk
class MinimalistChatApp(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.chat_window = None
        self.ocr_window = None  # Add ocr_window reference
        self.initUI()
        self.oldPos = self.pos()

    def initUI(self):
        self.setGeometry(1680, 992, 150, 35)  # Increase width to accommodate new button

        # Create main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        self.square_button = QPushButton(self)
        self.square_button.setFixedSize(35, 35)  # Set fixed size for square button
        
        self.chat_button = QPushButton(self)
        self.chat_button.setFixedSize(35, 35)
        
        self.exit_button = QPushButton(self)
        self.exit_button.setFixedSize(35, 35)

        # Load the icon images
        scan = QPixmap('./zoom-scan.png')
        chat = QPixmap('./message-dots.png')
        exit = QPixmap('./square-letter-x.png')
        
        # Configure square button
        self.square_button.setIcon(QIcon(scan))
        self.square_button.setIconSize(QSize(20, 20))  # Set the size of the icon
        self.square_button.setStyleSheet('background-color: lightgray; border: none;')  # Optional: set background color and remove border
        self.square_button.clicked.connect(self.open_ocr_window)  # Connect button click to open OCR window
        
        # Configure chat button
        self.chat_button.setIcon(QIcon(chat))
        self.chat_button.setIconSize(QSize(20, 20))  # Set the size of the icon
        self.chat_button.setStyleSheet('background-color: lightgray; border: none;')  # Optional: set background color and remove border
        self.chat_button.clicked.connect(self.toggle_chat_window)  # Connect button click to open chat window

        # Configure exit button
        self.exit_button.setIcon(QIcon(exit))
        self.exit_button.setIconSize(QSize(20, 20))  # Set the size of the icon
        self.exit_button.setStyleSheet('background-color: lightgray; border: none;')  # Optional: set background color and remove border
        self.exit_button.clicked.connect(self.close)

        # Add buttons to layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.square_button)
        main_layout.addWidget(self.chat_button)
        main_layout.addWidget(self.exit_button)

    def toggle_chat_window(self):
        if self.chat_window and self.chat_window.isVisible():
            self.chat_window.hide()
            
        else:
            if not self.chat_window:
                self.chat_window = ChatWindow(self)
            self.chat_window.show()
            

    def open_ocr_window(self):
        # Run Tkinter window in a separate thread
        def run_tkinter():
            root = tk.Tk()  # Create a root Tk instance
            root.withdraw()  # Hide the root window
            OCR(root)  # Create the OCR window
            root.mainloop()  # Run Tkinter's event loop
        threading.Thread(target=run_tkinter, daemon=True).start()
    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

    def closeEvent(self, event):
        if self.chat_window:
            self.chat_window.close()
        if self.ocr_window:
            self.ocr_window.close()
        event.accept()
