def load_text(filepath):
    with open(filepath, "r", encoding="UTF-8") as file:
        return file.read()
