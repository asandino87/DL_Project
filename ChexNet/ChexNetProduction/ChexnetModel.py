
from os import path
import numpy as np
import matplotlib.pyplot as plt

import cv2 as cv
import os
import pydicom as dicom

from AbstractProducts import load_mdl_chexnet
from ChexnetUtils import gradcam
from GenerateReport import GenerateReportClass 


# from seg_utils import create_segmentations

#%%
class ChexnetModel():

    def __init__(self,mdl):
        
        self.mdl=mdl
            
    def run_preprocessing(self,batch_x):
    
        batch_x = cv.resize(batch_x, (224,224))    
        batch_x = np.asarray(batch_x/255)
        imagenet_mean = np.array([0.485, 0.456, 0.406])
        imagenet_std = np.array([0.229, 0.224, 0.225])
        batch_x = (batch_x - imagenet_mean) / imagenet_std

        return batch_x


    def run_prediction(self,img):
        
        #patient_info = patient_info
        
        img_trans = self.run_preprocessing(img)
        img_trans2 = np.expand_dims(img_trans,axis=0)
        prediction = self.mdl.predict(img_trans2)
        prediction = np.squeeze(prediction,axis=0)
        
        im_heatmap=gradcam(self.mdl,img,img_trans2)
        
        #report(patient_info,prediction)

        return prediction

    def run_evaluation(self):
        pass

    def run_training(self):
        pass

#%% Prueba

mdl=ChexnetModel(load_mdl_chexnet())

#%%
imgdir = "C:/Users/Andres/Desktop/images/"

numfile = 1
listimgfile = os.listdir(imgdir)
imgfile = os.path.join(imgdir,listimgfile[numfile])

img = cv.imread(imgfile)

plt.imshow(img,cmap='gray')
plt.axis('off')
plt.title(listimgfile[numfile])

prediction2 = mdl.run_prediction(img)

# Metadata
patient_name = "Pepito Perez"
ID = '102234'
genre = 'F'
date = '02/02/02'
study_name = 'CHEST CT'
study_date = '01/01/01'
region = 'US' # or US
report='This report was automaticaly generated by theStella services. At least one patology pattern was indentified in this study. The heatmap overlead on the image represeted the area with the AI considered to do the automatic evaluation.'
report = report +report

report=GenerateReportClass(patient_name, ID, genre,date,study_name,study_date,report,prediction2,region)
report.generate_pdf()

print("el reporte ha sido generado con exito")
#zz.generate_pdf()

