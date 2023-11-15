import re

def remove_comments(file_path):
    with open(file_path, 'r') as file:
        c_code = file.read()

    # Remove /* ... */ comments
    c_code = re.sub(r'/\*.*?\*/', '', c_code, flags=re.DOTALL)

    # Remove // ... comments
    c_code = re.sub(r'//.*', '', c_code)

    # Remove empty lines
    c_code = re.sub(r'^\s*[\r\n]', '', c_code, flags=re.MULTILINE)

    new_file_path = f'./{file_path.split("/")[1].split(".")[0]}_rc.c'
    with open(new_file_path, 'w') as file:
        file.write(c_code)

    return new_file_path
