from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, USLT
from time import gmtime, strftime

class Handle_mp3:
    def __init__(self, full_filename):
        self.audio = ID3(full_filename)
        self.audio2 = MP3(full_filename)
    
    def getInfo(self):
        if not self.audio:
            raise "文件读取失败"
        dict_keys = self.audio.keys()

        info_dict = dict()

        if "TIT2" in dict_keys:
            info_dict['music_name'] = ",".join(self.audio["TIT2"])
        if "TALB" in dict_keys:
            info_dict['alnum_name'] = ",".join(self.audio["TALB"])
        if "TPE1" in dict_keys:
            info_dict['artist_name'] = "/".join(self.audio["TPE1"])
        
        if len(self.audio.getall("USLT")) > 0:
            info_dict['lyrics'] = self.audio.getall("USLT")[0].text
        try:
            info_dict['time_long'] = strftime("%H:%M:%S", gmtime(int(self.audio2.info.length)))
        except Exception as e:
            print (e)
        
        return info_dict
    
    def setInfo(self, info_dict):
        if "music_name" in info_dict:
            self.audio["TIT2"] = TIT2(encoding=3, text=info_dict['music_name'])
        if "artist_name" in info_dict:
            self.audio["TPE1"] = TPE1(encoding=3, text=info_dict['artist_name'])
        if "alnum_name" in info_dict:
            self.audio["TALB"] = TALB(encoding=3, text=info_dict['alnum_name'])
        if "lyrics" in info_dict:
            self.audio.setall("USLT", [USLT(encoding=3, lang='eng', text=info_dict['lyrics'])])
            
    def save(self):
        self.audio.save()