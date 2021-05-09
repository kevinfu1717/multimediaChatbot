# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 18:41:27 2020

@author: Administrator
"""

import cv2
import paddlehub as hub
import os
import CVTools
import time
import numpy as np
from tqdm import tqdm
from tqdm._tqdm import trange

os.environ['CUDA_VISIBLE_DEVICES'] = '0'


def filesInFolder(rootdir, fileType='.jpg'):
    pathList = []
    nameList = []
    filelist = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(len(filelist)):
        if filelist[i][-4:] == fileType:
            pathList.append(os.path.join(rootdir, filelist[i]))
            nameList.append(filelist[i])
    return pathList, nameList


# 模型加载
# use_gpu：是否使用GPU进行预测

# model = hub.Module(name='animegan_v2_hayao_99', use_gpu=True)
modelName = []
modelName.append('animegan_v2_shinkai_53')
modelName.append('animegan_v2_shinkai_33')
modelName.append('animegan_v2_paprika_98')
modelName.append('animegan_v2_paprika_97')
modelName.append('animegan_v2_paprika_74')

modelName.append('animegan_v2_paprika_54')

modelName.append('animegan_v2_hayao_99')
modelName.append('animegan_v2_hayao_64')
modelName.append('animegan_v1_hayao_60')
modelName.append('UGATIT_92w')
modelName.append('UGATIT_83w')
modelName.append('UGATIT_100w')
modelName.append('U2Net_Portrait')
modelName.append('Photo2Cartoon')

# 模型预测
# t1 = time.time()
# folderPath = 'E://DATA//XULIEZHEN'
# folderPath = 'E://DLresult//mopi9'
#
# # folderPath='E://DLresult//p1//pa97-2in1'
# outPath = 'E://DLresult//p1//sh53-2in1MOPI'

# outPath='E://DLresult//p1//pa97-8in1'
# os.makedirs(outPath)
# pathList, nameList = filesInFolder(folderPath)


def rename(pathList):
    # 外循环遍历所有文件名，内循环遍历每个文件名的每个字符
    for index, path in enumerate(pathList):

        if 'result' in path:
            #          newpath=path.replace('zudui','组队')
            newpath = path.replace('组队', 'zudui')
            os.renames(path, newpath)


# rename()
# pathList, nameList = filesInFolder(folderPath)
# print(nameList)
##https://www.paddlepaddle.org.cn/hubdetail?name=animegan_v2_paprika_97&en_category=GANs
# model.style_transfer(paths=pathList[0:1],visualization=True,output_dir=outPath)
# bgpic = cv2.imread('bg1.jpg')
# img = cv2.imread('./test/mopi.jpg')
#
# img = cv2.imread('./thin 3.jpg')
# contenx = int(img.shape[1] / resizeIndex)
# conteny = int(img.shape[0] / resizeIndex)
# #
#
# image = bgpic.copy()
class cartoon_face():
    def __init__(self,faceLandmarker):
        self.faceLandmarker=faceLandmarker
        self.perspect_size=256
        # resizeIndex = 2
        modelN = modelName[-7]
        print('modelN', modelN)
        self.cartoon_model = hub.Module(name=modelN, use_gpu=True)
    def process(self,roi_img):
        roi_img = cv2.medianBlur(roi_img, 3)
        return self.cartoon_model.style_transfer(images=[roi_img], visualization=False)[0]

    def run(self,user_bot,emotion_flag=0):
        img_path=user_bot.imgPath
        print('emotion_flag',emotion_flag)
        print('img_path',img_path)
        img=[]
        img=cv2.imread(img_path)[:,:,:3]
        if len(img.shape)==0:return []
        landmarks=self.faceLandmarker.run(img)
        if len(landmarks)>0:
            roi_img=CVTools.roiChoice(landmarks, img, self.perspect_size)
            user_bot.roiImg=roi_img
            user_bot.roiCartoon=self.process(roi_img)
            # roi_img = cv2.medianBlur(roi_img, 3)
            # user_bot.roiCartoon =self.cartoon_model.style_transfer(images=[roi_img], visualization=False)[0]
            return user_bot
        else:
            return user_bot





if __name__=='__main__':
    from landmarkModule import landmarker
    la=landmarker()
    cf=cartoon_face(la)
    import botClass
    bot=botClass.bot()
    bot.imgPath='pic/24451810641815485231.jpg'
    out=cf.run(bot,2)
    # print('in',image.shape,'out',out.shape)
    cv2.imwrite('../cartoon.jpg', out.roiCartoon)
    # print('time', time.time() - t1)