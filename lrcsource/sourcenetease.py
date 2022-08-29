from sourcebase import SourceBase, SearchRequest, SearchResponse
from PyQt6.QtNetwork import QNetworkReply, QNetworkAccessManager, QNetworkRequest
from PyQt6.QtCore import QUrl

class NeteaseSource(SourceBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def handleRequest(self, search_request):
        url = f"http://music.163.com/api/search/get/web?s={search_request.song_name}&type=1&offset=0&total=true&limit={10}"
        self.req = QNetworkRequest(QUrl(url))
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.httpFinished)
        self.nam.get(self.req)
        
    def httpFinished(self, reply):
        bty = reply.readAll()
        print(str(bty, 'utf-8'))
        
        #er = reply.error()
        #print (er)
        #if er == QNetworkReply.NoError:
        #    bty = reply.readAll()
        #    print(str(bty, 'utf-8'))
        #else:
        #    print (f"错误: {er}")
        #    print (reply.errorString())