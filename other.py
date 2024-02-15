import os

def console_clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def directory_clear(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        except:
            pass