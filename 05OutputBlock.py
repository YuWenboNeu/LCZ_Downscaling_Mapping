import tensorflow as tf
import numpy as np
from osgeo import gdal
from osgeo import osr
import os



result = np.load(r'result.npy')
image  = r'ImageBlockFolder/'
out_path  =  r'LCZBlockFolder/'
resolution = 32
def writeTif(fileName,outPath,lczType,imgFile):
    dataset_o = gdal.Open(fileName)
    if dataset_o == None:
        print(fileName+"Can't open file")
        return
    datatype = gdal.GDT_UInt16
    img_array = np.full((resolution,resolution),lczType)
    im_geotrans = dataset_o.GetGeoTransform()
    im_proj = dataset_o.GetProjection()
    driver = gdal.GetDriverByName("GTiff")
    imgOutPath = outPath+"\\" + imgFile + '.TIF'
    dataset_d = driver.Create(imgOutPath, resolution, resolution, 1, datatype)
    dataset_d.SetGeoTransform(im_geotrans)
    dataset_d.SetProjection(im_proj)
    dataset_d.GetRasterBand(1).WriteArray(img_array)
    del dataset_d
    del dataset_o

def file_name(path):
    F = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.TIF':
                t = os.path.splitext(file)[0]
                F.append(t)
    return F

def outputIMG(image_dir,out_path,result):
    fileNameArray = file_name(image_dir)
    num_tif = len(fileNameArray)
    tif_index = 0

    for tif in fileNameArray:
        i_lcz = result[tif_index]
        imgPath = image_dir + tif + '.TIF'
        writeTif(imgPath, out_path, i_lcz, tif)
        tif_index = tif_index + 1
        if  tif_index%1000 == 0:
            print('LCZ Type: ' + tif + ' is ' + str(i_lcz) + "\t Number = " + str(tif_index))
outputIMG(image,out_path,result)


