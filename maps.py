from import_file import *

__all__ = ["get_maps"]


class Map1(Entities):

    def __init__(self):
        super(Map1, self).__init__(8, 8)
        self.draw_env("""SSSSSSSS
SSSGGSSS
SGGGGGGS
SGCCGGGS
SSSGGCCS
SSSGGCCS
SSSCCCCS
SSSSSSSS""")
        self.start_from = (4, 4)


class Map2(Entities):

    def __init__(self):
        super(Map2, self).__init__(8, 8)
        self.draw_env("""SSSSSSSS
SDSGGSCS
SGGGGGGS
SGCCGGGS
SGGGGCCS
SGCSGCCS
SCCCCCCS
SSSSSSSS""")
        self.start_from = (2, 4)


class Map3(Entities):

    def __init__(self):
        super(Map3, self).__init__(8, 8)
        self.draw_env("""SSSSSSSS
SSSGGSSS
SGGGGGGS
SGCGGGGS
SSSGGCCS
SSSGGCCS
SSSCCCCS
SSSSSSSS""")
        self.start_from = (4, 4)

class Map4(Entities):

    def __init__(self):
        super(Map4, self).__init__(15, 15)
        self.draw_env("""SSSSSSSSSSSSSSS
SGGGGSSSSGGGGGS
SGGGGGGGGGGGGGS
SGGGGSSSSGGGGGS
SGGGGGGGGGGGGGS
SGGGSSSSSGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGSSSSGGGGGS
SGGGGGGGGGGGGGS
SGGGCCCCCGGGGGS
SGGGGGGGGGGGGGS
SGGGCCCCSGGGGGS
SSSSSSSSSSSSSSS""")
        self.start_from = (1, 13)


class Map5(Entities):

    def __init__(self):
        super(Map5, self).__init__(15, 15)
        self.draw_env("""SSSSSSSSSSSSSSS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGCCCGGGGS
SGGGGGGGSSGGGGS
SGGGGGGGGGGGGGS
SGGGGSSSGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGSGGGSGGGGGGGS
SGGGGGSSGGGGGGS
SGGGGSSSGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SSSSSSSSSSSSSSS""")
        self.start_from = (1, 13)


class Map6(Entities):

    def __init__(self):
        super(Map6, self).__init__(15, 15)
        self.draw_env("""SSSSSSSSSSSSSSS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SGGGGGGGGGGGGGS
SSSSSSSSSSSSSSS""")
        self.start_from = (1, 13)



def get_maps():
    return {"Map1": Map1,
            "Map2": Map2,
            "Map3": Map3,
            "Map4": Map4,
            "Map5": Map5,
            "Map6": Map6
            }
