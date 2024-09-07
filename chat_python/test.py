import ollama

# Get the models dictionary
models_dict = ollama.list()

# Extract the list of models
models = models_dict.get('models', [])

# Iterate through the list and print the name of each model
for model in models:
    print(model.get("name", "No name key"))
