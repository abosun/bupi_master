import os
import glob
import random
dirs = os.walk('./data/xuelang/').next()[1]
pathList = []
for dir in dirs:
  pathList.append(glob.glob('data/xuelang/'+dir+'/*jpg'))
size = min([len(ll) for ll in pathList])*2
print([len(ll) for ll in pathList])
for i,pathes in enumerate(pathList):
  if len(pathes)<=size:continue
  random.shuffle(pathes)
  for path in pathes[size:]:
    os.remove(path)
