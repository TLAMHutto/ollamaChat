from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QPixmap, QIcon
from chat_window import ChatWindow
from notes_window import NotesWindow
from terminal import TerminalWindow
from ocr import OCR
import threading
import tkinter as tk
class MinimalistChatApp(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.chat_window = None
        self.ocr_window = None  # Add ocr_window reference
        self.notes_window = None
        self.terminal_window = None
        self.initUI()
        self.oldPos = self.pos()

    def initUI(self):
        self.setGeometry(1680, 992, 150, 25)  # Increase width to accommodate new button

        # Create main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        
        self.terminal_button = QPushButton(self)
        self.terminal_button.setFixedSize(25, 25)

        self.square_button = QPushButton(self)
        self.square_button.setFixedSize(25, 25)
        
        self.chat_button = QPushButton(self)
        self.chat_button.setFixedSize(25, 25)
        
        self.notes_button = QPushButton(self)
        self.notes_button.setFixedSize(25, 25)
        
        self.exit_button = QPushButton(self)
        self.exit_button.setFixedSize(25, 25)
        


        # Load the icon images
        scan = QPixmap('./assets/zoom-scan.png')
        chat = QPixmap('./assets/message-dots.png')
        exit = QPixmap('./assets/square-letter-x.png')
        notes = QPixmap('./assets/notes.png')
        terminal = QPixmap('./assets/terminal.png')
        
        self.terminal_button.setIcon(QIcon(terminal))
        self.terminal_button.setIconSize(QSize(20, 20))  # Set the size of the icon
        self.terminal_button.setStyleSheet('background-color: lightgray; border: none;')  # Optional: set background color and remove border
        self.terminal_button.clicked.connect(self.toggle_terminal_window)  # Connect button click to open OCR window
        
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
        self.exit_button.clicked.connect(self.close)  # Only close the window on click

        # Configure notes button (Fix the connection)
        self.notes_button.setIcon(QIcon(notes))
        self.notes_button.setIconSize(QSize(20, 20))  # Set the size of the icon
        self.notes_button.setStyleSheet('background-color: lightgray; border: none;')  # Optional: set background color and remove border
        self.notes_button.clicked.connect(self.toggle_notes_window)  # Connect to the correct method for toggling notes window
        # Add buttons to layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.terminal_button)
        main_layout.addWidget(self.square_button)
        main_layout.addWidget(self.chat_button)
        main_layout.addWidget(self.notes_button)
        main_layout.addWidget(self.exit_button)
        
  
    def toggle_terminal_window(self):
        try:
            if self.terminal_window and self.terminal_window.isVisible():
                self.terminal_window.hide()
            else:
                if not self.terminal_window:
                    self.terminal_window = TerminalWindow()
                self.terminal_window.show()
        except Exception as e:
            print(f"Error in toggle_terminal_window: {e}")

    def toggle_chat_window(self):
    # Close the notes window if it's open
        if self.notes_window and self.notes_window.isVisible():
            self.notes_window.hide()

        # Toggle the chat window
        if self.chat_window and self.chat_window.isVisible():
            self.chat_window.hide()
        else:
            if not self.chat_window:
                self.chat_window = ChatWindow(self)
            self.chat_window.show()

    def toggle_notes_window(self):
        # Close the chat window if it's open
        if self.chat_window and self.chat_window.isVisible():
            self.chat_window.hide()

        # Toggle the notes window
        if self.notes_window and self.notes_window.isVisible():
            self.notes_window.hide()
        else:
            if not self.notes_window:
                self.notes_window = NotesWindow(self)
            self.notes_window.show()

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
        if self.notes_window:
            self.notes_window.close()
        if self.terminal_window:
            self.terminal_window.close()
        event.accept()

