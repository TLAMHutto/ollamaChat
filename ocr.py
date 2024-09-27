import os
import tkinter as tk
from tkinter import ttk, Tk, Label, Text, Scrollbar, VERTICAL, RIGHT, Y, Frame, Toplevel, Canvas
from PIL import Image, ImageTk
import mss
import mss.tools
import pytesseract
import itertools
import threading
from langdetect import detect
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
tess_map = {
    "afr": "Afrikaans", "amh": "Amharic", "ara": "Arabic", "asm": "Assamese",
    "aze": "Azerbaijani", "aze_cyrl": "Azerbaijani (Cyrillic)", 
    "bel": "Belarusian", "ben": "Bengali", "bod": "Tibetan", "bos": "Bosnian",
    "bre": "Breton", "bul": "Bulgarian", "cat": "Catalan", "ceb": "Cebuano",
    "ces": "Czech", "chi_sim": "Chinese (Simplified)",
    "chi_sim_vert": "Chinese (Simplified, Vertical)",
    "chi_tra": "Chinese (Traditional)", "chi_tra_vert": "Chinese (Traditional, Vertical)",
    "chr": "Cherokee", "cos": "Corsican", "cym": "Welsh", "dan": "Danish",
    "dan_frak": "Danish (Fraktur)", "deu": "German", "deu_frak": "German (Fraktur)",
    "deu_latf": "German (Latin, Fraktur)", "div": "Dhivehi",
    "dzo": "Dzongkha", "ell": "Greek", "eng": "English", "enm": "Middle English",
    "epo": "Esperanto", "equ": "Math/Symbol", "est": "Estonian", "eus": "Basque",
    "fao": "Faroese", "fas": "Persian", "fil": "Filipino", "fin": "Finnish",
    "fra": "French", "frm": "Middle French", "fry": "Frisian", "gla": "Scottish Gaelic",
    "gle": "Irish", "glg": "Galician", "grc": "Ancient Greek", "guj": "Gujarati",
    "hat": "Haitian", "heb": "Hebrew", "hin": "Hindi", "hrv": "Croatian",
    "hun": "Hungarian", "hye": "Armenian", "iku": "Inuktitut", "ind": "Indonesian",
    "isl": "Icelandic", "ita": "Italian", "ita_old": "Old Italian",
    "jav": "Javanese", "jpn": "Japanese", "jpn_vert": "Japanese (Vertical)",
    "kan": "Kannada", "kat": "Georgian", "kat_old": "Old Georgian",
    "kaz": "Kazakh", "khm": "Khmer", "kir": "Kyrgyz", "kmr": "Kurdish",
    "kor": "Korean", "kor_vert": "Korean (Vertical)",
    "lao": "Lao", "lat": "Latin", "lav": "Latvian", "lit": "Lithuanian",
    "ltz": "Luxembourgish", "mal": "Malayalam", "mar": "Marathi", "mkd": "Macedonian",
    "mlt": "Maltese", "mon": "Mongolian", "mri": "Maori", "msa": "Malay",
    "mya": "Burmese", "nep": "Nepali", "nld": "Dutch", "nor": "Norwegian",
    "oci": "Occitan", "ori": "Oriya", "osd": "Orientation Script Detection",
    "pan": "Punjabi", "pol": "Polish", "por": "Portuguese",
    "pus": "Pashto", "que": "Quechua", "ron": "Romanian", "rus": "Russian",
    "san": "Sanskrit", "sin": "Sinhala", "slk": "Slovak", "slk_frak": "Slovak (Fraktur)",
    "slv": "Slovenian", "snd": "Sindhi", "spa": "Spanish", "spa_old": "Old Spanish",
    "sqi": "Albanian", "srp": "Serbian", "srp_latn": "Serbian (Latin)",
    "sun": "Sundanese", "swa": "Swahili", "swe": "Swedish",
    "syr": "Syriac", "tam": "Tamil", "tat": "Tatar", "tel": "Telugu",
    "tgk": "Tajik", "tgl": "Tagalog", "tha": "Thai", "tir": "Tigrinya",
    "ton": "Tongan", "tur": "Turkish", "uig": "Uyghur", "ukr": "Ukrainian",
    "urd": "Urdu", "uzb": "Uzbek", "uzb_cyrl": "Uzbek (Cyrillic)",
    "vie": "Vietnamese", "yid": "Yiddish", "yor": "Yoruba"
}
def set_dark_theme(root):
    style = ttk.Style(root)
    style.theme_create("dark_theme", parent="alt", settings={
        "TFrame": {"configure": {"background": "#1e1e1e"}},
        "TLabel": {"configure": {"background": "#1e1e1e", "foreground": "#dcdcdc"}},
        "TButton": {"configure": {"background": "#3c3c3c", "foreground": "#dcdcdc"}},
        "TEntry": {"configure": {"fieldbackground": "#0f0f0f", "foreground": "#dcdcdc"}},
        "TText": {"configure": {"background": "#0f0f0f", "foreground": "#dcdcdc"}},
        "TCombobox": {"configure": {"fieldbackground": "#0f0f0f", "foreground": "#dcdcdc"}},
        "Vertical.TScrollbar": {"configure": {"background": "#3c3c3c", "troughcolor": "#1e1e1e"}},
    })
    style.theme_use("dark_theme")

    # Configure colors for standard Tkinter widgets
    root.configure(bg="#1e1e1e")
    root.option_add("*Background", "#1e1e1e")
    root.option_add("*Foreground", "#dcdcdc")
    root.option_add("*Entry.Background", "#0f0f0f")
    root.option_add("*Entry.Foreground", "#dcdcdc")
    root.option_add("*Text.Background", "#0f0f0f")
    root.option_add("*Text.Foreground", "#dcdcdc")
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
        widget.bind("<Button-4>", self._on_mousewheel)  # For Linux
        widget.bind("<Button-5>", self._on_mousewheel)  # For Linux

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:  # Scroll down
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:  # Scroll up
            self.canvas.yview_scroll(-1, "units")
