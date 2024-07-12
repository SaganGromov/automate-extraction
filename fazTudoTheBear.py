import os
import shutil
import subprocess
import re

directory_path = r"D:\testando\The.Bear.S03.1080p.WEB.H264-SUCCESSFULCRAB-PURO"

def extract_r00_with_winrar(file_path, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    # Full path to WinRAR.exe if it's not in your PATH
    winrar_path = r"C:\Program Files\WinRAR\WinRAR.exe"
    
    try:
        # Command to extract the .r00 file
        command = [winrar_path, 'x', file_path, output_directory]
        
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)
        
        # if result.returncode == 0:
        #     print(f"Extraction completed successfully to {output_directory}")
        # else:
        #     print(f"An error occurred: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_folders(directory):
    try:
        entries = os.listdir(directory)
        folders = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]
        return folders
    except FileNotFoundError:
        print(f"The directory {directory} was not found.")
        return []
    except PermissionError:
        print(f"Permission denied for directory {directory}.")
        return []

def list_files(directory):
    try:
        entries = os.listdir(directory)
        files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]
        return files
    except FileNotFoundError:
        print(f"The directory {directory} was not found.")
        return []
    except PermissionError:
        print(f"Permission denied for directory {directory}.")
        return []

def rev(l):
    return [i[::-1] if isinstance(i, str) else i for i in l]

def find_first_index(l):
    for index, string in enumerate(l):
        if isinstance(string, str) and string.startswith("00r."):
            return index
    return -1  # Return -1 if no element starts with "00r."

# Example usage
folders = list_folders(directory_path)

if folders:
    for i in range(len(folders)):  # Ensure valid range
        folder_path = os.path.join(directory_path, folders[i])
        files = list_files(folder_path)
        
        if files:
            ind = find_first_index(rev(files))
            if ind != -1:
                file_path = os.path.join(folder_path, files[ind])
                extract_r00_with_winrar(file_path, folder_path)
            else:
                print(f"No file ending with '.r00' found in folder {folders[i]}")
        else:
            print(f"No files found in folder {folders[i]}")
else:
    print("No folders found.")

print("Extraction of all files has been completed.")

def delete_non_mkv_files_and_subfolders(directory):
    try:
        mkv_files = []
        for root, dirs, files in os.walk(directory):
            for name in files:
                file_path = os.path.join(root, name)
                if name.endswith(".mkv"):
                    mkv_files.append(file_path)
                else:
                    os.remove(file_path)
                    # print(f"Deleted file: {file_path}")
            for name in dirs:
                dir_path = os.path.join(root, name)
                # Delete subfolders recursively
                for root_sub, dirs_sub, files_sub in os.walk(dir_path, topdown=False):
                    for dir_sub in dirs_sub:
                        dir_sub_path = os.path.join(root_sub, dir_sub)
                        os.rmdir(dir_sub_path)
                        # print(f"Deleted subfolder: {dir_sub_path}")
        
        # Move all .mkv files to directory A
        for mkv_file in mkv_files:
            shutil.move(mkv_file, os.path.join(directory, os.path.basename(mkv_file)))
            # print(f"Moved .mkv file: {mkv_file}")
        
        # Delete all subfolders in directory A
        for root, dirs, files in os.walk(directory, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)
                # print(f"Deleted subfolder: {dir_path}")
        
        # print("Deletion and movement completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

delete_non_mkv_files_and_subfolders(directory_path)

def rename_files_in_folder(folder):
    try:
        for filename in os.listdir(folder):
            # Split filename and extension
            base_name, extension = os.path.splitext(filename)
            
            # Define a generic pattern for TV series episode naming
            pattern = r"([a-zA-Z\s.]+)\.s(\d{2})e(\d{2})"
            
            # Try to match the pattern
            match = re.match(pattern, base_name, flags=re.IGNORECASE)
            if match:
                series_name = match.group(1).replace(".", " ").title()  # Capitalize series name
                season = match.group(2).lstrip("0")
                episode = match.group(3).lstrip("0")
                
                new_base_name = f"{series_name}, Season {season}, Episode {episode}"
                new_filename = f"{new_base_name}{extension}"
                
                # Rename file
                os.rename(os.path.join(folder, filename), os.path.join(folder, new_filename))
                # print(f"Renamed {filename} to {new_filename}")
            else:
                print(f"Skipped {filename} (no matching pattern)")
        
        # print("Renaming completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
folder_path = directory_path
rename_files_in_folder(folder_path)
print("\nAnd now the files have also been renamed. Enjoy!")