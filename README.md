# LrcInlineTool



# 运行

目前还不是正式版，先不准备打包成`exe`

## 依赖

代码基于`PyQt6`，需要依赖以下库

+ `pip install PyQt6`

+ `pip install eyed3` (用于支持修改`mp3`文件标签)

  如果想要修改`.ui文件`则需要安装下面的工具，使用`designer.exe`编辑`ui文件`

+ `pip install PyQt6-tools`

## 重新生成界面代码

+ 运行`ui/gen_py.bat`即可
+ 

# API

## 网易云

参考：[网易云音乐的API - 知乎 (zhihu.com)](https://www.zhihu.com/column/p/21326015?utm_medium=social&utm_source=weibo)

### 搜索歌曲 (获取歌曲id)

`http://music.163.com/api/search/get/web?s=声&type=1&offset=0&total=true&limit=60`

### 获取歌词

`http://music.163.com/api/song/lyric?id=424057340&lv=-1&kv=-1&tv=-1`