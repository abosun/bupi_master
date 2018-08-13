# -*- coding: UTF-8 -*-
import glob
import os
import random

num_yc = len([path for path in glob.glob('data/xuelang/*/*') if not '正常' in path])
list_zc = glob.glob('data/xuelang/00正常/*')
random.shuffle(list_zc)
for path in list_zc[num_yc:]:
  os.remove(path)
