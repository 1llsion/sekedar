# Open File untuk mengambil list

def open_file(file_name):
    with open(file_name, 'r') as file:
        target = file.read()
    return target

# Save File 

def save(file_name, content):
    with open(f"result/{file_name}.txt", 'a') as file:
        file.write(content + "\n")