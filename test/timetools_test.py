import sys
sys.path.append('../utils')

from timetools import sub_min_unit_from_lrc_line

test_list = []

test_list.append('[00:05.99]这是一行lrc歌词')
test_list.append('[99:99.99]这是一行lrc歌词')
test_list.append('[00:00.00]这是一行lrc歌词')
test_list.append('[00:3.0]这是一行lrc歌词')
test_list.append('[00:50.22]这是一行lrc歌词')

for line in test_list:
    print(sub_min_unit_from_lrc_line(line))

