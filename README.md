# Ollama Chat Application

This is a simple chat application built using `PyQt6` and `Tkinter` that integrates with the `Ollama` model server. It also offers a UI tool to utilize OCR for text extraction by draging a selection box and having OCR analyze the screenshot and has note saving functionality. You can use app either by cloning, downloading zip or by downloading the `.exe`.
![Chat Application Interface](./assets/ss.png)
## Installation

1. **Download the Zip or clone**: 
   - Navigate to root directory and run ```py main.py```
   - Install dependencies as needed

2. **To use the OCR tool**:
  - First install Google's Tesseract OCR model [here](https://github.com/tesseract-ocr/tesseract)
  - This app uses pytesseract more info can be found [here] https://github.com/h/pytesseract
  - Set up your systems enviromental variables as necessary
  - By default the software is install into your C:\Program Files\Tesseract-OCR\tesseract.exe if you're running Windows

  - When using the OCR every screenshot you process is automatically injected into chat, examples of usage would be to take a screenshot of those pesky Windows error messages that you cant copy/paste the text from, preform OCR, and in chat ask something like "What does this error mean" and hit enter. If you dont want the OCR output text injected into chat make sure to hit 'Clear' in the OCR window.

3. - This app automatically runs a script to start the Ollama serve upon starting app. You chage that in the ```main.py```

## Currently I dont have a updated exe for this due to the OCR binary complications, the exe available in release works it just lasks newer updated functionalities such as OCR and notes
