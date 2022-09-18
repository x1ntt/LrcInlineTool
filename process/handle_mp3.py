from mutagen.mp3 import MP3

class Handle_mp3:
    def __init__(self, full_filename):
        self.audio = MP3(full_filename)
    
    def getInfo(self):
        # print (self.audio.pprint())
        
        if not self.audio:
            raise "文件读取失败"
        dict_keys = self.audio.keys()

        info_dict = dict()
        
        # self.audio.pprint()
        
        if "TIT2" in dict_keys:
            info_dict['music_name'] = ",".join(self.audio["TIT2"])
        if "TALB" in dict_keys:
            info_dict['alnum_name'] = ",".join(self.audio["TALB"])
        if "TPE1" in dict_keys:
            info_dict['artist_name'] = "/".join(self.audio["TPE1"])
        if "USLT::eng" in dict_keys:
            info_dict['lyrics'] = str(self.audio["USLT::eng"])
        # print (dict_keys)
        
        return info_dict