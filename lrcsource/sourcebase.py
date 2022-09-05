
# 传递搜索依据
class SearchRequest:
    def __init__(self, music_name, art_name):
        self.music_name = music_name
        self.art_name = art_name

# 传递搜索结果 所有源的实现统一使用这两个结构
class SearchResponseItem:
    def __init__(self, music_id, music_name, art_list):
        self.music_id = music_id
        self.music_name = music_name
        self.art = art_list
        
    def print(self):
        print (f"{self.music_id}, {self.music_name}", end="")
        print (self.art)

class SourceBase:
    def __init__(self):
        self.source_name = ""
        
    def SetCallbackObject(self, obj):
        self.callbackObject = obj
        
    def getResultList(self, search_reqeust):
        pass
        
    def sendRequest(self):
        pass