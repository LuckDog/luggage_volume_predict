import os
import imageio
import matplotlib.pyplot as plt
mask_path = '/home/ty/jishi/luggage_volume_predict'
mask_0 = imageio.imread(os.path.join(mask_path, '0-69_mask.png'))
mask_0 = mask_0 > 0
mask_70 = imageio.imread(os.path.join(mask_path, '70_mask.png'))
mask_70 = mask_70 > 0


depth_path = '/home/ty/baidunetdiskdownload/20191230_convert'
bottom_0 = imageio.imread(os.path.join(depth_path, 'Depth_0.bmp'))
bottom_0 = bottom_0*mask_0
bottom_70 = imageio.imread(os.path.join(depth_path, 'Depth_239.bmp'))
bottom_70 = bottom_70*mask_70
top_0 = imageio.imread(os.path.join(depth_path, 'Depth_4.bmp'))
top_0 = top_0*mask_0
top_70 = imageio.imread(os.path.join(depth_path, 'Depth_224.bmp'))
top_70 = top_70*mask_70


image = imageio.imread(os.path.join(depth_path, 'Depth_19.bmp'))


def ratio_0(image):
    return (image * mask_0 - bottom_0).sum() / (top_0 - bottom_0).sum()


def ratio_70(image):
    return (image * mask_70 - bottom_70).sum() / (top_70 - bottom_70).sum()
