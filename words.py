import os

# Specify the directory of your codebase
directory = r"C:\Users\keaton\projects\Chat\chat_python"

# Specify the file extensions you want to include
file_extensions = [".js", ".jsx", ".css", ".html", ".py", ".ts"]

# Specify folders to exclude
excluded_folders = ["node_modules", "venv", ".git", "build", "dist", "_pychace_"]  # Add any other folders you want to exclude

def count_words_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        words = content.split()
        return len(words)

def count_words_in_directory(directory, extensions, excluded_folders):
    total_words = 0
    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to skip excluded folders
        dirs[:] = [d for d in dirs if d not in excluded_folders]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                total_words += count_words_in_file(filepath)
    return total_words

# Count words in the codebase, excluding specified folders
total_words = count_words_in_directory(directory, file_extensions, excluded_folders)
print(f"Total words in the codebase: {total_words}")
