import cv2
import os
import pydicom
from pydicom.pixel_data_handlers.util import convert_color_space

inputdir = 'C:/Users/kimdh/PycharmProjects/data/USdicom_ex/'
outdir = 'C:/Users/kimdh/PycharmProjects/data/dicom_convert_to_png/'

test_list = [f for f in os.listdir(inputdir)]

for f in test_list:
    ds = pydicom.dcmread(inputdir + f) # read dicom image
    temp = ds.pixel_array # get image array
    img = convert_color_space(temp, 'YBR_FULL', 'RGB')
    cv2.imwrite(outdir + f.replace('.dcm','.png'),img) # write png image
    cv2.im