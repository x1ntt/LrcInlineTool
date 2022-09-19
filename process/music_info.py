# 暂不使用
class MusicInfo:
    def __init__():
        self.music_name = ""
        self.artist_name = ""
        self.alnum_name = ""
        self.lyrics = ""
    
    def setMusicName(self, name):
        self.music_name = name
    def setArtistName(self, name):
        self.artist_name = name
    def setAlnumName(self, name):
        self.alnum_name = name
    def setLyrics(self, lyrics):
        self.lyrics = lyrics
        
    def getMusicName(self):
        return self.music_name
    def getArtistName(self):
        return self.artist_name
    def getAlnumName(self):
        return self.alnum_name
    def getLyrics(self):
        return self.lyrics
