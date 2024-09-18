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
        
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_notes)
        
        # Add buttons to button layout
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.clear_button)
        
        
        # Add widgets to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def clear_notes(self):
        self.text_edit.clear()
    
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

                # Extract just the file name (without the full path)
                file_display_name = file_name.split('/')[-1]  # For Linux/Mac paths
                if '\\' in file_name:  # For Windows paths
                    file_display_name = file_name.split('\\')[-1]
                
                # Update the QLabel to display the file name
                self.title_label.setText(f"Notes - {file_display_name}")
                
                # Show a message box indicating success
                QMessageBox.information(self, "Success", f"Notes loaded from {file_name}")
            except Exception as e:
                # Show an error message if something goes wrong
                QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")

                
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition().toPoint()
            self.resize_edge = self.get_resize_edge(event.pos())
            if self.resize_edge:
                self.resizing = True
            else:
                self.resizing = False

    def mouseMoveEvent(self, event):
        if self.resizing:
            self.resize_window(event.globalPosition().toPoint())
        elif event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
        
        self.update_cursor(event.pos())
        self.oldPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.resize_edge = None
        self.unsetCursor()

    def get_resize_edge(self, pos):
        if 0 <= pos.x() <= self.resize_margin:
            if 0 <= pos.y() <= self.resize_margin:
                return 'top_left'
            elif self.height() - self.resize_margin <= pos.y() <= self.height():
                return 'bottom_left'
            else:
                return 'left'
        return None

    def resize_window(self, global_pos):
        delta = global_pos - self.oldPos
        if self.resize_edge in ['left', 'top_left', 'bottom_left']:
            new_width = max(self.width() - delta.x(), 100)
            new_x = self.x() + self.width() - new_width
            self.setGeometry(new_x, self.y(), new_width, self.height())
        if self.resize_edge in ['top_left']:
            new_height = max(self.height() - delta.y(), 100)
            new_y = self.y() + self.height() - new_height
            self.setGeometry(self.x(), new_y, self.width(), new_height)
        elif self.resize_edge in ['bottom_left']:
            new_height = max(self.height() + delta.y(), 100)
            self.resize(self.width(), new_height)

    def update_cursor(self, pos):
        resize_edge = self.get_resize_edge(pos)
        if resize_edge == 'left':
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif resize_edge in ['top_left', 'bottom_left']:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        else:
            self.unsetCursor()

    def enterEvent(self, event):
        self.update_cursor(self.mapFromGlobal(self.cursor().pos()))

    def leaveEvent(self, event):
        self.unsetCursor()
