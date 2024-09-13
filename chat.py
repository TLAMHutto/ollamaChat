import re
import html
import sys
from PyQt6 import QtCore
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QLineEdit, QPushButton, QComboBox, QLabel, QApplication)
from PyQt6.QtGui import QTextCursor, QIcon, QPainter, QColor
from PyQt6.QtCore import Qt, QPoint, QBuffer, QRect, QTimer
import ollama
import tokenize
import io
import pytesseract
from PIL import Image
import re
import html
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QLineEdit, QPushButton, QComboBox, QLabel)
from PyQt6.QtGui import QTextCursor, QIcon
from PyQt6.QtCore import Qt, QPoint
import ollama

class ChatWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.initUI()
        self.oldPos = self.pos()
        self.token_count = 0

    def initUI(self):
        self.setGeometry(1620, 390, 300, 600)

        layout = QVBoxLayout()

        # Create a horizontal layout for the dropdown, refresh button, and token count
        top_layout = QHBoxLayout()

        # Add the model dropdown
        self.model_dropdown = QComboBox(self)
        self.populate_model_dropdown()
        top_layout.addWidget(self.model_dropdown)

        # Add the refresh button with an icon
        self.refresh_button = QPushButton(self)
        self.refresh_button.setIcon(QIcon.fromTheme("view-refresh"))
        self.refresh_button.setToolTip("Clear chat")
        self.refresh_button.clicked.connect(self.clear_chat)
        top_layout.addWidget(self.refresh_button)

        # Add the token count label
        self.token_count_label = QLabel("Tokens: 0", self)
        top_layout.addWidget(self.token_count_label)

        layout.addLayout(top_layout)

        # Add the chat area
        self.chat_area = QTextEdit(self)
        self.chat_area.setReadOnly(True)
        layout.addWidget(self.chat_area)

        # Add the text input at the bottom of the window
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Type your message here...")
        layout.addWidget(self.text_input)

        # Connect the return key (Enter) press to send message action
        self.text_input.returnPressed.connect(self.send_message)

        self.setLayout(layout)

    def send_message(self):
        message = self.text_input.text().strip()
        if message:
            self.append_message("User", message)
            self.text_input.clear()
            
            # Get the selected model
            model = self.model_dropdown.currentText()
            
            try:
                # Send message to Ollama and get response
                response = ollama.chat(model=model, messages=[
                    {
                        'role': 'user',
                        'content': message,
                    },
                ])
                
                # Display the AI's response
                ai_message = response['message']['content']
                self.append_message(f"AI ({model})", ai_message)
            except Exception as e:
                self.append_message("Error", f"Failed to get response from {model}. {str(e)}")

    def populate_model_dropdown(self):
        try:
            models_dict = ollama.list()
            models = models_dict.get('models', [])
            for model in models:
                model_name = model.get("name", "No name key")
                self.model_dropdown.addItem(model_name)
        except Exception as e:
            self.append_message("Error", f"Error fetching models: {str(e)}")

    def append_message(self, sender, message):
        # Format the message with code blocks
        formatted_message = self.format_message(message)
        
        # Append the formatted message to the chat area
        self.chat_area.append(f"<b>{sender}:</b> {formatted_message}")
        
        # Update token count
        self.update_token_count(message)
        
        # Scroll to the bottom of the chat area
        self.chat_area.moveCursor(QTextCursor.MoveOperation.End)
        self.chat_area.ensureCursorVisible()

    def format_message(self, message):
        # Use regex to find code blocks (text between triple backticks)
        code_block_pattern = r'```([\s\S]*?)```'
        
        def replace_code_block(match):
            # Escape the code for HTML rendering
            code = html.escape(match.group(1).strip())
            return f'<pre style="background-color: #000000; padding: 10px; border-radius: 5px;"><code>{code}</code></pre>'
        
        # Replace code blocks with formatted HTML
        formatted_message = re.sub(code_block_pattern, replace_code_block, message)
        
        # Replace newlines with <br> tags for proper HTML rendering
        formatted_message = formatted_message.replace('\n', '<br>')
    
        return formatted_message

    def clear_chat(self):
        self.chat_area.clear()
        self.token_count = 0
        self.update_token_count_label()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

    def update_token_count(self, message):
        # Simple word-based tokenization
        tokens = message.split()
        self.token_count += len(tokens)
        self.update_token_count_label()

    def update_token_count_label(self):
        self.token_count_label.setText(f"Tokens: {self.token_count}")
        
class OCRWindow(QWidget):
    def __init__(self):
        super().__init__(None, QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowOpacity(0.3)
        self.setCursor(QtCore.Qt.CursorShape.CrossCursor)
        self.setGeometry(QGuiApplication.primaryScreen().geometry())
        self.start = QPoint()
        self.end = QPoint()
        self.drawing = False

    def paintEvent(self, event):
        if self.drawing:
            painter = QPainter(self)
            painter.setPen(QColor(255, 0, 0))
            painter.drawRect(QRect(self.start, self.end))

    def mousePressEvent(self, event):
        print(f"Mouse pressed at: {event.pos()}")
        self.start = event.pos()
        self.end = event.pos()
        self.drawing = True

    def mouseMoveEvent(self, event):
        if self.drawing:
            print(f"Mouse moved to: {event.pos()}")
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        print(f"Mouse released at: {event.pos()}")
        self.drawing = False
        x1, y1 = min(self.start.x(), self.end.x()), min(self.start.y(), self.end.y())
        x2, y2 = max(self.start.x(), self.end.x()), max(self.start.y(), self.end.y())
        self.perform_ocr(x1, y1, x2 - x1, y2 - y1)
        
    def perform_ocr(self, x, y, width, height):
        print(f"Performing OCR on region: ({x}, {y}, {width}, {height})")
        screen = QGuiApplication.primaryScreen().grabWindow(0, x, y, width, height)
        image = screen.toImage()
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QBuffer.OpenModeFlag.ReadWrite)
        image.save(buffer, "PNG")
        pil_image = Image.open(io.BytesIO(buffer.data()))
        text = pytesseract.image_to_string(pil_image)
        print(f"OCR result: {text}")
        # Delay hiding the OCR window to ensure the result window is shown
        QTimer.singleShot(10, self.hide)
        self.show_result(text)

    def show_result(self, text):
        print(f"Showing result window with text: {text}")
        result_window = QWidget(None, QtCore.Qt.WindowType.Window)
        result_window.setWindowTitle("OCR Result")
        layout = QHBoxLayout()
        label = QLabel(text)
        layout.addWidget(label)
        result_window.setLayout(layout)
        result_window.resize(400, 200)  # Set size for visibility
        result_window.move(100, 100)    # Move to a visible location
        result_window.show()

                
class MinimalistChatApp(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.chat_window = None
        self.ocr_window = None
        self.initUI()
        self.oldPos = self.pos()

    def initUI(self):
        self.setGeometry(1765, 992, 150, 35)  # Increased width to accommodate the new button

        # Create main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Create chat window button
        self.chat_button = QPushButton('Open Chat', self)
        self.chat_button.clicked.connect(self.toggle_chat_window)
        main_layout.addWidget(self.chat_button)

        # Create OCR button
        ocr_button = QPushButton('OCR', self)
        ocr_button.clicked.connect(self.toggle_ocr_window)
        main_layout.addWidget(ocr_button)

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

    def toggle_ocr_window(self):
        if not self.ocr_window:
            self.ocr_window = OCRWindow()
        self.ocr_window.show()

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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MinimalistChatApp()
    ex.show()
    sys.exit(app.exec())