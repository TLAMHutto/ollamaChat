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

        # Create small square button
        self.square_button = QPushButton(self)
        self.square_button.setFixedSize(35, 35)  # Set fixed size for square button

        # Load the icon image
        icon_pixmap = QPixmap('./zoom-scan.png')
        self.square_button.setFixedSize(20, 20)
        # Set a smaller size for the icon
        icon_size = QSize(20, 20)  # Specify the desired size for the icon
        self.square_button.setIcon(QIcon(icon_pixmap))
        self.square_button.setIconSize(icon_size)  # Set the size of the icon

        self.square_button.setStyleSheet('background-color: lightgray; border: none;')  # Optional: set background color and remove border
        self.square_button.clicked.connect(self.open_ocr_window)  # Connect button click to open OCR window
        main_layout.addWidget(self.square_button)

        # Create chat window button
        self.chat_button = QPushButton('Open Chat', self)
        self.chat_button.clicked.connect(self.toggle_chat_window)
        main_layout.addWidget(self.chat_button)

        # Create exit button
        exit_button = QPushButton('Exit', self)
        exit_button.clicked.connect(self.close)
        main_layout.addWidget(exit_button)

        self.setLayout(main_layout)

    def toggle_chat_window(self):
        if self.chat_window and self.chat_window.isVisible():
            self.chat_window.hide()
            self.chat_button.setText('Open Chat')
        else:
            if not self.chat_window:
                self.chat_window = ChatWindow(self)
            self.chat_window.show()
            self.chat_button.setText('Close Chat')

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
