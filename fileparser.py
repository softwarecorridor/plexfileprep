import re
import os
from show import Show

def is_crc(string):
    ''' crc is in hex so just check for that
    :param string:
    :return: boolean
    '''
    try:
        int(string, 16)
    except ValueError:
        return(False)

    return True

def is_group_name(string):
    #naive way - group names rarely contain more than a couple of numbers
    MAX_DIGIT = 2
    t = re.findall("\d", string)
    if (len(t)) > MAX_DIGIT:
        return False

    return True

def get_detail_list():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path,"details.txt")

    with open(file_path,"r") as f_in:
        return f_in.read().splitlines()

def is_details(string):
    details = get_detail_list()
    arr = string.split(" ")
    results = []
    for item in arr:
        for detail in details:
            if item.startswith(detail):
                results.append(True)

    if False in results:
        return False

    return True

def get_non_bracket_text(string):
    result = []
    non_brackets = [s.split(']')[-1] for s in string.split('[')]

    if non_brackets:
        for item in non_brackets:
            if item:
                result.append(item.strip())
    else:
        result.append(string)
    return result


def get_extension(string):
    index = string.rfind('.')
    extension = string[index:]
    return extension


def get_show_name_and_episode(string):
    name_array = string.split('-')

    possible_episode_num = name_array[-1]
    non_version = possible_episode_num.split("v")[0]

    try:
        ep = int(non_version)
        return ["".join(name_array[:-1]).strip(), ep]
    except ValueError:
        return ["".join(name_array), None]


def break_down_filename(string):
    new_string = string[:string.rfind(".")]
    non_brackets = get_non_bracket_text(new_string)
    brackets = re.findall("\[([^[\]]*)\]", new_string)
    return list(filter(None, non_brackets + brackets))

def get_resolution(string):
    acceptable_res = ["1080p", "1080i", "720p", "720i", "576p", "480p", "368p", "360p"]

    sections = string.split(" ")
    for item in sections:
        if item in acceptable_res:
            return item

    return None


def get_prepared_string(string):
    replace_underscores = string.replace("_", " ")
    replace_open_paren = replace_underscores.replace("(","[")
    replace_close_paren = replace_open_paren.replace(")", "]")


    return replace_close_paren

def get_version(string):
    #regex
    match = re.search("(?<=v)\d*", string)
    if match.group(0):
        return match.group(0)
    else:
        return '1'

def parse(string, season = None):

    prepared_string = get_prepared_string(string)
    extension = get_extension(prepared_string)

    sections = break_down_filename(prepared_string)
    name, episode = get_show_name_and_episode(sections[0])

    group = ""
    encoding = ""
    version = get_version(prepared_string)

    for item in sections[1:]:
        if is_crc(item):
            pass
        elif is_group_name(item):
            group = item
        elif is_details(item):
            encoding = get_resolution(item)

    if episode:
        if season:
            return Show(string, name,extension,group,episode,encoding, season, version=version)
        else:
            return Show(string, name,extension,group,episode,encoding, 1, version=version)
    else:
        return Show(string, name,extension,group,encoding=encoding, version=version)


    
# test = "[ILA]_Aim_for_the_Ace!_-_05.avi"
# test = "Senki zesshou symphyogear.mkv"
# test = "Senki zesshou symphyogear - [v2][BD 720p AAC]  [EB80A8D7].mkv"
# #
# s = parse(test)
#
# print(s.version)