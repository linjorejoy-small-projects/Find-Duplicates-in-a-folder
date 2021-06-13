
import hashlib
from pathlib import Path

hash_dict = {}

class FileInfo():
    def __init__(self, file_name:str="", file_hash:str="", file_location:str=""):
        self.file_name = file_name
        self.file_hash = file_hash
        self.file_location = file_location
        

def hash_file(filename) -> str:

   h = hashlib.sha1()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)
   return h.hexdigest()


def add_fileinfo_to_dict(file_hash: str, file_obj:FileInfo):
    pass

def get_files_from_parent_folder(parent_folder: str, file_extension: str = "*"):

    pathlist = Path(parent_folder).rglob(f"**/*.{file_extension}")
    for path in pathlist:
        path_in_str = str(path)
        yield path_in_str


def main():
    pass


if __name__ == "__main__":
    main()