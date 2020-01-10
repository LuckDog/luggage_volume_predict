import os
import sys
import cv2
import imageio
import matplotlib.pyplot as plt

def ratio(image, mask, top, bottom):
    return (image * mask - bottom).sum() / (top - bottom).sum()

def getRatio(image_name, mask, top, bottom):
	image = imageio.imread(image_name)
	volume_ratio = ratio(image, mask, top, bottom)
	return volume_ratio

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

# e.g: python .\volume_predict.py .\20191230_convert\ .\config_data\ out_img
if __name__ == '__main__':
	if(len(sys.argv) < 4):
		print("<input_img_dir> <config_data_path> <output_img_dir>")
		sys.exit()
	input_image_dir = sys.argv[1]
	config_data_path = sys.argv[2]
	output_img_dir = sys.argv[3]

	mask_path = config_data_path
	mask_0 = imageio.imread(os.path.join(mask_path, '0-69_mask.png'))
	mask_0 = mask_0 > 0
	mask_70 = imageio.imread(os.path.join(mask_path, '70_mask.png'))
	mask_70 = mask_70 > 0

	depth_path = config_data_path
	bottom_0 = imageio.imread(os.path.join(depth_path, 'Depth_0.bmp'))
	bottom_0 = bottom_0*mask_0
	bottom_70 = imageio.imread(os.path.join(depth_path, 'Depth_239.bmp'))
	bottom_70 = bottom_70*mask_70
	top_0 = imageio.imread(os.path.join(depth_path, 'Depth_4.bmp'))
	top_0 = top_0*mask_0
	top_70 = imageio.imread(os.path.join(depth_path, 'Depth_224.bmp'))
	top_70 = top_70*mask_70
	mkDir(output_img_dir)
	image_list = getFileListFromDir(input_image_dir, "bmp")
	for image_name in image_list:
		basename = image_name.split("_")[-1].split(".")[0]
		color_name = os.path.join(os.path.dirname(image_name), "Color_" + basename + ".png")
		output_img_name = os.path.join(output_img_dir, "Color_" + basename + ".png")
		print(color_name)
		if(int(basename) < 67):
			volume_ratio =  getRatio(image_name, mask_0, top_0, bottom_0)
		elif(int(basename) > 70):
			volume_ratio =  getRatio(image_name, mask_70, top_70, bottom_70)
		else:
			volume_ratio = -1
		img = cv2.imread(color_name)
		font = cv2.FONT_HERSHEY_SIMPLEX
		imgzi = cv2.putText(img, str(volume_ratio), (30, 30), font, 1.2, (0, 0, 255), 2)
		cv2.imshow("Volume Ratio", imgzi)
		cv2.imwrite(output_img_name, imgzi)
		cv2.waitKey(1)