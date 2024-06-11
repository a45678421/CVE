import os
import shutil

def main():
    source_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    destination_folder = os.path.dirname(os.path.abspath(__file__))

    # Move feedback.txt
    source_file = os.path.join(source_folder, 'feedback.txt')
    destination_file = os.path.join(destination_folder, 'feedback.txt')

    if not os.path.exists(source_file):
        print(f'File not found: "{source_file}"')
    else:
        if os.path.exists(destination_file):
            os.remove(destination_file)
            print(f'Removed existing file: "{destination_file}"')
        
        shutil.move(source_file, destination_folder)
        print('Moved feedback.txt successfully.')

if __name__ == "__main__":
    main()
