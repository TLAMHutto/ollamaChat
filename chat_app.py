from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QPoint
from chat_window import ChatWindow

class MinimalistChatApp(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.chat_window = None
        self.ocr_window = None  # Add ocr_window reference
        self.initUI()
        self.oldPos = self.pos()
        self.ocr_window = None
    def initUI(self):
        self.setGeometry(1680, 992, 100, 35)

        # Create main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

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
