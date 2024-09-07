import tkinter as tk
from PIL import Image, ImageTk

class DraggableWindow:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove the title bar and borders
        self.root.attributes("-topmost", True)  # Keep the button window on top

        # Load and resize images
        self.open_icon = self.load_and_resize_image("chat.png", size=(24, 24))  # Resize to 24x24
        self.close_icon = self.load_and_resize_image("exit.png", size=(24, 24))  # Resize to 24x24

        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        # Create buttons
        self.open_button = tk.Button(button_frame, image=self.open_icon, command=self.toggle_chat_window)
        self.open_button.pack(side="left", padx=5)

        self.close_button = tk.Button(button_frame, image=self.close_icon, command=self.root.quit)  # Close the main window
        self.close_button.pack(side="left", padx=5)

        self.chat_window = None
        self.root.bind("<Button-1>", self.start_move_main)
        self.root.bind("<B1-Motion>", self.do_move_main)

        # Track the offset between the main window and the chat window
        self.offset_x = 0
        self.offset_y = 0

    def load_and_resize_image(self, image_path, size):
        """Load an image from a file and resize it."""
        with Image.open(image_path) as img:
            img = img.resize(size, Image.LANCZOS)  # Resize image
            return ImageTk.PhotoImage(img)

    def toggle_chat_window(self):
        if self.chat_window is None or not self.chat_window.winfo_exists():
            self.create_chat_window()
        elif self.chat_window.state() == 'normal':
            self.chat_window.withdraw()
        else:
            self.chat_window.deiconify()

    def create_chat_window(self):
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title("Chat Window")
        self.chat_window.geometry("300x200+1591+752")  # Width x Height + X + Y
        self.chat_window.overrideredirect(True)  # Remove the title bar and borders
        self.chat_window.attributes("-topmost", True)  # Keep the chat window on top

        # Create a frame to hold the buttons and dropdown
        main_frame = tk.Frame(self.chat_window)
        main_frame.pack(fill="both", expand=True)

        # Create a frame for buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side="top", fill="x")

        # Add close button to chat window
        close_button = tk.Button(button_frame, image=self.close_icon, command=self.chat_window.withdraw)
        close_button.pack(side="right", padx=5)

        # Create a dropdown selection box
        self.options = ["Option 1", "Option 2", "Option 3"]
        self.selected_option = tk.StringVar(value=self.options[0])  # Default value

        dropdown = tk.OptionMenu(main_frame, self.selected_option, *self.options)
        dropdown.pack(pady=10)

        self.chat_window.protocol("WM_DELETE_WINDOW", self.toggle_chat_window)
        
        # Bind events for dragging the chat window
        self.chat_window.bind("<Button-1>", self.start_move_chat)
        self.chat_window.bind("<B1-Motion>", self.do_move_chat)

        self.chat_window.withdraw()

    def start_move_main(self, event):
        self.x = event.x_root
        self.y = event.y_root

        # If the chat window is open, calculate the offset
        if self.chat_window and self.chat_window.winfo_ismapped():
            self.offset_x = event.x_root - self.chat_window.winfo_rootx()
            self.offset_y = event.y_root - self.chat_window.winfo_rooty()

    def do_move_main(self, event):
        dx = event.x_root - self.x
        dy = event.y_root - self.y
        new_x = self.root.winfo_x() + dx
        new_y = self.root.winfo_y() + dy

        # Update main window position
        self.root.geometry(f'+{new_x}+{new_y}')
        print(f'Main Window Position: {new_x}, {new_y}')

        # Update chat window position if it is open
        if self.chat_window and self.chat_window.winfo_ismapped():
            self.chat_window.geometry(f'+{new_x + self.offset_x}+{new_y + self.offset_y}')
            print(f'Chat Window Position: {self.chat_window.winfo_x()}, {self.chat_window.winfo_y()}')

        # Update the starting point for the next move
        self.x = event.x_root
        self.y = event.y_root

    def start_move_chat(self, event):
        # This method is no longer used, but we need it for consistency
        pass

    def do_move_chat(self, event):
        # This method is no longer used, but we need it for consistency
        pass
