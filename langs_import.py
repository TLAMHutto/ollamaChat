import os

def list_files_with_extension(folder_path, file_extension):
    file_names = []
    
    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file ends with the specified extension
        if file_name.endswith(file_extension):
            # Add the file name without the extension to the list
            file_names.append(os.path.splitext(file_name)[0])
    
    # Join the list of file names using the "+" symbol
    return "+".join(file_names)

# Example usage
folder_path = r'C:\Program Files\Tesseract-OCR\tessdata'  # Update this to your folder path
file_extension = '.traineddata'  # Specify the extension you want to count (e.g., .txt, .py, .jpg)

file_names_combined = list_files_with_extension(folder_path, file_extension)
print(f"Files with '{file_extension}' extension: {file_names_combined}")
