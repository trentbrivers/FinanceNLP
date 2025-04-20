from preprocessing_inputs import process_input
import os

#fstring = r"E:\Data\NLP\Morningstar\0ab48845-e8dc-401d-b6ab-5f471f54112a.pdf"

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

path = r"E:\Data\NLP\Morningstar"

morningstar_files = list_files_in_directory(path)
#print(morningstar_files[0])

processed_text, label = process_input(os.path.join(path, morningstar_files[0]))

print(processed_text, "the label is ", label)