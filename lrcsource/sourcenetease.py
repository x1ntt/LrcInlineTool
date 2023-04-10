from lrcsource.sourcebase import SourceBase, SearchRequest, SearchResponseItem

from urllib.parse import quote_plus 
from PyQt5.QtNetwork import QNetworkReply, QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl
import json

class NeteaseSource(SourceBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_name = "棒棒的网易云"
        
    def getResultList(self, search_request):
        self.music_name = search_request.music_name
        self.art_name = search_request.art_name
        
        url = f"http://music.163.com/api/search/get/web?s={quote_plus(str(self.music_name + self.art_name))}&type=1&offset=0&total=true&limit={100}"
        print (url)
        self.req = QNetworkRequest(QUrl(url))
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.httpFinishedResultList)
        self.nam.get(self.req)
        
    def parseJson(self, json_str):
        if len(json_str) == 0:
            raise "返回结果为空"
        res = json.loads(json_str)
        # print (res)
        if res["code"] != 200:
            raise f"api返回的状态码不正确 {res['code']}"
        songs = res["result"]["songs"]
        res_list = []
        for song in songs:
            art_list = []
            for art in song["artists"]:
                art_list.append(art["name"])
            res_list.append(SearchResponseItem(song["id"], song["name"], song["album"]["name"], art_list))
        return res_list
        
    def httpFinishedResultList(self, reply):
        bty = ""
        error_str = ""
        res_list = []
        if reply.error() == QNetworkReply.NetworkError.NoError:
            bty = reply.readAll()
            json_str = str(bty, 'utf-8')
            try:
                res_list = self.parseJson(json_str)
            except Exception as e:
                error_str = str(e)
        else:
            print(f"错误 {reply.error()}")
            error_str = f"错误 {reply.error()}"
        self.callbackObject.resultList(error_str, res_list)
        
    def getLrc(self, music_id, reason):
        if len(music_id) == 0:
            return
        url = f"http://music.163.com/api/song/lyric?id={str(music_id)}&lv=-1&kv=-1&tv=-1"
        self.req2 = QNetworkRequest(QUrl(url))
        self.nam2 = QNetworkAccessManager()
        self.nam2.finished.connect(self.httpFinishedLrc)
        self.nam2.get(self.req2)
        self.reason2 = reason
        self.music_id2 = music_id
        
    def parseLrcJson(self, json_str):
        if len(json_str) == 0:
            raise "返回结果为空"
        res = json.loads(json_str)
        if res["code"] != 200:
            raise f"api返回的状态码不正确 {res['code']}"
        lrcs = {}   # 保存所有的歌词
        try:
            lrcs["lyric"] = res["lrc"]["lyric"]             # 歌词
            lrcs["tlyric"] = res["tlyric"]["lyric"]         # 歌词翻译
        except:
            pass    # 纯音乐没有tlyric
        return lrcs
        
    def httpFinishedLrc(self, reply):
        bty = ""
        error_str = ""
        json_str = ""
        res = {}
        if reply.error() == QNetworkReply.NetworkError.NoError:
            bty = reply.readAll()
            json_str = str(bty, 'utf-8')
            try:
                res = self.parseLrcJson(json_str)
            except Exception as e:
                error_str = str(e)
        else:
            error_str = f"错误 {reply.error()}"
        self.callbackObject.lrcResult(error_str, res, self.music_id2, self.reason2)