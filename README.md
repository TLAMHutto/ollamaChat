# Ollama Chat Application

This is a simple chat application built using `PyQt6` and `Tkinter` that integrates with the `Ollama` model server. It also offers a UI tool to utilize OCR for text extraction by dragging a selection box and having OCR analyze the screenshot and has note saving functionality. You can use app either by cloning, downloading zip or by downloading the `.exe`.
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

I built a simple chat application that integrates with Ollama to run models locally.

What My Project Does:

Along with the Ollama model chat, it also offers a UI tool to utilize OCR for text extraction and has note saving functionality.

Target Audience:

It has a compact and always-on-top display, great for on the fly questions. I found it very useful for debugging windows error messages that dont let you copy/paste the text in the window, the text output of OCR is directly injected into the LLM.

Comparison:

I havent found any other Ollama chat UIs that have OCR and Note saving

https://github.com/TLAMHutto/ollamaChat