# by @Nuked88 - https://github.com/Nuked88
import subprocess
import importlib.util
import sys
from packaging import version
import platform
import os
import json
import folder_paths


# From WAS
class color:
        END = '\33[0m'
        BOLD = '\33[1m'
        ITALIC = '\33[3m'
        UNDERLINE = '\33[4m'
        BLINK = '\33[5m'
        BLINK2 = '\33[6m'
        SELECTED = '\33[7m'

        BLACK = '\33[30m'
        RED = '\33[31m'
        GREEN = '\33[32m'
        YELLOW = '\33[33m'
        BLUE = '\33[34m'
        VIOLET = '\33[35m'
        BEIGE = '\33[36m'
        WHITE = '\33[37m'

        BLACKBG = '\33[40m'
        REDBG = '\33[41m'
        GREENBG = '\33[42m'
        YELLOWBG = '\33[43m'
        BLUEBG = '\33[44m'
        VIOLETBG = '\33[45m'
        BEIGEBG = '\33[46m'
        WHITEBG = '\33[47m'

        GREY = '\33[90m'
        LIGHTRED = '\33[91m'
        LIGHTGREEN = '\33[92m'
        LIGHTYELLOW = '\33[93m'
        LIGHTBLUE = '\33[94m'
        LIGHTVIOLET = '\33[95m'
        LIGHTBEIGE = '\33[96m'
        LIGHTWHITE = '\33[97m'

        GREYBG = '\33[100m'
        LIGHTREDBG = '\33[101m'
        LIGHTGREENBG = '\33[102m'
        LIGHTYELLOWBG = '\33[103m'
        LIGHTBLUEBG = '\33[104m'
        LIGHTVIOLETBG = '\33[105m'
        LIGHTBEIGEBG = '\33[106m'
        LIGHTWHITEBG = '\33[107m'


def read_config(param):
    #read config.json
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.json")
    #get python path from config.json
    # check if the file exists
    if not os.path.isfile(config_file):
        print("Config file not found:", config_file)
        return None
    try:
        with open(config_file, 'r') as file:
            config_data = json.load(file)

        return config_data[param]

    except:
        return None
    
#setting python path based on config.json
python_path = read_config("python")
if python_path == "default":
    python_path = sys.executable


def get_os():
    return platform.system().lower()

def check_and_install(package, import_name="", desired_version=None,extra="",reboot=False):
    if import_name == "":
        import_name = package
    try:
        library_module = importlib.import_module(import_name)
        current_version  = getattr(library_module, '__version__', None)
        if current_version :
            if current_version:
                print(f"Current version of {import_name}: {current_version}")
            if desired_version:
                if version.parse(current_version) < version.parse(desired_version):
                    print(f"Updating {import_name} to version {desired_version}...")
                    install_package(f"{package}=={desired_version}",extra)
                    print(f"{import_name} updated successfully to version {desired_version}")
                #else:
                #    print(f"{import_name} is already up-to-date with version {current_version}")

        else:
            print(f"Version of {import_name}: Version information not found")

        
    except ImportError:
        print(f"Installing {import_name}...")
        install_package(package,extra)
        if reboot:
            print(f"{color.RED}IMPORTANT: Please reboot the system!{color.END}")


def install_package(package, extra):
    args = [python_path, "-m", "pip", "install", "--no-cache-dir"]
    if extra:
        args.extend(extra.split(" "))
    args.append(package)
    subprocess.check_call(args)