from mutagen.flac import FLAC

class Handle_flac:
    def __init__(self, full_filename):
        self.audio = FLAC(full_filename)
    
    def getInfo(self):
        if not self.audio:
            raise "文件读取失败"
        dict_keys = self.audio.keys()
        
        music_name = ""
        artist_name = ""
        alnum_name = ""
        lyrics = ""
        
        self.audio.pprint()
        
        if "title" in dict_keys:
            music_name = self.audio["title"]
        if "album" in dict_keys:
            alnum_name = self.audio["album"]
        if "artist" in dict_keys:
            artist_name = self.audio["artist"]
        if "lyrics" in dict_keys:
            lyrics = self.audio["lyrics"]
        
        return (",".join(music_name), "/".join(artist_name), ",".join(alnum_name), lyrics)