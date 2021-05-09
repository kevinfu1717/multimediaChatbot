
import moviepy.video.io.ImageSequenceClip
# import imageio
# 
# from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np
import time
import CVTools
from faceFatModule import face_morph

def makeMovie(imgList, fps=4, outputPath=''):
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(imgList, fps=fps)
    path=outputPath + 'video' +str(time.time())+ '.mp4'
    clip.write_videofile()
    return path

class movie_maker():
    def __init__(self,outPath,landmarker,cartoon_maker):
        self.cartoon_maker=cartoon_maker
        self.outPath=outPath
        print('movie maker',self.outPath)
        self.face_morph=face_morph(landmarker,self.cartoon_maker)
        self.view_morph=''
        self.handImg=cv2.imread('resource/zhang.png',cv2.IMREAD_UNCHANGED)
        print('self.handImg',self.handImg.shape)
    def run(self,user_bot,emotion_flag):#cartoonImg,roiLandmarks,specialImg
        if emotion_flag==2:
            if len(user_bot.specialImg)==0:
                user_bot=self.face_morph.run(user_bot)

            if len(user_bot.roiLandmarks)==0:
                r_position=user_bot.cartoonImg.shape[1]/2
                l_position=user_bot.cartoonImg.shape[1]/2
            else:
                r_position = [max(np.array(user_bot.roiLandmarks)[:,1]),
                              (max(np.array(user_bot.roiLandmarks)[:,0])+min(np.array(user_bot.roiLandmarks)[:,0]))/2]
                l_position =[min(np.array(user_bot.roiLandmarks)[:,1]),
                              (max(np.array(user_bot.roiLandmarks)[:,0])+min(np.array(user_bot.roiLandmarks)[:,0]))/2]
            rightImg=CVTools.combineImg(self.handImg,user_bot.roiCartoon,  r_position,2)
            leftImg=CVTools.combineImg(self.handImg,user_bot.roiCartoon,  l_position,1)
        ####
            user_bot.roiCartoon=cv2.cvtColor(user_bot.roiCartoon,cv2.COLOR_BGR2RGB)
            rightImg=cv2.cvtColor(rightImg,cv2.COLOR_BGR2RGB)
            leftImg=cv2.cvtColor(leftImg,cv2.COLOR_BGR2RGB)
            user_bot.specialImg=cv2.cvtColor(user_bot.specialImg,cv2.COLOR_BGR2RGB)
        ####
            imgList=[user_bot.roiCartoon,user_bot.roiCartoon,
                       rightImg,rightImg,
                       rightImg,
                       user_bot.roiCartoon, user_bot.roiCartoon,
                       leftImg,leftImg,
                       leftImg,
                       user_bot.specialImg, user_bot.specialImg,
                       user_bot.specialImg, user_bot.specialImg,
                       user_bot.specialImg, user_bot.specialImg,
                       user_bot.specialImg, user_bot.specialImg
                     ]

            user_bot.moviePath=CVTools.makeMovie(imgList,self.outPath)
        return user_bot

if __name__=='__main__':
    import botClass
    from landmarkModule import landmarker
    bb=botClass.bot()
    la=landmarker()
    bb.roiCartoon=cv2.imread('pic/1620210456.7131963.jpg')
    bb.roiLandmarks=la.run(bb.roiCartoon)[0]
    bb.specialImg=cv2.imread('../facefatter.jpg')
    mm=movie_maker('pic/',la)
    bb=mm.run(bb,1)
    print(bb.moviePath)