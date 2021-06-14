
import hashlib
import os
import json
import datetime
from pathlib import Path
from typing import Dict, List

hash_dict:Dict[str, List] = {}
LOGS = []
checked_folders = []

FILE_TYPES = ["JPG", "PNG", "GIF", "WEBP", "TIFF", "PSD", "RAW", "BMP", "HEIF", "INDD", "JPEG 2000"]


        
class FolderInfo():
    def __init__(self, folder_name:str = ""):
        self.folder_name = folder_name
        self.timestamp = str(datetime.datetime.now()).replace(":", "-")
        self.file_count = {}
        self.folder_count = 0
        self.checked_folders = []
        self.file_info_dict:Dict[str, List[str]] = dict()
    
    
    def add_fileinfo_to_dict(self, file_hash: str, file_name:str):
        
        if file_hash in self.file_info_dict.keys():
            self.file_info_dict[file_hash].append(file_name)
        else:
            self.file_info_dict[file_hash] = [file_name]
            
    def get_files_from_parent_folder(self, parent_folder: str, file_extension: str = "*"):

        pathlist = Path(parent_folder).rglob(f"**/*.{file_extension}")
        for path in pathlist:
            path_in_str = str(path)
            yield path_in_str



def hash_file(filename) -> str:

   h = hashlib.sha1()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)
   return h.hexdigest()
   

def write_to_file(file_name:str, data:str, write_type:str="w"):
    with open(file_name, write_type) as file_stream:
        file_stream.write(data)
    

def to_dict(obj) -> str:
    return json.dumps(obj, default=lambda o: o.__dict__, indent=2)


def main():

    parent_folder = input("What is the Parent Folder : ")
    global LOGS

    folder_info_obj = FolderInfo(parent_folder)
    output_folder_timestamp = folder_info_obj.timestamp
    for extenstion in FILE_TYPES:
        extenstion = extenstion.lower()
        folder_info_obj.file_count[extenstion] = 0
        print(f"{extenstion=}")
        for file_name in folder_info_obj.get_files_from_parent_folder(parent_folder, file_extension=extenstion):
            file_hash = "File Not Readable"
            folder_info_obj.file_count[extenstion] += 1
            try:
                file_hash = hash_file(file_name)
            except PermissionError:
                LOGS.append(f"PermissionError for file {file_name}")
            except Exception as e:
                LOGS.append(f"{e} for file {file_name}")

            full_file_name = os.path.abspath(file_name)
            folder_name = os.path.dirname(full_file_name)

            if folder_name not in folder_info_obj.checked_folders:
                print(f"Started with {folder_name}")
                folder_info_obj.folder_count += 1
                folder_info_obj.checked_folders.append(folder_name)

            folder_info_obj.add_fileinfo_to_dict(file_hash, full_file_name)

    outputs_folder_path = os.path.join(os.getcwd(), "outputs")

    if not os.path.exists(outputs_folder_path):
        os.mkdir(outputs_folder_path)

    os.mkdir(os.path.join(outputs_folder_path, output_folder_timestamp))

    write_to_file(f"outputs/{output_folder_timestamp}/outputs.json", to_dict(folder_info_obj))

    LOGS = [*LOGS, "\n\nCheckd Folders", *folder_info_obj.checked_folders]
    
    write_to_file(f"outputs/{output_folder_timestamp}/LOGS.txt", "\n".join(LOGS),write_type="w")


if __name__ == "__main__":
    import time
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'finished in {elapsed_time:.05f}s')