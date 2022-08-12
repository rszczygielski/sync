import os
import shutil
import argparse

class Sync():
    def __init__(self, source: str, destination:str):
        self.source = source
        self.destination = destination

    def get_catalogs_and_files(self, path: str, all_files: list):
        catalogs_and_files = os.listdir(path)
        for elem in catalogs_and_files:
            all_files.append(os.path.join(path, elem))
            if os.path.isdir(os.path.join(path, elem)):
                self.get_catalogs_and_files(os.path.join(path, elem), all_files)

    def copy_to_destination(self):
        all_files = []
        self.get_catalogs_and_files(self.source, all_files)
        for file in all_files:
            extra_catalog = file.replace(self.source, "")
            destination_file_or_catalog = os.path.join(self.destination, extra_catalog)
            if os.path.isdir(file):
                if not os.path.isdir(destination_file_or_catalog):
                    os.mkdir(destination_file_or_catalog)
            else:
                if not os.path.isfile(destination_file_or_catalog):
                    shutil.copyfile(file, destination_file_or_catalog)

    def delete_from_destination(self):
        destination_files_paths = []
        source_files_paths = []
        self.get_catalogs_and_files(self.destination, destination_files_paths)
        self.get_catalogs_and_files(self.source, source_files_paths)
        source_files = []
        for file in source_files_paths:
            source_files.append(file.replace(self.source, ""))
        for file in destination_files_paths:
            extra_catalog_or_file = file.replace(self.destination, "")
            if extra_catalog_or_file not in source_files:
                if os.path.isfile(file):
                    os.remove(file) 
                else:
                    shutil.rmtree(file, ignore_errors=True)         

def run(source_path, destination_path):
    sync = Sync(source_path, destination_path)
    number = input("""
        Press 1 to copy all files to directory
        Press 2 delete all files diffrent from the source: """)
    if number == "1":
        sync.copy_to_destination()
    elif number == "2":
        sync.delete_from_destination()
    else:
        print("Please input correct data")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='program which can copy or delete files and catalogs which are in destination and dont in source')
    parser.add_argument('src', metavar='source', type=str,
                    help='source catalog')
    parser.add_argument('des', metavar='destinatin', type=str,
                    help='destination catalog')
    parser.add_argument('-d', "--syc-delete", action="store_true", default=False, dest="sync_delete", required=False,
                    help='delete files and catalogs which are in destination and dont in source')
    arg = parser.parse_args()

    source_dir = arg.src
    destination_dir = arg.des
    issync_delete = arg.sync_delete

    sync = Sync(source_dir, destination_dir)
    sync.copy_to_destination()
    if issync_delete:
        sync.delete_from_destination(source_dir, destination_dir)