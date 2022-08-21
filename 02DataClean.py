import numpy as np
from osgeo import gdal
import os

image_dir = r'ImageBlockFolder'
resolution = 32
band_num = 10

def cleanData(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName+"Can't open file")
        return
    im_width = dataset.RasterXSize #the number of columns of the raster matrix
    im_height = dataset.RasterYSize #the number of rows of the raster matrix
    if im_width != resolution or im_height != resolution:
        image_path =  os.path.split(fileName)
        image_name = os.path.splitext(image_path[1])
        removeName.append(image_name[0])
        print(image_name[0] + ' should be removed')


def file_name(path):
    F = []
    for root, dirs, files in os.walk(path):
        #print root
        #print dirs
        for file in files:
            if os.path.splitext(file)[1] == '.TIF':
                t = os.path.splitext(file)[0]
                F.append(t) #Add all TIFFs to the list
    return F   # return list

fileNameArray = file_name(image_dir)
removeName = []
i=0
for tif in fileNameArray:
    image_path = image_dir + tif+'.TIF'
    i=i+1
    if(i%1000 == 0):
        print(i)
    cleanData(image_path)

for rN in removeName:
    imageTIF = image_dir + rN+'.TIF'
    imageTFW = image_dir + rN + '.tfw'
    imageXML = image_dir + rN + '.TIF.aux.xml'
    imageOVR = image_dir + rN + '.TIF.ovr'
    if os.path.exists(imageTIF):  
        os.remove(imageTIF)
    if os.path.exists(imageTFW):  
        os.remove(imageTFW)
    if os.path.exists(imageXML):  
        os.remove(imageXML)
    if os.path.exists(imageOVR):  
        os.remove(imageOVR)
    print(rN + ' has been removed')