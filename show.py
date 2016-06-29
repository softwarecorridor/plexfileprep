# desired output: Show Name - s##e## - random.ext

import re

class Show:
    name = ""
    group = ""
    episode = ""
    encoding = None
    extension = ""
    original = ""
    version = 1
    season = None
    mark_delete = False

    def __init__(self, path, filename, file_extension, group = None, episode_number = None, encoding = None, season = None, version = 1 ):

        self.original = path
        self.name = filename
        self.extension = file_extension
        self.group = group
        self.episode = episode_number
        self.encoding = encoding
        self.season = season
        self.version = version


    def output(self):
        array_to_convert = [self.name]
        if self.episode:
            array_to_convert.append(" - ")
            array_to_convert.append("s")
            if self.season:
                array_to_convert.append("%02d" % self.season)
            else:
                array_to_convert.append("01")
            array_to_convert.append("e")
            array_to_convert.append("%02d" % self.episode)
        if self.encoding or self.group:
            if self.encoding:
                array_to_convert.append("[{0}]".format(self.encoding))
            if self.group:
                array_to_convert.append("[{0}]".format(self.group))

        array_to_convert.append(self.extension)

        string_to_return = "".join(array_to_convert)

        if validate(string_to_return):
            return string_to_return

        return None

def validate(string):
    MAX_LENGTH = 250
    if len(string) >= MAX_LENGTH:
        return False
    special_char = "[\|\?\*\\\<>:\\/]"
    t = re.search(special_char,string)
    if t:
        return False

    return True
