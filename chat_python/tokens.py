import tokenize
import io

def count_tokens(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize the code
    tokens = tokenize.tokenize(io.BytesIO(code.encode('utf-8')).readline)
    # Count tokens, excluding encoding token
    return len([token for token in tokens if token.type != tokenize.ENCODING])

# Example usage
file_path = 'main.py'
num_tokens = count_tokens(file_path)
print(f"Number of tokens in {file_path}: {num_tokens}")
