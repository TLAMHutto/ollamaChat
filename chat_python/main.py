import sys
import ollama
import re
import html
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QComboBox, QLineEdit
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon, QTextCursor

class ChatWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.initUI()
        self.oldPos = self.pos()

    def initUI(self):
        self.setGeometry(1620, 390, 300, 600)

        layout = QVBoxLayout()

        # Create a horizontal layout for the dropdown and refresh button
        top_layout = QHBoxLayout()

        # Add the model dropdown
        self.model_dropdown = QComboBox(self)
        self.populate_model_dropdown()
        top_layout.addWidget(self.model_dropdown)

        # Add the refresh button with an icon
        self.refresh_button = QPushButton(self)
        self.refresh_button.setIcon(QIcon.fromTheme("view-refresh"))  # Use system theme icon
        self.refresh_button.setToolTip("Clear chat")
        self.refresh_button.clicked.connect(self.clear_chat)
        top_layout.addWidget(self.refresh_button)

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
            self.chat_area.append(f"User: {message}")
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
                self.chat_area.append(f"AI ({model}): {ai_message}")
            except Exception as e:
                self.chat_area.append(f"Error: Failed to get response from {model}. {str(e)}")

    def populate_model_dropdown(self):
        try:
            models_dict = ollama.list()
            models = models_dict.get('models', [])
            for model in models:
                model_name = model.get("name", "No name key")
                self.model_dropdown.addItem(model_name)
        except Exception as e:
            self.chat_area.append(f"Error fetching models: {str(e)}")
    def append_message(self, sender, message):
            # Format the message with code blocks
            formatted_message = self.format_message(message)
            
            # Append the formatted message to the chat area
            self.chat_area.append(f"<b>{sender}:</b> {formatted_message}")
            
            # Scroll to the bottom of the chat area
            self.chat_area.moveCursor(QTextCursor.MoveOperation.End)
            self.chat_area.ensureCursorVisible()

    def format_message(self, message):
        # Use regex to find code blocks (text between triple backticks)
        code_block_pattern = r'```([\s\S]*?)```'
        
        def replace_code_block(match):
            # Escape the code for HTML rendering
            code = html.escape(match.group(1).strip())
            return f'<pre style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;"><code>{code}</code></pre>'
        
        # Replace code blocks with formatted HTML
        formatted_message = re.sub(code_block_pattern, replace_code_block, message)
        
        # Replace newlines with <br> tags for proper HTML rendering
        formatted_message = formatted_message.replace('\n', '<br>')
    
        return formatted_message

    def clear_chat(self):
        self.chat_area.clear()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

class MinimalistChatApp(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.chat_window = None
        self.initUI()
        self.oldPos = self.pos()

    def initUI(self):
        self.setGeometry(1765, 992, 100, 35)

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
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MinimalistChatApp()
    ex.show()
    sys.exit(app.exec())