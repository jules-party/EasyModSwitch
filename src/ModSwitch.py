import os
import sys
import yaml
import shutil
import getopt

with open('../yaml/config.yaml', 'r') as file:
    data = yaml.safe_load(file)

folder_paths: list[str] = data.get('dirs')
folder_names: list[str] = [None] * len(folder_paths)

for i in range(len(folder_paths)):
    folder_names[i] = folder_paths[i].split(chr(92))[-1]

argv: list[str] = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hli:",["index="])
except getopt.GetoptError:
    print("option -i requires argument")
    exit(1)

class file_management:
    def __init__(self):
        self.mods_folder = '' 

    def set_mods_folder(self):

        if ((data['mods_folder'] == '') and (sys.platform == 'win32')):
            print('No mod folder found...\nUsing default location!\n')
            self.mods_folder = os.getenv('AppData')
            self.mods_folder = f"{self.mods_folder}\\.minecraft\\mods\\"
        elif ((data['mods_folder'] == '') and (sys.platform == 'linux')):
            print('No mod folder found...\nUsing default location!\n')
            self.mods_folder = os.getenv('HOME')
            self.mods_folder = f"{self.mods_folder}/.minecraft/"
        elif((data['mods_folder'] == '') and (sys.platform == 'darwin')):
            print('No mod folder found...\nUsing default location!\n')
            self.mods_folder = os.getenv('HOME')
            self.mods_folder = f"{self.mods_folder}/Library/Application Support/minecraft/mods/"
        else:
            print('Custom `mods` location found in config!\nUsing it...')
            self.mods_folder = data['mods_folder']
            print(self.mods_folder)

    def delete_mods_files(self):
        if self.mods_folder == '':
            raise ValueError('Variable `mods_folder` was not set!')

        for f in os.listdir(self.mods_folder):
            if not f.endswith('.jar'):
                continue
            os.remove(os.path.join(self.mods_folder, f))

    def copy_mod_files(self, mod_index="SETME"):
        if self.mods_folder == '':
            raise ValueError('Variable `mods_folder` was not set!')

        if mod_index == "SETME":
            for i in range(0, len(data.get('dirs'))):
                print(f"({i+1}) {folder_names[i]}")

            mod_index = input('~> ') 
        mod_index = int(mod_index) - 1

        self.delete_mods_files()
        folder = data.get('dirs')[mod_index]
        for file_name in os.listdir(folder):
            source = folder +'\\'+ file_name
            dest = self.mods_folder + file_name

            if os.path.isfile(source):
                shutil.copy(source, dest)
                print('Copied file with name: ', file_name)


if __name__ == "__main__":
    file_man = file_management()
    modf_index = "SETME"
    for opt, arg in opts:
        if opt == '-h':
            print('-i <index>\t| Set index on run')
            print('-l\t\t| List all folders in config.yaml')
            sys.exit()
        elif opt in ("-i", "--index"):
            modf_index = arg
        elif opt in ("-l", "--list-folders"):
            for i in range(0, len(data.get('dirs'))):
                print(f"({i+1}) {folder_names[i]}")
            sys.exit()

    file_man.set_mods_folder()
    file_man.copy_mod_files(modf_index)
