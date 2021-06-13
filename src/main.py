
import hashlib
import os
import json
import datetime
from pathlib import Path
from typing import Dict, List

hash_dict:Dict[str, List] = {}
LOGS = []

FILE_TYPES = ["JPG", "PNG", "GIF", "WEBP", "TIFF", "PSD", "RAW", "BMP", "HEIF", "INDD", "JPEG 2000"]
"JPG", "PNG", "GIF", "WEBP", "TIFF", "PSD", "RAW", "BMP", "HEIF", "INDD", "JPEG 2000"


class FileInfo():
    def __init__(self, file_name:str="", file_hash:str="", file_location:str=None):
        _, self.file_location = self.get_file_info(file_name)
    
    def get_file_info(self, full_file_path):
        abs_path = os.path.abspath(full_file_path)
        file_name = os.path.basename(full_file_path)
        return file_name, os.path.dirname(abs_path)
        
class FolderInfo():
    def __init__(self, folder_name:str = ""):
        self.folder_name = folder_name
        self.timestamp = str(datetime.datetime.now()).replace(":", "-")
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
   

def write_to_file(file_name:str, data:str):
    with open(file_name, "w") as file_stream:
        file_stream.write(data)
    

def to_dict(obj) -> str:
    return json.dumps(obj, default=lambda o: o.__dict__, indent=2)


def main():

    parent_folder = input("What is the Parent Folder : ")
    global LOGS

    folder_info_obj = FolderInfo(parent_folder)
    output_folder = folder_info_obj.timestamp

    for file_name in folder_info_obj.get_files_from_parent_folder(parent_folder):
        file_hash = "File Not Readable"
        try:
            file_hash = hash_file(file_name)
        except PermissionError:
            LOGS.append(f"PermissionError for file {file_name}")
        except Exception as e:
            LOGS.append(f"{e} for file {file_name}")

        full_file_name = os.path.abspath(file_name)
        folder_info_obj.add_fileinfo_to_dict(file_hash, full_file_name)

    os.mkdir(f"outputs/{output_folder}")

    write_to_file(f"outputs/{output_folder}/outputs.json", to_dict(folder_info_obj))

    if LOGS:
        write_to_file(f"outputs/{output_folder}/LOGS.txt", "\n".join(LOGS))


if __name__ == "__main__":
    main()