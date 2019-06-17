# coding: utf-8

import os
import sys



sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.system("mitmdump -q -s main.py")
