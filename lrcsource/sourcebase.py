
# 传递搜索依据
class SearchRequest:
    def __init__(self, song_name):
        self.song_name = song_name

# 传递搜索结果 所有源的实现统一使用这两个结构
class SearchResponse:
    def __init__(self, result_list):
        self.result_list = result_list

class SourceBase:
    def __init__(self):
        self.source_name = ""
        
    def SetMainWindow(main_window):
        self.main_window = main_window
        
    def getResultList(self, search_reqeust):
        pass
        
    def sendRequest(self):
        pass