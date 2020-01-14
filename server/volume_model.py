# -*- coding: utf-8 -*-  
import os
import sys
import cv2
import imageio
import matplotlib.pyplot as plt
import numpy
from PIL import Image, ImageDraw, ImageFont

def judgeIfClose(image, mask, top):
	image_mask = (image * mask) > 0
	mean_value = (image * mask * image_mask - top * image_mask).sum() / image_mask.sum()
	if mean_value < 0.015:
		return True
	else:
		return False

def judgeIfHasOcclusion(image, mask):
	image_mask = image * mask > 0
	sub_number = mask.sum() - image_mask.sum()
	if float(sub_number) / mask.sum() > 0.3:
		return True
	return False

def getMeanValue(image, rect_not_change):
	sub_image = image[rect_not_change[1]:rect_not_change[3], rect_not_change[0]: rect_not_change[2]]
	mean_value = sub_image.mean()
	return mean_value

def limit(image, value_1, value_2):
	mask_1 = image > value_1
	mask_2 = image < value_2
	#print((image < value_1).sum(), (image > value_2).sum())
	image = image * mask_1 * mask_2
	return image

def ratio(image, mask, top, bottom):
	image_mask = image*mask > 0
	top_mask = top > 0
	bottom_mask = bottom > 0
	intersection = image_mask*top_mask*bottom_mask

	bottom = bottom * intersection
	top = top * intersection
	image = image * intersection

	volume_area = bottom - top
	value_1 = 0
	value_2 = volume_area.max()
	volume_self = limit(bottom - image, value_1, value_2)
	volume_area = limit(volume_area, value_1, value_2)
	#print(volume_self.sum() / volume_area.sum())
	return volume_self.sum() / volume_area.sum()
	#print((bottom - image).max(), (bottom - image).min())
	#print((bottom - top).max(), (bottom - top).min())

	#print(((bottom - image) < 0).sum(), ((bottom - top) < 0).sum(), ((bottom - image) > 0).sum(), ((bottom - top) > 0).sum())

	#return (bottom - image).sum() / (bottom - top).sum()

def getRatio(image_name, mask, top, bottom, ref, rect_not_change):
	image = imageio.imread(image_name)[:,:, 0]
	image = getNormalImage(image)
	ref = getNormalImage(ref)
	sub_image = image[rect_not_change[1]:rect_not_change[3], rect_not_change[0]: rect_not_change[2]]
	sub_ref = ref[rect_not_change[1]:rect_not_change[3], rect_not_change[0]: rect_not_change[2]]
	bias = sub_image.mean()-sub_ref.mean()
	#image = image-bias
	volume_ratio = ratio(image, mask, top, bottom)
	if judgeIfHasOcclusion(image, mask):
		return -1.00
	if judgeIfClose(image, mask, top):
		return -2.00
	if volume_ratio < 0:
		volume_ratio = 0.00
	if volume_ratio > 1:
		volume_ratio = 1.00
	return round(volume_ratio,2)

def mkDir(dir):    
    if os.path.exists(dir):        
        return    
    else:        
        os.mkdir(dir)

def getFileListFromDir(fin_dir, suffix=""):
    file_list = []
    for root , dirs, files in os.walk(fin_dir):
        for file in files:
            path = os.path.join(root, file)
            if os.path.isfile(path):
                if len(suffix) != 0: 
                    if suffix in path:
                        file_list.append(path)
                else:
                    file_list.append(path)
    return file_list

def getNormalImage(image):
	image_mask = image > 0
	max_value = image.max()
	min_value = image.min()
	image_normal = (image - min_value) * image_mask / float(max_value - min_value)
	return image_normal

def getStatus(volume_ratio):
	if volume_ratio == -3.0:
		return ["camera motion", (0, 0, 0)]
	elif volume_ratio == -2.0:
		return ["luggage rack close", (0, 0, 0)]
	elif volume_ratio == -1.0:
		return ["object occlusion", (0, 0, 6)]
	else:
		return ["space", (0, 255, 0)]

class OccupationModel():
	def __init__(self, config_data_path):
		mask_path = config_data_path
		mask = imageio.imread(os.path.join(mask_path, '70_mask.png'))
		self.mask = mask > 0

		depth_path = config_data_path
		bottom = imageio.imread(os.path.join(depth_path, 'Depth_239.bmp'))
		top = imageio.imread(os.path.join(depth_path, 'Depth_224.bmp'))

		self.ref = imageio.imread(os.path.join(depth_path, 'Depth_239.bmp'))

		self.rect_not_change = (600, 135, 635, 155)

		bottom = getNormalImage(bottom)
		top = getNormalImage(top)
		self.bottom = bottom*self.mask
		self.top = top*self.mask		

	def predict(self, image_name):
		volume_ratio =  getRatio(image_name, self.mask, self.top, self.bottom, self.ref, self.rect_not_change)
		return volume_ratio