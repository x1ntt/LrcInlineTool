# 翻译歌词加上最小单位时间，用于兼容支持多行显示的播放器，实现双语歌词 （目前没有正确实现）
# 思路来自 https://github.com/jitwxs/163MusicLyrics/issues/171 感谢 @daoxi

import re

def sub_min_unit_from_lrc_line(lrc_line):
    if len(lrc_line) == 0:
        return lrc_line
    try:
        # 在第一个闭合括号处分割行，以获取时间
        time_str = lrc_line.split(']')[0][1:]
        # 将时间字符串分割为分钟、秒和毫秒
        minutes, seconds_milliseconds = time_str.split(':')
        seconds, milliseconds = seconds_milliseconds.split('.')
        # 将所有内容转换为整数
        minutes = int(minutes)
        seconds = int(seconds)
        milliseconds = int(milliseconds)
    except:
        return lrc_line
    # 从毫秒中减去最小时间单位（1毫秒）
    milliseconds -= 1
    # 如果毫秒为负数，则从秒中减去1，并将100添加到毫秒中
    if milliseconds < 0:
        seconds -= 1
        milliseconds += 100
    # 如果秒为负数，则从分钟中减去1，并将60添加到秒中
    if seconds < 0:
        minutes -= 1
        seconds += 60
    # 如果分钟为负数，则将其设置为0，并将秒和毫秒设置为0
    if minutes < 0:
        minutes = 0
        seconds = 0
        milliseconds = 0
    # 格式化调整后的时间字符串，并将其与行的其余部分返回
    adjusted_time_str = f"[{minutes:02d}:{seconds:02d}.{milliseconds:02d}]"
    return adjusted_time_str + lrc_line.split(']')[1]

def get_time_from_lrc_line(lrc_line):
    result = ""
    res = re.findall("^\[.*\]", lrc_line)
    if len(res):
        result = res[0]
    return result
    
def replace_time(lrc_line, lrc_time):
    # 通过']'分割lrc_line，将时间和歌词分开
    split_line = lrc_line.split(']')
    # 用lrc_time中的新时间替换原时间
    split_line[0] = lrc_time
    # 用']'将分割后的split_line重新连接起来并返回结果
    return ''.join(split_line)

def match_translate_line(tlyric_list, lrc_time):
    for line in tlyric_list:
        if lrc_time in line:
            return line
    return ""