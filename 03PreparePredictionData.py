import numpy as np
from osgeo import gdal
import os

image_dir = r"ImageBlock/"
band_num = 10

def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName+"文件无法打开")
        return
    im_width = dataset.RasterXSize #栅格矩阵的列数
    im_height = dataset.RasterYSize #栅格矩阵的行数
    im_data = dataset.ReadAsArray(0,0,im_width,im_height)#获取数据
    np_data = np.array(im_data)
    np_data =np.expand_dims(np_data,axis=0)

    return np_data

def file_name(path):
    F = []
    for root, dirs, files in os.walk(path):
        #print root
        #print dirs
        for file in files:
            #print file.decode('gbk')    #文件名中有中文字符时转码
            if os.path.splitext(file)[1] == '.TIF':
                t = os.path.splitext(file)[0]
                F.append(t) #将所有的文件名添加到L列表中
    return F   # 返回L列表

fileNameArray = file_name(image_dir)
num_tif = len(fileNameArray)#计算包含多少个TIF文件
print(num_tif)

#直接创建该长度的数组
tif_np = np.zeros(shape=(num_tif,band_num,resolution,resolution))
print(tif_np.shape)
#设置一个计数器
tif_index = 0
for tif in fileNameArray:
    image_path = image_dir + tif+'.TIF'
    np_image = readTif(image_path)
    #append方法的原理是复制之前的数组，再加入一个新的，这样导致运行速度随着数组长度的增加而逐渐减慢。
    # tif_np = np.append(tif_np,np_image,axis=0)
    #不用append方法，采用直接赋值的方法
    tif_np[tif_index,:] = np_image
    tif_index = tif_index + 1
    print(tif_index)

def normalize(data):
    [one, _, _, four] = data.shape
    for i in range(one):
        for j in range(four):
            mean = np.mean(data[i, :, :, j])
            std = np.std(data[i, :, :, j])
            data[i, :, :, j] = (data[i, :, :, j] - mean) / std

    return data


tif_np = tif_np/10000
tif_np = np.transpose(tif_np,(0,2,3,1))
print(tif_np.shape)

np.save(r'F:/pre_image',tif_np)

