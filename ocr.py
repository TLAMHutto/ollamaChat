import tkinter as tk
from tkinter import ttk, Tk, Label, Text, Scrollbar, VERTICAL, RIGHT, Y, Frame, Toplevel, Canvas
from PIL import Image, ImageTk
import mss
import mss.tools
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to scrolling
        self.bind_mousewheel(self.canvas)
        self.bind_mousewheel(self.scrollable_frame)

    def bind_mousewheel(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel)
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

class OCR:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("OCR Window")
        self.window.geometry("500x700")  # Set initial size

        # Create a scrollable frame
        self.scroll_frame = ScrollableFrame(self.window)
        self.scroll_frame.pack(fill="both", expand=True)

        # Now add all widgets to self.scroll_frame.scrollable_frame instead of self.window
        self.select_button = ttk.Button(self.scroll_frame.scrollable_frame, text="Select Area", command=self.select_area)
        self.select_button.pack(padx=10, pady=10)

        self.result_label = ttk.Label(self.scroll_frame.scrollable_frame, text="")
        self.result_label.pack(padx=10, pady=10)

        # Create an image display area in the OCR window
        self.image_label = tk.Label(self.scroll_frame.scrollable_frame)
        self.image_label.pack(padx=10, pady=10)

        # Create a text field for OCR output
        self.text_output = tk.Text(self.scroll_frame.scrollable_frame, height=10, width=50)
        self.text_output.pack(padx=10, pady=10)

        # Create an OCR button
        self.ocr_button = ttk.Button(self.scroll_frame.scrollable_frame, text="Perform OCR", command=self.perform_ocr)
        self.ocr_button.pack(padx=10, pady=10)

    def select_area(self):
        self.window.withdraw()  # Hide the OCR window
        self.root.withdraw()    # Hide the main window
        self.screenshot = mss.mss()
        self.root.after(100, self.start_selection)

    def start_selection(self):
        self.select_window = tk.Toplevel(self.root)
        self.select_window.attributes('-fullscreen', True)
        self.select_window.attributes('-alpha', 0.3)
        self.select_window.configure(cursor="cross")

        self.canvas = tk.Canvas(self.select_window, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.select_window.bind("<ButtonPress-1>", self.on_press)
        self.select_window.bind("<B1-Motion>", self.on_drag)
        self.select_window.bind("<ButtonRelease-1>", self.on_release)

        self.rect = None
        self.start_x = None
        self.start_y = None

    def on_press(self, event):
        self.start_x = self.select_window.winfo_pointerx()
        self.start_y = self.select_window.winfo_pointery()
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_drag(self, event):
        cur_x = self.select_window.winfo_pointerx()
        cur_y = self.select_window.winfo_pointery()
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        end_x = self.select_window.winfo_pointerx()
        end_y = self.select_window.winfo_pointery()
        self.select_window.destroy()
        self.window.deiconify()  # Show the OCR window again

        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        width = abs(end_x - self.start_x)
        height = abs(end_y - self.start_y)

        monitor = {"top": top, "left": left, "width": width, "height": height}
        screenshot = self.screenshot.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output="screenshot.png")

        self.result_label.config(text="Screenshot captured")
        self.display_image("screenshot.png")

    def display_image(self, image_path):
        # Open the image file
        img = Image.open(image_path)
        
        # Resize the image to fit within a maximum size (e.g., 400x400)
        img.thumbnail((400, 400))
        
        # Convert the Image object to a PhotoImage object
        photo = ImageTk.PhotoImage(img)
        
        # Update the image in the label
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference to avoid garbage collection
        
    def perform_ocr(self):
        try:
            text = pytesseract.image_to_string(Image.open("screenshot.png"))
            self.text_output.delete(1.0, tk.END)  # Clear previous text
            self.text_output.insert(tk.END, text)
            self.result_label.config(text="OCR completed")
            
            # Save the OCR text to a file
            with open("ocr_output.txt", "w", encoding="utf-8") as f:
                f.write(text)
            
        except Exception as e:
            self.result_label.config(text=f"OCR failed: {str(e)}")

    def run(self):
        self.window.mainloop()