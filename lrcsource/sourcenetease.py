from lrcsource.sourcebase import SourceBase, SearchRequest, SearchResponseItem

from PyQt6.QtNetwork import QNetworkReply, QNetworkAccessManager, QNetworkRequest
from PyQt6.QtCore import QUrl
import json

class NeteaseSource(SourceBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_name = "棒棒的网易云"
        
    def getResultList(self, search_request):
        self.music_name = search_request.music_name
        self.art_name = search_request.art_name
        
        url = f"http://music.163.com/api/search/get/web?s={self.music_name}&type=1&offset=0&total=true&limit={50}"
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
            res_list.append(SearchResponseItem(song["id"], song["name"], art_list))
        return res_list
        
    def httpFinishedResultList(self, reply):
        bty = ""
        error_str = ""
        res_list = []
        if reply.error() == QNetworkReply.NetworkError.NoError:
            bty = reply.readAll()
            json_str = str(bty, 'utf-8')
            # print(json_str)
            # res_list = self.parseJson(json_str)
            try:
                res_list = self.parseJson(json_str)
            except Exception as e:
                error_str = str(e)
        else:
            print(f"错误 {reply.error()}")
            error_str = f"错误 {reply.error()}"
        # print (res_list)
        self.callbackObject.resultList(error_str, res_list)
        
    def getLrc(self):
        pass
        
    def httpFinishedLrc(self, reply):
        pass