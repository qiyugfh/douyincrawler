# coding: utf-8

import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


os.system("mitmdump -q -s appium_douyin.py")
