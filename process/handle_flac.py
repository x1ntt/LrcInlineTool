from mutagen.flac import FLAC
from time import gmtime, strftime

class Handle_flac:
    def __init__(self, full_filename):
        self.audio = FLAC(full_filename)
    
    def getInfo(self):
        if not self.audio:
            raise "文件读取失败"
        dict_keys = self.audio.keys()
        
        info_dict = dict()
        
        if "title" in dict_keys:
            info_dict['music_name'] = ",".join(self.audio["title"])
        if "album" in dict_keys:
            info_dict['alnum_name'] = ",".join(self.audio["album"])
        if "artist" in dict_keys:
            info_dict['artist_name'] = "/".join(self.audio["artist"])
        if "lyrics" in dict_keys:
            info_dict['lyrics'] = "".join(self.audio["lyrics"])
        
        try:
            info_dict['time_long'] = strftime("%H:%M:%S", gmtime(int(self.audio.info.length)))
        except Exception as e:
            print (e)
        
        return info_dict
        
    def setInfo(self, info_dict):
        if "music_name" in info_dict:
            self.audio["title"] = info_dict['music_name']
        if "artist_name" in info_dict:
            self.audio["artist"] = info_dict['artist_name']
        if "alnum_name" in info_dict:
            self.audio["album"] = info_dict['alnum_name']
        if "lyrics" in info_dict:
            self.audio["lyrics"] = info_dict['lyrics']
            
    def save(self):
        self.audio.save()