class AnimatedLabel(ttk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._is_running = False
        self._spinner = itertools.cycle(['-', '/', '|', '\\'])
        self._animation_id = None

    def start(self):
        """Start the spinner animation."""
        if not self._is_running:
            self._is_running = True
            self._animate()

    def stop(self):
        """Stop the spinner animation."""
        self._is_running = False
        if self._animation_id:
            self.after_cancel(self._animation_id)  # Cancel the scheduled `after` call
            self._animation_id = None
        self.configure(text="")  # Clear the label

    def _animate(self):
        """Animate the spinner by updating the text periodically using after()."""
        if self._is_running:
            self.configure(text=next(self._spinner) + " Processing...")
            self._animation_id = self.after(100, self._animate)
            
class OCR:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("OCR Window")
        set_dark_theme(self.window)
        
        width = 400
        height = 600
        x_offset = 1500
        y_offset = 50

        # Set the geometry of the window: "widthxheight+x_offset+y_offset"
        self.window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

        # Create a scrollable frame
        self.scroll_frame = ScrollableFrame(self.window)
        self.scroll_frame.pack(fill="both", expand=True)

        # Add the animated label
        self.loading_label = AnimatedLabel(self.scroll_frame.scrollable_frame)
        self.loading_label.pack(padx=10, pady=10)

        # Add the Select Area button to the scrollable frame
        self.select_button = ttk.Button(self.scroll_frame.scrollable_frame, text="Select Area", command=self.select_area)
        self.select_button.pack(padx=10, pady=10)

        # Create a dropdown menu (combobox) under the Select Area button
        # Set the StringVar for the dropdown
        self.dropdown_var = tk.StringVar()

        # Create the Combobox with sorted language values
        self.dropdown = ttk.Combobox(self.scroll_frame.scrollable_frame, textvariable=self.dropdown_var, state='readonly')
        self.dropdown['values'] = sorted(tess_map.values())

        # Set "English" as the default selection
        self.dropdown_var.set("English")  # Use the name directly

        # Ensure the Combobox reflects the default selection
        self.dropdown.pack(padx=10, pady=10)
        
        self.result_label = ttk.Label(self.scroll_frame.scrollable_frame, text="")
        self.result_label.pack(padx=10, pady=10)

        self.lang_label = ttk.Label(self.scroll_frame.scrollable_frame, text="")
        self.lang_label.pack(padx=10, pady=10)
        
        # Create an image display area in the OCR window
        self.image_label = tk.Label(self.scroll_frame.scrollable_frame)
        self.image_label.pack(padx=10, pady=10)

        # Create a text field for OCR output
        self.text_output = tk.Text(self.scroll_frame.scrollable_frame, height=10, width=50)
        self.text_output.pack(padx=10, pady=10)

        self.button_frame = ttk.Frame(self.scroll_frame.scrollable_frame)
        self.button_frame.pack(padx=10, pady=10)

        # Create an OCR button
        self.ocr_button = ttk.Button(self.button_frame, text="Perform OCR", command=self.perform_ocr)
        self.ocr_button.pack(side=tk.LEFT, padx=(0, 5))

        # Create a Clear button
        self.clear_button = ttk.Button(self.button_frame, text="Clear", command=self.clear_ocr)
        self.clear_button.pack(side=tk.LEFT, padx=(5, 0))

        self.lang_button = ttk.Button(self.button_frame, text="Language Detection", command=self.lang_detect)
        self.lang_button.pack(side=tk.LEFT, padx=(5, 0))
        


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
        mss.tools.to_png(screenshot.rgb, screenshot.size, output="./assets/screenshot.png")

        self.result_label.config(text="Screenshot captured")
        self.display_image("./assets/screenshot.png")

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
            # Get the selected option's full name
            selected_option = self.dropdown_var.get()
            # Get the corresponding code from tess_map
            selected_code = [code for code, name in tess_map.items() if name == selected_option][0]
            
            # Perform OCR using the selected language code
            text = pytesseract.image_to_string(Image.open("./assets/screenshot.png"), lang=selected_code)
            
            self.text_output.delete(1.0, tk.END)  # Clear previous text
            self.text_output.insert(tk.END, text)
            self.result_label.config(text="OCR completed")
            with open("./assets/ocr_output.txt", "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}")
 
    def lang_detect(self):
        self.loading_label.start()
        self.lang_button.config(state=tk.DISABLED)  
        def run_ocr():
            detect_map = {
        'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali', 
        'ca': 'Catalan', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 
        'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 
        'et': 'Estonian', 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 
        'gu': 'Gujarati', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian', 
        'hu': 'Hungarian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 
        'kn': 'Kannada', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 
        'mk': 'Macedonian', 'ml': 'Malayalam', 'mr': 'Marathi', 'ne': 'Nepali', 
        'nl': 'Dutch', 'no': 'Norwegian', 'pa': 'Punjabi', 'pl': 'Polish', 
        'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak', 
        'sl': 'Slovenian', 'so': 'Somali', 'sq': 'Albanian', 'sv': 'Swedish', 
        'sw': 'Swahili', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 
        'tl': 'Tagalog', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 
        'vi': 'Vietnamese', 'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)'
            }
            try:
                text = pytesseract.image_to_string(Image.open("./assets/screenshot.png"), lang='afr+amh+ara+asm+aze+aze_cyrl+bel+ben+bod+bos+bre+bul+cat+ceb+ces+chi_sim+chi_sim_vert+chi_tra+chi_tra_vert+chr+cos+cym+dan+dan_frak+deu+deu_frak+deu_latf+div+dzo+ell+eng+enm+epo+equ+est+eus+fao+fas+fil+fin+fra+frm+fry+gla+gle+glg+grc+guj+hat+heb+hin+hrv+hun+hye+iku+ind+isl+ita+ita_old+jav+jpn+jpn_vert+kan+kat+kat_old+kaz+khm+kir+kmr+kor+kor_vert+lao+lat+lav+lit+ltz+mal+mar+mkd+mlt+mon+mri+msa+mya+nep+nld+nor+oci+ori+osd+pan+pol+por+pus+que+ron+rus+san+sin+slk+slk_frak+slv+snd+spa+spa_old+sqi+srp+srp_latn+sun+swa+swe+syr+tam+tat+tel+tgk+tgl+tha+tir+ton+tur+uig+ukr+urd+uzb+uzb_cyrl+vie+yid+yor')
                lang = detect(text)
                full_lang_name = detect_map.get(lang, 'Unknown language')
                
                self.window.after(0, lambda: self._update_gui(text, full_lang_name))
                
                with open("./assets/ocr_output.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                
            except Exception as e:
                self.window.after(0, lambda: self.lang_label.config(text=f"Language Detection Failed: {str(e)}"))
            finally:
                self.window.after(0, self._finish_processing)

        threading.Thread(target=run_ocr, daemon=True).start()

    def _update_gui(self, text, full_lang_name):
        self.window.after(0, lambda: self.text_output.delete(1.0, tk.END))
        self.window.after(0, lambda: self.insert_text_in_chunks(text))
        self.window.after(0, lambda: self.lang_label.config(text=f'Language detected as: {full_lang_name}'))

    def insert_text_in_chunks(self, text, index=0, chunk_size=100):
        if index < len(text):
            self.text_output.insert(tk.END, text[index:index + chunk_size])
            self.window.after(1, self.insert_text_in_chunks, text, index + chunk_size)

    def _finish_processing(self):
        # Schedule the stop() call and button re-enabling to happen on the main thread
        if self.loading_label.winfo_exists():
            # Ensure that stop() runs on the main thread using after
            self.window.after(0, lambda: self.loading_label.stop())
        else:
            print("Warning: Loading label no longer exists.")

        # Re-enable the button safely on the main thread
        self.window.after(0, self.lang_button.config, {"state": tk.NORMAL})

    def clear_ocr(self):
        try:
            # Delete the ocr_output.txt file
            if os.path.exists("./assets/ocr_output.txt"):
                os.remove("./assets/ocr_output.txt")
                self.result_label.config(text="OCR output cleared")
            else:
                self.result_label.config(text="No OCR output to clear")

            # Clear the text output field
            self.text_output.delete(1.0, tk.END)
            self.image_label.config(image='')  # Clear the image in the label
            self.image_label.image = None  # Remove the reference to the image
            self.lang_label.config(text='')
        except Exception as e:
            self.result_label.config(text=f"Clear failed: {str(e)}")

    def run(self):
        self.window.mainloop()