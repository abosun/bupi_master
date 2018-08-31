# -*- coding: UTF-8 -*- 
from object_detection.utils import dataset_util
from lxml import etree
import glob
import cv2 as cv
import os
import numpy as np
DIR_img = 'data/xuelang*/*/'
DIR_xml = 'data/xuelang*/*/'
DIR_tag = 'data/crop/'
crop_size = 640
def boxGen(size, stride):
    box_list = []
    for i in range((1920-size)//stride+1):
      for j in range((2560-size)//stride+1 ):
        box_list.append([i*stride, i*stride+size, j*stride, j*stride+size])
    return box_list
boxe43 = boxGen(640, 80)
#(xi,xa,yi,ya)
c = 0
c2 = 0
DIR_data = 'data/xuelang'
DIR_zc = 'data/xuelang/zc'
DIR_yc = 'data/xuelang/yc'
lll = []
mem = []
def getLabel(path):
	return os.path.basename(os.path.dirname(path))
def iou(box1, boxa):
	ll = (boxa[1]-boxa[0])//3
	box2 = [boxa[0]+ll,boxa[1]-ll,boxa[2]+ll,boxa[3]-ll]
	if max(box1[0],box2[0])>min(box1[1],box2[1]):return False
	if max(box1[2],box2[2])>min(box1[3],box2[3]):return False
	return True

def listIou(box_list, boxa):
	if len(box_list)==0:return False
	for box in box_list:
		if iou(box,boxa):
			return True
	return False

def crop(xi,xa,yi,ya,X,Y):
	w = xa-xi
	h = ya-yi
	if w<crop_size :
		xi = max(0, xi-int((crop_size-w)/2))
		xa = min(X, xi+int((crop_size-w)/2))
		if xa-xi<crop_size:
			xi = max(0,  xi - (crop_size-xa+xi))
			xa = min(X,  xa + (crop_size-xa+xi))
	if h<crop_size :
		yi = max(0, yi-int((crop_size-w)/2))
		ya = min(Y, yi+int((crop_size-w)/2))
		if ya-yi<crop_size:
			yi = max(0,  yi - (crop_size-ya+yi))
			ya = min(Y,  ya + (crop_size-ya+yi))
	return (xi,xa,yi,ya)
def get_black(box_list, img):
	w,h,_ = img.shape
	res = img.copy()
	res *= 0
	for box in box_list:
		res[box[0]:box[1], box[2]:box[3]] = 1
	return np.multiply(res,img)
	for i in range(w):
		for j in range(h):
			res[i,j] = img[i,j]*res[i,j]
	return res
def fun(path, imgpath, labelSet):
	img = cv.imread(imgpath)
	line = open(path).read()
	xml = etree.fromstring(line)
	data = dataset_util.recursive_parse_xml_to_dict(xml)['annotation']
	image_list = []
	box_list = []
	for obj in data['object']:
		box_list.append([int(obj['bndbox']['ymin']),int(obj['bndbox']['ymax']),int(obj['bndbox']['xmin']),int(obj['bndbox']['xmax'])])
		box = box_list[-1]
		mem.append(min(box[1]-box[0], box[3]-box[2]))
	mark = False
#	black  = get_black(box_list, img)
	for i,box in enumerate(boxe43):
		_path = os.path.basename(imgpath).split('.jpg')[0] + "%02d"%i + '.jpg'
		#bpath = os.path.basename(imgpath).split('.jpg')[0] + "%02d"%i + 'b.jpg'
		if (listIou(box_list, box)):
			if getLabel(path) in labelSet:
				label = getLabel(path)
			else:
				label = '其他'
			_path = os.path.join(DIR_data, labelSet[label]+label, _path)

if __name__ == '__main__':
	labelDict = {}
	with open('code/label.txt') as f:
		labels = f.read().split('\n')
        for i,x in enumerate(labels):
		labelDict[x] = "%02d"%i
	path_list = glob.glob(DIR_xml+'*xml')
	for xmlpath in path_list:
		imgpath = os.path.join(os.path.dirname(xmlpath), os.path.basename(xmlpath).split('.xml')[0]+'.jpg')
		imgCrop = fun(xmlpath, imgpath, labelDict)
	for i in range(1,20):
		print(len([x for x in mem if (i-1)*100<x<i*100]))

