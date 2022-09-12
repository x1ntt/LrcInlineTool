from mutagen.mp3 import MP3

class Handle_mp3:
    def __init__(self, full_filename):
        self.audio = MP3(full_filename)
    
    def getInfo(self):
        # print (self.audio.pprint())
        
        if not self.audio:
            raise "文件读取失败"
        dict_keys = self.audio.keys()
        
        music_name = ""
        artist_name = ""
        alnum_name = ""
        lyrics = ""
        
        self.audio.pprint()
        
        if "TIT2" in dict_keys:
            music_name = self.audio["TIT2"]
        if "TALB" in dict_keys:
            alnum_name = self.audio["TALB"]
        if "TPE1" in dict_keys:
            artist_name = self.audio["TPE1"]
        if "USLT::eng" in dict_keys:
            lyrics = self.audio["USLT::eng"]
        # print (dict_keys)
        
        return (",".join(music_name.text), "/".join(artist_name), ",".join(alnum_name), lyrics)