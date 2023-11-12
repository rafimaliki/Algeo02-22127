import os

current_directory = os.getcwd()
print("Current working directory:", current_directory)


script_directory = os.path.dirname(os.path.abspath(__file__))
print("Script directory:", script_directory)
