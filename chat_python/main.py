# main.py
import tkinter as tk
from draggable_window import DraggableWindow

def main():
    root = tk.Tk()
    root.geometry("100x35+1792+965")  # Width x Height + X + Y
    app = DraggableWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
