from mutagen.flac import FLAC

class Handle_flac:
    def __init__(self, full_filename):
        self.audio = FLAC(full_filename)
    
    def getInfo(self):
        if not self.audio:
            raise "文件读取失败"
        dict_keys = self.audio.keys()
        
        # self.audio.pprint()
        
        info_dict = dict()
        
        if "title" in dict_keys:
            info_dict['music_name'] = ",".join(self.audio["title"])
        if "album" in dict_keys:
            info_dict['alnum_name'] = ",".join(self.audio["album"])
        if "artist" in dict_keys:
            info_dict['artist_name'] = "/".join(self.audio["artist"])
        if "lyrics" in dict_keys:
            info_dict['lyrics'] = self.audio["lyrics"]
        
        return info_dict