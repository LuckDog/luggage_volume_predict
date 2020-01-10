import os
import sys
import shutil

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


if __name__ == '__main__':
	if(len(sys.argv) < 3):
		print("<input_img_dir> <output_img_dir>")
		sys.exit()
	input_image_dir = sys.argv[1]
	output_img_dir = sys.argv[2]
	cmd = "./NiViewer.exe " # convert tools
	image_list = getFileListFromDir(input_image_dir, "raw")
	for image_name in image_list:
		#if "Color" in image_name:
		#	continue
		cmd_new = cmd + image_name
		print(image_name)
		os.system(cmd_new)
	image_list_bmp = getFileListFromDir(input_image_dir, "bmp")
	mkDir(output_img_dir)
	for image_bmp in image_list_bmp:
		basename = image_bmp.split("/")[-1].split("\\")[-1]
		new_image_name = os.path.join(output_img_dir, basename)
		shutil.move(image_bmp, new_image_name)
		print(basename)
