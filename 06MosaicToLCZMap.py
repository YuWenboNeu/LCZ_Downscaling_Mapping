import arcpy
import numpy as np
import os

image_dir = 'LCZBlockFolder/'
def file_name(path):
    F = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.TIF':
                t = os.path.splitext(file)[0]
                p = path + t+ '.TIF'
                F.append(p)
    return f
fileNameArray = file_name(image_dir)
print(fileNameArray[0])
arcpy.MosaicToNewRaster_management(fileNameArray,"Folder","LCZ.tif","#","16_BIT_UNSIGNED","#","1","#","#")