from sourcebase import SourceBase, SearchRequest, SearchResponse
from PyQt6.QtNetwork import QNetworkReply, QNetworkAccessManager, QNetworkRequest
from PyQt6.QtCore import QUrl
import json

class NeteaseSource(SourceBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def getResultList(self, search_request):
        url = f"http://music.163.com/api/search/get/web?s={search_request.song_name}&type=1&offset=0&total=true&limit={100}"
        self.req = QNetworkRequest(QUrl(url))
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.httpFinishedResultList)
        self.nam.get(self.req)
        
    def httpFinishedResultList(self, reply):
        bty = ""
        if reply.error() == QNetworkReply.NetworkError.NoError:
            bty = reply.readAll()
        print(json.loads(str(bty, 'utf-8')))
        
    def getLrc(self):
        pass
        
    def httpFinishedLrc(self, reply):
        pass