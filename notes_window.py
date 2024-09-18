from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt

class NotesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.initUI()
        self.oldPos = self.pos()
        self.resizing = True
        self.resize_edge = None
        self.resize_margin = 10  # The width of the "resizable" border area
        self.token_count = 0

    def initUI(self):
        self.setGeometry(1620, 390, 300, 600)
        self.setWindowTitle('Notes')
        
        # Create layout for the note-taking area
        layout = QVBoxLayout(self)
        
        # Add a QLabel for the title or instructions
        self.title_label = QLabel("Notes", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        
        # Add a QTextEdit for writing notes
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Write your notes here...")  # Placeholder text
        
        # Add a horizontal layout for buttons
        button_layout = QHBoxLayout()
        
        # Add a Save button
        self.save_button = QPushButton("Save Notes", self)
        self.save_button.clicked.connect(self.save_notes_to_file)
        
        # Add an Open button
        self.open_button = QPushButton("Open Notes", self)
        self.open_button.clicked.connect(self.open_notes_from_file)
        
        # Add buttons to button layout
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.open_button)
        
        # Connect the text change signal to a slot for updating token count (optional)
        self.text_edit.textChanged.connect(self.update_token_count)
        
        # Add widgets to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def update_token_count(self):
        # Optionally, track the token or word count in real-time
        text = self.text_edit.toPlainText()
        self.token_count = len(text.split())  # Count words by splitting the text by spaces

    def save_notes_to_file(self):
        # Open a file dialog to save the file
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Notes", "", "Text Files (*.txt);;All Files (*)")

        if file_name:  # If a valid file name was chosen
            try:
                with open(file_name, 'w') as file:
                    file.write(self.text_edit.toPlainText())  # Write the notes to the file
                # Show a message box indicating success
                QMessageBox.information(self, "Success", f"Notes saved to {file_name}")
            except Exception as e:
                # Show an error message if something goes wrong
                QMessageBox.critical(self, "Error", f"Failed to save notes: {str(e)}")

    def open_notes_from_file(self):
        # Open a file dialog to select a file to open
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Notes", "", "Text Files (*.txt);;All Files (*)")

        if file_name:  # If a valid file name was selected
            try:
                with open(file_name, 'r') as file:
                    content = file.read()  # Read the file's content
                    self.text_edit.setPlainText(content)  # Set the content to the QTextEdit
                # Show a message box indicating success
                QMessageBox.information(self, "Success", f"Notes loaded from {file_name}")
            except Exception as e:
                # Show an error message if something goes wrong
                QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")
