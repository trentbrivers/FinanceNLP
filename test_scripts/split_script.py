import random
import os
import shutil

def list_files_in_directory(folder_path):
  """Lists all files in the specified directory.

  Args:
    folder_path: The path to the directory.

  Returns:
    A list of strings, where each string is the name of a file in the directory.
    Returns an empty list if the directory does not exist or is empty.
  """
  try:
    files = os.listdir(folder_path)
    return [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
  except FileNotFoundError:
    return []

def move_file(file_name, source, destination):
	file_path = os.path.join(source, file_name)
	try:
	    shutil.move(file_path, destination)
	    print(f"File moved successfully from {source_path} to {destination}")
	except FileNotFoundError:
	    print(f"Error: File not found at {source_path}")
	except FileExistsError:
	    print(f"Error: File already exists at {destination}")
	except Exception as e:
	    print(f"An error occurred: {e}")

source_path = r"E:\Data\NLP\Morningstar"
destination_path = r"E:\Data\NLP\Morningstar\Test"

all_files = list_files_in_directory(source_path)
dest_files = list_files_in_directory(destination_path)

if len(dest_files) < 90:
	sample_needed = 90 - len(dest_files)

split_selection = random.sample(all_files, sample_needed)
for selected_file in split_selection:
	move_file(selected_file, source_path, destination_path)