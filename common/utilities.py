import os

def ensure_file_exists(path):
    if not os.path.isfile(path):
        print(f'Provided path "{path}" does not seem to be a file')
        exit(1)
    return path