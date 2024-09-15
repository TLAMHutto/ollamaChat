from tkinter import Tk, Label, Text, Scrollbar, VERTICAL, RIGHT, Y, Frame, Toplevel, Canvas
from tkinter import messagebox
from PIL import ImageTk, Image, ImageGrab
import pytesseract
import os

class OCR:
    def __init__(self, app):
        self.app = app
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def show_image(self, image):
        # Display the image in the GUI
        photo = ImageTk.PhotoImage(image)
        self.app.image_label.config(image=photo)
        self.app.image_label.image = photo

        # Define directories
        save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
        text_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgTxt")

        # Save image
        if save_dir:
            filename = "snip_latest.png"
            file_path = os.path.join(save_dir, filename)

            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            image.save(file_path)
            messagebox.showinfo("Image Saved", f"Image saved as {filename} in {save_dir}")

            # Perform OCR on the saved image
            text = pytesseract.image_to_string(Image.open(file_path))

            # Save the extracted text
            if not os.path.exists(text_dir):
                os.makedirs(text_dir)

            text_filename = "snip_latest.txt"
            text_file_path = os.path.join(text_dir, text_filename)

            with open(text_file_path, "w") as text_file:
                text_file.write(text)

            messagebox.showinfo("Text Extracted", f"Text extracted and saved as {text_filename} in {text_dir}")

            # Update the text display
            self.update_text_display(text_file_path)

    def update_text_display(self, text_file_path):
        if os.path.exists(text_file_path):
            with open(text_file_path, "r") as text_file:
                content = text_file.read()
                self.app.text_display.delete(1.0, "end")  # Clear existing text
                self.app.text_display.insert("end", content)  # Insert new text

class SnipTool:
    def __init__(self, app):
        self.app = app
        self.snip_surface = None
        self.canvas = None
        self.rect = None

    def start_snip(self):
        self.app.withdraw()  # Hide the main window
        self.snip_surface = Toplevel(self.app)
        self.snip_surface.attributes("-fullscreen", True)
        self.snip_surface.attributes("-alpha", 0.3)
        self.snip_surface.configure(cursor="cross")

        self.canvas = Canvas(self.snip_surface, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_snip_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)

        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        self.snip_surface.withdraw()
        self.app.deiconify()  # Show the main window again

        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.app.image_handler.show_image(image)

        self.snip_surface.destroy()

class MyApp(Tk):
    def __init__(self):
        super().__init__()

        self.title("Image and Text Display")

        # Image display setup
        self.image_label = Label(self)
        self.image_label.pack()

        # Text display setup
        self.text_display_frame = Frame(self)
        self.text_display_frame.pack()

        self.text_display = Text(self.text_display_frame, wrap='word', height=10, width=50)
        self.text_display.pack(side="left", fill="both", expand=True)

        self.scrollbar = Scrollbar(self.text_display_frame, orient=VERTICAL, command=self.text_display.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.text_display.config(yscrollcommand=self.scrollbar.set)

        # Initialize ImageHandler and SnipTool
        self.image_handler = OCR(self)
        self.snip_tool = SnipTool(self)

        # Add a button to start snipping
        self.snip_button = Label(self, text="Start Snipping", bg="lightblue", padx=10, pady=5)
        self.snip_button.pack(pady=10)
        self.snip_button.bind("<Button-1>", self.start_snip)

    def start_snip(self, event):
        self.snip_tool.start_snip()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
