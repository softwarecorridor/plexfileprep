import os
import argparse
import fileparser


#TODO: deal with v2 files (keep only the v2 one)
#TODO: keep db of changed names so you can reverse
#TODO: look for db and add to it so we can reverse all the way

def get_shows(array_files, season_number = None):
    shows = []
    for file in array_files:
        # parse every file in the directory
        show = fileparser.parse(file, season_number)
        shows.append(show)

    return shows

def is_season_folder(name):
    if len(name)<3 and name[0] == "s":
        try:
            int(name[1:])
            return True
        except ValueError:
            return False
    elif name.startswith("Season"):
        return True

    return False

def get_season_number(name):
    if len(name)< 3 and name[0] == "s":
        try:
            return int(name[1:])
        except ValueError:
            return False
    elif name.startswith("Season"):
        print(name)
        arr = name.split(" ")
        return int(arr[1])

    return False


def get_supported_extensions():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path,"supported_extensions.txt")

    with open(file_path,"r") as f_in:
        return f_in.read().splitlines()

def walk(path, is_dry_run):
    if os.path.isdir(path):
        for dirPath, subdirList, fileList in os.walk(path):
            dirName = os.path.basename(dirPath)
            fileList = [file for file in fileList if file[file.rfind("."):] in  get_supported_extensions()]

            shows = []
            if dirName == "extras":
                pass
            elif is_season_folder(dirName):
                num = get_season_number(dirName)
                shows = get_shows(fileList, num)
            else:
                shows = get_shows(fileList)

            if is_dry_run:
                for item in shows:
                    print(" -> ".join([item.original, item.output()]))
            else:
                for item in shows:
                    src_path = os.path.join(dirPath,item.original)
                    dst_path = os.path.join(dirPath,item.output())
                    os.rename(src_path,dst_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rename files to match plex standard.')
    parser.add_argument('path',
                        help='folder where media is stored')
    parser.add_argument('--dry-run', action='store_true',
                        help='don\'t rename anything; instead print results')

    args = parser.parse_args()


    if args.path:
        walk(args.path, args.dry_run)

