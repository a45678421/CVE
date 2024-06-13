def read_feedback_file(file_path, encoding):
    variables = {}
    with open(file_path, "r", encoding=encoding) as file:
        lines = file.readlines()
    for line in lines:
        if "=" in line:
            key, value = line.split("=", 1)
            variables[key.strip()] = value.strip().strip('"')
    return variables