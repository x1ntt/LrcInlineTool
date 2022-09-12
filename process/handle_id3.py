from mutagen.id3 import ID3

class Handle_id3:
    def __init__(self, full_name):
        self.id3 = ID3(full_name)
    
    def getInfo(self):
        print(self.id3)