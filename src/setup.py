import os
import logging
import datetime

def configure_logging(folder_path):
    """
    Configures logging for the application.
    
    Parameters:
    folder_path (str): Path to the folder where log files are stored. The function assumes that the folder exists.

    Returns:
    formatter (logging.Formatter): A configured formatter object for logging.
    """
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    logging.basicConfig(filename=os.path.join(folder_path, 'logfile.log'), filemode='w', level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    return formatter

def setup_game_environment():
    """
    Sets up the game environment, including cleaning log files.
    
    This function initializes the game environment by specifying the path to the folder where log files are stored.
    It then retrieves a list of all files in the specified folder and calls the `clear_log_files` function to remove any log files.
    Finally, it returns the path to the folder where log files are stored.

    Returns:
    folder_path (str): Path to the folder where log files are stored. The default value is "output", but it should be replaced with the actual folder path.
    """
    folder_path = "output"  # Replace with actual folder path
    files = os.listdir(folder_path)
    clear_log_files(folder_path, files)
    return folder_path

def clear_log_files(folder_path, files):
    """
    Clears old log files from the specified folder.
    
    This function iterates through the list of files in the given folder and checks if each file is a regular file.
    If a file is found, it is deleted using the os.remove() function and a message indicating the deletion is printed.

    Parameters:
    folder_path (str): Path to the folder where log files are stored. This parameter is expected to be a string representing the valid path to the folder.
    files (list): List of files to check for deletion. This parameter is expected to be a list of strings, where each string represents a file name.

    Returns:
    None. The function does not return any value.
    """
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted old log file: {file_name}")