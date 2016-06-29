import os
import argparse
import fileparser
from collections import defaultdict

#TODO: keep db of changed names so you can reverse
#TODO: look for db and add to it so we can reverse all the way
#TODO: deal with case when two files the same name

def get_shows(array_files, season_number = None):
    shows = []
    for file in array_files:
        # parse every file in the directory
        show = fileparser.parse(file, season_number)
        shows.append(show)

    return shows

def find_duplicate_episode_numbers(shows):
    episodes = defaultdict(list)

    for show in shows:
        episodes[str(show.episode)].append(show)

    for key, value in episodes.items():
        if len(value) > 1:
            groups = defaultdict(list)

            for item in value:
                groups[item.group].append(item)

            for group, grp_shows in groups.items():
                if len(grp_shows) > 1:
                    vers=[]
                    for grp_show in grp_shows:
                        vers.append(grp_show.version)


                    max_val = max(vers)
                    max_index = vers.index(max_val)
                    grp_shows.pop(max_index)

                    for x in grp_shows:
                        x.mark_delete = True


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


            find_duplicate_episode_numbers(shows)


            if is_dry_run:
                for item in shows:
                    if not item.mark_delete:
                        print(" -> ".join([item.original, item.output()]))
                    else:
                        print(" -> ".join([item.original, "delete"]))
            else:
                for item in shows:
                    src_path = os.path.join(dirPath,item.original)

                    if not item.mark_delete:
                        dst_path = os.path.join(dirPath,item.output())
                        os.rename(src_path,dst_path)
                    else:
                        os.remove(src_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rename files to match plex standard.')
    parser.add_argument('path',
                        help='folder where media is stored')
    parser.add_argument('--dry-run', action='store_true',
                        help='don\'t rename anything; instead print results')

    args = parser.parse_args()


    if args.path:
        walk(args.path, args.dry_run)

