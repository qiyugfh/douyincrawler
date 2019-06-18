# coding: utf-8

import os
import sys


print('****************************************************************************')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# -q 屏蔽 mitmdump 默认的控制台日志，只显示自己脚本中的
# -s 入口脚本文件
os.system("mitmdump -p 8080 -q -s main.py")

# os.system('mitmweb -s main.py')

print('****************************************************************************')