# Paddlehub微信聊天机器人-图片、动图、视频动态生成的多轮情景对话

## 项目描述
构建了可用于多个对话框架的场景型对话的聊天机器人。支持吐槽类情景及情感倾诉型情景。使用wechaty，结合Paddlehub的人脸特征点、动漫人脸生成、对联生成、情感分类，ernie迁移，人脸变胖

## 项目结构
```
-|data
-|resource
-README.MD
```
## 使用方式
A：在AI Studio的脚本任务上[运行本项目](https://aistudio.baidu.com/aistudio/usercenter)
B：在配置比较好的服务器上运行

# A.摘要

##  1.功能简介

本项目构建了一个用于场景型多轮对话，这里可用于让人们吐槽（图嘈）发泄，以及情感倾诉。根据对话内容，分析对话者是情感倾诉还是要吐槽发泄，会进入多轮对话文本、爬虫获取信息、卡通人脸生成、吐槽对称句生成、变胖人脸生成、情话生成、动态个性化表情动图生成、视频合成等多模块组合到一个聊天模块下，可方便根据聊天情景快速切换到自己的场景使用

本项目中对话为特定情景下的引导性对话，非开放性闲聊对话。但多资源反馈部分，也可以接入开放性闲聊对话，增加对话乐趣。

##  2.整体流程

2.1 botProces中的bot_manager使用类似“简易工厂模式”。（熟悉工厂模式的筒子可以忽略本段）。每一个触发聊天的用户都会生成一个user_bot,用户的输入就好像工厂里面的原材料，经过bot_manager分配到各个工序的工人(各个技能模块，如：卡通人脸生成、爬虫、变胖人脸等）进行处理，最终组装好的产品给到用户。不同用户的输入就像不同的原材料，不断送进工厂处理，流水的bot铁打不变的bot_manager，而每个user_bot装载的是整个聊天过程中的所有对话。以上纯属个人胡扯，工厂模式正规解释具体见：[https://www.cnblogs.com/wly923/archive/2013/05/10/3068313.html](http://https://www.cnblogs.com/wly923/archive/2013/05/10/3068313.html)

2.2 talkProcess中会把botProcess中返回的对话内容，“翻译”成真正发给用户的内容。例如：是文本的直接返回，要生成cartoon图的生成卡通图给用户，要生成被打肿了的脸的则去生成打肿的脸的视频等。


##  3.包含框架及模块

调用Paddlehub来丰富chatbot的技能，直接使用或修改后使用的Paddlehub模块。包含了：

### 3.1 情感分类

emotion_detection_textcnn模型：所在脚本 emotionModule.py

### 3.2 漫画人脸生成

animegan 模型：所在脚本cartonModule.py
    
——需要调整图片尺寸或图片的纹理复杂度，再中值滤波，不然就会脸上很多线条。animegan在处理特写人脸时，可能训练样品不够，需要图片预处理了再生成。
      
![](https://ai-studio-static-online.cdn.bcebos.com/e509e94f3b9c4482b7b2c8806d10dd29e54aba4bfc3f47d19f50b1b0b39888cb)
    

### 3.3 对偶句生成
ernie_gen_couplet/ernie_gen模型：所在脚本coupletModule.py

### 3.4 情话生成 
ernie_gen_lover_words模型：所在脚本	loveModule.py

### 3.5 人脸特征点
face_landmark_localization模型：所在脚本landmarkModule.py
在多个人脸变形或口型或换脸中使用

![](https://ai-studio-static-online.cdn.bcebos.com/62ffe830a6fa40a1a99ed53229fb1dcd58fc691948e6496d8473510039c1ac58)

另再加上：

### 3.6 百度爬虫:	

所在脚本：crawlerModule.py

——根据对话内容爬取需要的图片

### 3.7 人脸变胖:

所在脚本：faceFatModule.py
    
——使用类似瘦脸的方法，让人变成胖子
      
![](https://ai-studio-static-online.cdn.bcebos.com/53d0ffe790a84d768c43dee3aa538b1ef105e7ee47514c15b83fb9857bf76222)


### 3.8 人脸五官迁移到动态表情包:	

所在脚本：emoiModule.py
    
——下载下来的表情包，用Paddlehub的ocr截取文字内容，并按文字内容标签该图。拿类似的文案替换进去。同时，把用户的人脸与表情包原来的人脸进行对齐，换成用户提供的人脸的黑白图，并生成闭嘴的图。写上新的吐槽语句，组合起来一个gif或视频的动图表情包
      

![](https://ai-studio-static-online.cdn.bcebos.com/268d1cbd3026461d95d60d0a5cfda9eb2b7a1caea5e34dfd9305fc2e233e4cf9)

### 3.9 视频/动图生成:
所在脚本：movieModule.py

### 3.10 词向量匹配
所在脚本：roastModule.py

我收集了吐槽大会的几百句经典语录。对经典吐槽语句的句子的n系列词性的词组建立句子vector向量（v系列词性的也建了，但效果不好没使用），然后对要处理的句子进行相似计算。
PS:因aistudio脚本任务运行Paddlehub的wordvector报错，暂时关了此功能，若在其他地方运行，在代码中取消=None即可开启

### 3.11 wechaty聊天框架

本次中使用wechaty作为对话框架，使用起来稍麻烦一些，稍后整理使用
所在脚本：run_bot.py

    

# B. 主要功能模块 及 脚本简述

## 1.  botclass.py 定义的每个聊天对象：


```python
class imgContainer():
    def __init__(self):
        self.landmarks=[]#用户发的原始图的人脸特征点
        self.imgPath='' #用户发的图的路径
        # self.cartoonImgPath=[]
        self.roiImg=[] #用户发的图切出人脸附近区域
        self.roiCartoon=[] # 人脸附近区域进行漫画话
        self.specialImg=[] #进行特殊处理的图，如：吐槽是打脸的图
        self.filtImg=[] #
        self.roiLandmarks=[] #变成emoi表情时，进行人脸对齐时的人脸特征点
        self.emoi=[] #生成的emoi表情图片
        self.emoiWordsArea=[] #emoi的文字所在区域
        self.emoiMoviePath=''#emoi输出的视频或gif的地址
class bot(imgContainer):
    def __init__(self):
        self.param_init()
        self.user_init()
    def user_init(self):
        self.userName = ''#用户微信名称，暂时作为唯一id
    def param_init(self):
        super(bot,self).__init__()
        self.imgbot=imgContainer()
        self.client=""
        self.inTime=0 #进入时间
        self.queryList=[] #用户说的话
        self.replys=[] #每次回复，回复用户的内容（列表）
        self.replys_index=0 #回复用户的话回复到第几部分
        self.talkPic=[] 

        self.step=0#当前step
        self.stepRecord=[]#经历过的step
        self.emoition=''#情感类别
        self.emoitionRatio=0#情感强度
        self.abstract=''#用户对吐槽物的概述
        self.description=[]#用户对吐槽物的进一步描述
        self.ganImgPath=[]# 生成的图片路径
        self.transImgPath=[] #进行处理后图片路径
        self.ganTextList=[] #生成的文本列表
        self.moviePath='' #生成的视频地址
```

## 2.  botProcess.py 定义的每个聊天对象：

后面有时间或者大家反响好就更换成状态机。有接触过游戏引擎的筒子都应该了解了，能实现多状态切换。之前实现了一套，在xmind编辑流程图，输出后作为chatbot不同主题的流程剧本，可以有多主题以及不同主题间跳转。


```python
from collections import deque
import botClass
import time
import cv2
# from emoiProcess import face_drawer
# from morphImg import face_movie
import numpy as np


class botManger():
    def __init__(self,maxuser):
        self.userBotDict={}
        self.userTimeDict={}
        self.maxuser=maxuser
        self.splitNum=5
        self.loopLimit=4
        self.rightWords=['对','是','没错','嗯','yes','Yes','YES','right','Right']
        self.falseWords=['不','没有','No','no','NO']
        self.joinWords=['吐槽','图嘈','倾诉','树洞','心事']
        self.replyList=["""”图槽树洞“  这里是一个你可以倾诉对某人的心事，发泄吐槽某人的地方。我是一个机器人，你不用担心会泄漏出去。
           你只需要发你想向他/她倾诉的人或要吐槽的人或物的照片或名字就可以开始了""",
           "88~~ 主人我没空 不跟你玩了"]
    def createBot(self,username,content):
        print('bot process create', username)
        self.userBotDict[username]=botClass.bot()
        self.userBotDict[username].userName=username
        return self.updateBot(username,content)
    def updateBot(self,username,content):
        print('bot process update', username,content)
        # print('botprocess self.userTimeDict[username]',self.userTimeDict)
        self.userTimeDict[username]=time.time()
        self.userBotDict[username].queryList.append(content)
        # print('botprocess self.userTimeDict[username]',self.userTimeDict)
        ##
        return self.talk(username,content)
    def get_target_img(self,username,content,step):
        self.userBotDict[username].step = step

        if content[:self.splitNum]=='#pic#':
            try:
                # time.sleep(0.2)
                self.userBotDict[username].imgPath = content[self.splitNum:]
                # print('img----', self.userBotDict[username].img.shape)
            except Exception as e:
                pass
            # print('du tu', e)
            # time.sleep(1)
            # self.userBotDict[username].img = cv2.imread(content[self.splitNum:])
        replys=['#str#'+username+' 请一两句话概况你想对他/它说的话']

        self.userBotDict[username].replys_index = len(replys)
        self.userBotDict[username].replys.append(replys)
        return self.userBotDict[username]
    def TrueFalse(self,words):
        for rw in self.rightWords:
            if rw in words:
                for fw in self.falseWords:
                    if fw in words:
                        return False
                return True
        return False

    def talk(self,username,content):
        ##########跳出死循环
        if len(self.userBotDict[username].stepRecord)>=self.loopLimit:
            if sum(self.userBotDict[username].stepRecord[-1*self.loopLimit:])== \
                    self.userBotDict[username].stepRecord[-1]**self.loopLimit:
                self.userBotDict[username].step =100
        ##########"""这部分后面用状态机替换掉就不贴出来了，可以源文件里看"""
    def removeBot(self,dictKey):
        print('bot process remove',dictKey)
        del self.userTimeDict[dictKey]
        del self.userBotDict[dictKey]
    def getBotList(self):
        return self.userBotDict
    def run(self,username,content):
        if username in self.userBotDict.keys():
            print('botprocess already user；',self.userBotDict[username])
            return self.updateBot(username,content)
        else:
            for word in self.joinWords:
                if word in content:
                    print('join word',word)
                    if len(self.userBotDict)>self.maxuser:
                        oldest=min(list(self.userTimeDict.values()))
                        inList = list(self.userTimeDict.keys())[list(self.userTimeDict.values()).index(oldest)]
                        self.removeBot(inList)

                    return self.createBot(username, content)

        return None
if __name__ == "__main__":
    from talkProcess import talkManger
    tm=talkManger()

    bm=botManger(2)
    from testTemplate import *

    inputsList=inputsList1
    for inputs in inputsList:
        print('inputs[1]',inputs[1])
        re=bm.run(inputs[0],inputs[1])

        for i in range(re.replys_index):
            re,rdict=tm.run(re)
            print(rdict)



```

## 3. talkprocess.py 实现多种形式的对话（支持动图、图片、文本、视频）：

结合返回内容的包头，是#str# #emo# #mov#来进行各种爬取图片、文本生成、图片生成、表情包生成、视频生成、卡通化、打肿的人脸等的生成


```python
import paddlehub as hub
from loveModule import love_module
from emoiModule import emoi_movie_module
from movieModule import movie_maker
from emotionModule import emotion_module
from crawlerModule import pic_crawler
from  cartonModule import cartoon_face
from landmarkModule import landmarker
from coupletModule import couplet_module
import time
import cv2
import numpy as np
class talkManger():
    def __init__(self,outPath,tempPicPath,emoi_folder='data/emoi/',debug=False):
        self.splitNum=5
        self.love_module=love_module
        self.couplet_module=couplet_module
        self.landmarker=landmarker()
        self.cartoon_face=cartoon_face(self.landmarker)

        self.emoi_movie_maker=emoi_movie_module(emoi_folder, outPath, self.landmarker, debug)


        self.movie_maker=movie_maker(outPath,self.landmarker)
        self.emotion_module=emotion_module
        self.crawl_module=pic_crawler(tempPicPath)
        self.outPath=outPath
    def run(self,userDictBot,packageList=[],nums=5):
        # print('userDictBot',userDictBot)
        if len(packageList)==0:packageList=userDictBot.replys[-1]
        # print('packageList',packageList)
        package = packageList[len(packageList)-userDictBot.replys_index]
        # print('package',package)
        userDictBot.replys_index-=1
        # print('package[:self.splitNum]',package[:self.splitNum])
        if package[:self.splitNum]=='#str#':
            print({'str':package[self.splitNum:]})
            return userDictBot,{'str':package[self.splitNum:]}
        elif package[:self.splitNum]=='#cra#':
            result=self.crawl_module.run(package[self.splitNum:])
            userDictBot.imgPath=result[0]
            return userDictBot,{'pic':userDictBot.imgPath}

        elif package[:self.splitNum]=='#cla#':
            result =self.emotion_module.emotion_classify(texts=[package[self.splitNum:]])[0]
            print('emotion result:',result)
            if result['positive_probs']>result['negative_probs']:

                userDictBot.emoition='positive'
                userDictBot.emoitionRatio = result['positive_probs']
            else:

                userDictBot.emoition='negative'
                userDictBot.emoitionRatio = result['neutral_probs']


            return userDictBot,{}
        elif package[:self.splitNum] == '#gst#':
            inputs=eval('userDictBot.'+package[self.splitNum:])
            # if package[self.splitNum:]=='abstract':
            #     inputs=userDictBot.abstract
            # elif package[self.splitNum:]=='description':
            #     inputs = userDictBot.description

            if userDictBot.emoition=='positive' :

                result =self.love_module.generate(texts=[inputs],  beam_width=nums)[0][np.random.randint(nums)]

            else:
                result=self.couplet_module.generate(texts=[inputs],  beam_width=nums)[0][np.random.randint(nums)]

            userDictBot.ganTextList.append(result)
            return userDictBot, {'str': result}
        elif package[:self.splitNum] == '#gim#':
            if userDictBot.emoition=='positive' :
                emotion_flag=1
            else:
                emotion_flag = 2
            userDictBot=self.cartoon_face.run(userDictBot ,emotion_flag)
            path=self.outPath+str(time.time())+'.jpg'
            cv2.imwrite(path,userDictBot.roiCartoon)
            userDictBot.cartoonImgPath=path
            return userDictBot,{'pic':path}

        elif package[:self.splitNum] == '#emo#':
            inputs = eval('userDictBot.' + package[self.splitNum:])
            if userDictBot.emoition == 'positive':
                emotion_flag=1
            else:
                emotion_flag=2
            print('emo inputs',[inputs],emotion_flag)

            userDictBot = self.emoi_movie_maker.run(userDictBot,[inputs],emotion_flag)
            # userDictBot.emoiMoviePath=result
            return userDictBot, {'mov': userDictBot.emoiMoviePath}

        elif package[:self.splitNum] == '#mov#':
            if userDictBot.emoition == 'positive' or userDictBot.emoition == 'neutral':
                emotion_flag=1
            else:
                emotion_flag = 2
            userDictBot=self.movie_maker.run(userDictBot,emotion_flag)
            return userDictBot, {'mov': userDictBot.moviePath}

```

## 4.动态生成特定人脸的表情包 emoiModule.py
1. 需要下载广大网友的表情包，运行表情包处理的代码，筛选出有一定文字长度及能识别到人脸的表情包。识别“文字位置”及“人脸特征点位置”，然后备着后面用（下图为原emoi图）

![](https://ai-studio-static-online.cdn.bcebos.com/de8b7ea00be143fba77c2c2d5292fc561cc0ec9860ac429fb729601a9ccfaaf0)

  

2. 对用户发上来的人脸，识别人脸特征点，并框选特征点内所在的矩形（比特征点所在区域大及像素，效果会好些）。对该区域进行二值化等图像处理，提取出黑白的人脸五官图

3. 把人脸五官的黑白图的五官通过本项目中的CVTools.py里面的morph脚本与表情包的人脸进行角度朝向位置的对齐。

![](https://ai-studio-static-online.cdn.bcebos.com/799090ba64c24b6bb13e5b4786955ef66bb28ceb7acb4ceeb775a8c1eee22d8f)


4. 用cv2.seamlessclone进行五官融合得到表情图a

![](https://ai-studio-static-online.cdn.bcebos.com/f16303d9543c4e70888f208099dd82b84fbc5b47ad494800acfea509afda974e)


5. 生成根据人脸特征点生成一个闭嘴的图片，并融合到表情图a上，生成一张新的表情图b。下图为闭嘴图片，就是那一横（因这种是黑白emoi，不用很细致，直接opencv画出闭嘴的，不进行morph了）

![](https://ai-studio-static-online.cdn.bcebos.com/57f4c421cbd34df182eb227fa9f7302157963f539166471f8dbf36eb1e6a6a9f)


6. 序列插入图片，有闭嘴的图有原来的图间或组合在一起形成口在动。并在表情包原来打字的位置，重新用PIL库写上字（用字库会好看一些）

7. 用emoi_movie_module 调用imageio或moviepy生成gif或视频mp4

![](https://ai-studio-static-online.cdn.bcebos.com/268d1cbd3026461d95d60d0a5cfda9eb2b7a1caea5e34dfd9305fc2e233e4cf9)



```python
import cv2
import numpy as np
import CVTools

def transformation_points(src_img_shape, src_points, dst_img, dst_points):
    src_points = np.matrix(src_points, np.float64)[:27, :]
    dst_points = np.matrix(dst_points, np.float64)[:27, :]
    print('emoi trans')
    print('src_points', src_points.shape)
    print('dst_points', dst_points.shape)
    c1 = np.mean(src_points, axis=0)
    c2 = np.mean(dst_points, axis=0)

    src_points -= c1
    dst_points -= c2

    s1 = np.std(src_points)
    s2 = np.std(dst_points)

    src_points /= s1
    dst_points /= s2

    u, s, vt = np.linalg.svd(src_points.T * dst_points)
    r = (u * vt).T

    m = np.vstack([np.hstack(((s2 / s1) * r, c2.T - (s2 / s1) * r * c1.T)), np.matrix([0., 0., 1.])])

    output = cv2.warpAffine(dst_img, m[:2],
                            (src_img_shape[1], src_img_shape[0]),
                            borderMode=cv2.BORDER_TRANSPARENT,
                            flags=cv2.WARP_INVERSE_MAP)

    return output


class emoi_module():
    def __init__(self,dataPath,outPath,landmarker,debug=False):
        self.outPath=outPath
        self.face_landmark=landmarker
        self.debug=debug
        self.landmarkPath = dataPath + 'landmarkArray.txt'
        self.img_base_folder=dataPath +'pic/'
        self.landmarkBaseDict = {}
        self.textBaseDict = {}
        self.posBaseDict = {}
        with open(dataPath + 'landmarkArray.txt', encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                data = line.split(";")
                key=data[0]
                landmarkList=data[1].split(" ")
                landmark=[ float(la) for la in landmarkList]
                landmark=np.array(landmark)
                landmark = np.reshape(landmark,(68,2))
                self.landmarkBaseDict[key]=landmark
        # print('self.landmarkBaseDict',self.landmarkBaseDict)
        ##
        with open(dataPath + 'sentencePosition.txt',encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                data = line.split(";")
                # print(data)
                # print('eval(line)',(line),type(line),len(line))
                try:
                    key=data[0]
                    self.textBaseDict[key]=data[1]
                    posStr=data[2].replace(' ','')
                    posStr = posStr.replace(r"\n", '')
                    posStr=posStr[:-1]
                    posStr=posStr.replace('][',',')
                    posArray=np.array(eval(posStr))
                    posArray=np.reshape(posArray,(-1,4,2))
                    # print(posArray)
                    self.posBaseDict[key]=posArray

                except Exception as e:
                    print('eeeeeee',e,posStr)
                    # print(posList)

            # print('self.posBaseDict', self.posBaseDict[0:2],len(self.posBaseDict[1]),len(self.posBaseDict[0]))
        # print('self.landmarkBaseDict,',self.posBaseDict,self.textBaseDict)

    def _baidu_landmark(self, img):
        # landmarks = []
        # print('begin baidu landmark')
        landmarks = self.face_landmark.run(img)
       # print('emoi baidu landmark',landmarks)

        return landmarks

    def get_source_landmark(self, user_bot):
        if len(user_bot.landmarks )==0:
            img = cv2.imread(user_bot.imgPath)
            landmarks = self._baidu_landmark(img)[0]
            user_bot.landmarks = landmarks
        #        print('landmarks',landmarks.shape)
        return user_bot

    def get_tranInput_landmark(self, imgContainer, baseLandmark):
        try:
            roiimg = imgContainer.roiImg

            landmarks = self._baidu_landmark(imgContainer.roiImg)[0]
            print('landmarks get tran input', landmarks)
            # for  la in landmarks:
            #     print('la',la)
            # lal=[]
            # for la in landmarks:
            #     lal.append((la[0],la[1]))
            # cv2.circle(roiimg,lal,2,(0,255,0))
            if self.debug:
                cv2.imwrite('roiimg.jpg', roiimg)
            if len(landmarks) > 0:
                imgContainer.roiLandmarks = landmarks
                # TODO 根据效果看是否要加
                #imgContainer.roiLandmarks = baseLandmark
                #imgContainer.roiLandmarks = ProcessPoints(landmarks)
                print('sucess get roi landmark')
                return imgContainer
        except Exception as e:
            print('get_tranInput_landmark', e)
        # 若转换后无法再识别landmark，暂时用source，TODO 改为第一次landmark点做变换
        imgContainer.roiLandmarks = baseLandmark

        return imgContainer
    def get_emoi(self, imgContainer, baseImg, basePos, bias=4):
        if len(imgContainer.roiLandmarks) > 0:
            landmark = np.array(imgContainer.roiLandmarks, dtype=np.int)

        # print(landmark.shape)
        # print(np.min(landmark[:,1]),np.max(landmark[:,1]),np.min(landmark[:,0]),np.max(landmark[:,0]))
        # https://github.com/PaddlePaddle/PaddleHub/tree/release/v2.1/modules/image/keypoint_detection/face_landmark_localization
        # 扩大一下roi
        area = imgContainer.roiImg[(np.min(landmark[17:, 1]) - bias):(np.max(landmark[17:, 1]) + 2 * bias),
               np.min(landmark[17:, 0]) - bias:np.max(landmark[17:, 0]) + bias, :]
        gray = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)
        thresh3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 2)
        kk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
        filtImg = cv2.morphologyEx(thresh3, cv2.MORPH_CLOSE, kk)
        imgContainer.filtImg = filtImg
        filtImg = cv2.cvtColor(filtImg, cv2.COLOR_GRAY2BGR)

        mask = 255 * np.ones(filtImg.shape, filtImg.dtype)

        # center (x,y)
        center = (int(np.min(landmark[17:, 0]) - bias + filtImg.shape[0] / 2),
                  int(np.min(landmark[17:, 1]) - bias + filtImg.shape[1] / 2))
        # center=(100,150)
        # print('filtImg.shape, center',filtImg.shape, center)
        # cv2.imwrite('filtImg.jpg', filtImg)

        normal_clone = cv2.seamlessClone(filtImg, baseImg, mask, center, cv2.NORMAL_CLONE)
        # cv2.imwrite('normal_clonemask.jpg', normal_clone)
        ##
        # print('basePos',basePos)
        emoiWordsArea = {}
        for bp in basePos:
            # bp [[12, 9], [208, 9], [208, 32], [12, 32]],  bp [[89, 30], [124, 30], [124, 55], [89, 55]]
            # print('bp',bp)
            normal_clone[bp[0][1]:bp[2][1], bp[0][0]:bp[2][0], :] = [255, 255, 255]
            emoiWordsArea[(bp[2][0] - bp[0][0]) * (bp[2][1] - bp[0][1])] = [bp[0][0], bp[0][1], bp[2][0] - bp[0][0],
                                                                       bp[2][1] - bp[0][1]]
            # print('emoiWordsArea',emoiWordsArea)
        # normal_clone=cv2.resize(normal_clone,(normal_clone.shape[0]+normal_clone.shape[0]%2,normal_clone.shape[1]+normal_clone.shape[1]%2))
        normal_clone = cv2.resize(normal_clone,
                                  (normal_clone.shape[1] + normal_clone.shape[1] % 2,
                                   normal_clone.shape[0] + normal_clone.shape[0] % 2))
        imgContainer.emoi = normal_clone
        imgContainer.emoiWordsArea = emoiWordsArea
        # print(cv2.imwrite('./normal_clone.jpg', normal_clone))
        return imgContainer

    def get_transformFace(self, baseShape, baseLandmark, user_bot):
        img=cv2.imread(user_bot.imgPath)

        rotateImg = transformation_points(baseShape, baseLandmark, img, user_bot.landmarks)
        user_bot.roiImg = rotateImg
        # cv2.imwrite("rotateImg.jpg",rotateImg)
        return user_bot

    def run(self, user_bot,emotion_flag):
        index = 1
        # imgBaseDict = self.picBasePathList[index]
        img_base_name=list(self.landmarkBaseDict.keys())[index]
        img_base_path=self.img_base_folder+img_base_name
        # print('path', path)
        #                path='data/emoi/emoiOutput/000001.jpg'
        imgBase = cv2.imread(img_base_path)

        basePos = self.posBaseDict[img_base_name]
        # baseLandmark=self.landmarkBaseDict[img_base_name]
        baseLandmark=self._baidu_landmark(imgBase)[0]
        user_bot=self.get_source_landmark(user_bot)

        user_bot = self.get_transformFace(imgBase.shape, baseLandmark, user_bot)
        print('transform face')
        user_bot = self.get_tranInput_landmark(user_bot, baseLandmark)
        print('landmkark')
        user_bot = self.get_emoi(user_bot, imgBase,  basePos)
        print('get emoi')
        # imgContainer = self.printText(imgContainer)
        return user_bot
    # def run(self,user_bot,sentence,emotion_flag):
    #     user_bot=self.process_emoi( user_bot)
    #     return user_bot

class emoi_movie_module():
    def __init__(self,emoiFolder,outPath,landmarker,debug=False):
        self.outPath=outPath
        print('emoi movie',self.outPath)
        self.debug=debug
        self.landmarker=landmarker
        self.emoier = emoi_module(emoiFolder, outPath, landmarker, self.debug)

    def run(self,user_bot,sentenceList,emotion_flag,outType='mp4'):

        user_bot = self.emoier.run(user_bot, emotion_flag)
        ##
        self.talkOnce(user_bot)
        imgList = self.printText(user_bot,sentenceList)
        # print('make movie',imgList)
        if outType=='gif':#movie
            user_bot.emoiMoviePath = CVTools.saveGif(imgList, self.outPath)
        else:
            user_bot.emoiMoviePath=CVTools.makeMovie(imgList,self.outPath)
        #
        return user_bot

    def morph(self, user_bot):
        img = user_bot.emoi
        # cv2.imwrite('emoi.jpg',img)
        # print('user_bot.roiLandmarks', user_bot.roiLandmarks)
        try:
            landmark=self.landmarker.run(img)
        except Exception as e:
            landmark=[]
            print('landmark landmark error',e)
            pass
        if len(landmark)==0:
            src_points = np.array(user_bot.roiLandmarks, 'int32')
        else:
            print('emoi roi landmark',landmark[0])
            src_points = np.array(landmark[0], 'int32')

        # img = cv2.resize(img, (img.shape[1] + 1-(img.shape[1] % 2), img.shape[0] + 1-(img.shape[0] % 2)))
        # mor_img, mask_img = CVTools.morph_mouth_close(img, src_points, img, src_points)
        mor_img, mask_img = CVTools.morph_mouth_close(img, src_points)
        mor_img = np.array(mor_img, img.dtype)
        mask_img = np.array(mask_img, img.dtype)
        # cv2.imwrite('morimg.jpg', mor_img)
        # cv2.imwrite('mask_img.jpg',mask_img)
        result = np.where(mask_img == 255, mor_img, img)

        return result

    def talkOnce(self, user_bot):
        # cv2.imwrite('talkonce.jpg',user_bot.emoi)
        morphImg = self.morph(user_bot)
        if self.debug:
            cv2.imwrite('tomorphImg.jpg', morphImg)
        user_bot.talkPic = [morphImg, morphImg,
                                morphImg, user_bot.emoi,
                                morphImg, user_bot.emoi,
                                morphImg, user_bot.emoi]

    def printText(self, user_bot,sentenceList):
        id = max(user_bot.emoiWordsArea.keys())
        left, top, width, height = user_bot.emoiWordsArea[id]
        imgList = []

        for text in sentenceList:

            text = text.replace("#username#", user_bot.userName)
            # print('text',text,(left,top),user_bot.emoi.shape)
            for index, talkPic in enumerate(user_bot.talkPic):
                if index < 2:
                    imgList.append(talkPic)
                else:
                    imgList.append(CVTools.drawText(talkPic, text, (left, top), 20))
        # cv2.imwrite('emoi.jpg',user_bot.emoi)
        return imgList

if __name__=='__main__':
    from landmarkModule import landmarker
    import botClass
    bb=botClass.bot()
    bb.imgPath='pic/25033812051166452013.jpg'
    landmarker=landmarker(False)
    em=emoi_movie_module('data/emoi/','pic/',landmarker,True)
    bb=em.run(bb,['没有伤悲就不会有慈悲。'],1,'gif')
```

#  5. 被打胖视频movieModule.py

1.首先，生成人脸变胖的图片：

——1.1 对用户发的图像进行人脸识别，获取人脸特征点

——1.2 使用类似瘦脸算法反向胖脸，参数可以根据之前emotion的检测到的强度来调节。卡通图真人图都可以，关键前一步拿较好的图片来识别人脸特征点。

![](https://ai-studio-static-online.cdn.bcebos.com/c2e28a1a642248b9a71311fe8c4361892a209669c7a646cc8c6998ec07fc17fc)
![](https://ai-studio-static-online.cdn.bcebos.com/7e4f8bcd25a64fb8a1bdd6d9e451a5a1bb6ee4c7879440a2b96bb10e26dc3ec0)


——1.3 与几张手掌的png进行前后景融合，生成掌刮的图

![](https://ai-studio-static-online.cdn.bcebos.com/92ff2a4075324b51a0c132282fe603bb058915a9427840aa9aaff495b03778ef)


——1.4利用上述生成的图片，用imageio或moviepy生成gif或视频mp4

# C. 运行

## 1.用wechaty框架完整运行本项目：

1.在一台云服务器上，docker pull wechaty_puppet_service_token_gateway的镜像。记得设定一个自己的唯一id，然后运行wechaty的docker：
```
export WECHATY_LOG="verbose"
export WECHATY_PUPPET="wechaty-puppet-wechat"
export WECHATY_PUPPET_SERVER_PORT="8080"
export WECHATY_TOKEN="your_write_id_what_you_like"#自定义的唯一id

docker run -ti \
--name wechaty_puppet_service_token_gateway \
--rm \
-e WECHATY_LOG \
-e WECHATY_PUPPET \
-e WECHATY_PUPPET_SERVER_PORT \
-e WECHATY_TOKEN \
-p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" \
wechaty/wechaty:latest
```


2. 下载本项目中的压缩包（里面包含有所的了，不用管压缩包外的脚本，那些只是用于给看aistudio的来查阅），解压所有文件到aistudio的脚本任务中或一台比较好的服务器上（可以与docker那台一样，也可不一样）。文件结构不要变



3. 在这台较好的服务器或aistudio的脚本任务上，修改run.sh中的

WECHATY_PUPPET_SERVICE_TOKEN为wechaty中拿到的token ，修改 WECHATY_PUPPET_SERVICE_TOKEN为刚刚定义的唯一id：

```
export WECHATY_PUPPET_SERVICE_TOKEN="puppet_padlocal_you_get_from_wechaty"

WECHATY_PUPPET_SERVICE_TOKEN=your_write_id_what_you_like#自定义的唯一id
```


4. 配置你的环境为python3.7，输入sh run.sh运行即可

## 2.只参考使用本项目多轮聊天模块：

1.可直接接入botprocess.py的返回，返回的是一个都是一个bot的对象及回复的内容，回复内容以字典形式，key为类型，value为图片视频文件路径或回复的文本

2.可能一次回复会有几项内容，数目为replys_index的值。当其不为0时，循环去run就好，可参考run_bot.py

3.给到botprocess的需要稍微封装一下，也可参考run_bot.py

# D.总结

1. 因时间较赶，未用上状态机进行聊天机器人的情景设置。若关注start或fork的人有兴趣可留言，后面更新此功能。只需xmind中设置流程图，文件导入到程序，就可实现多场景无需写代码就实现自己的多轮聊天机器人

2. 希望大家若觉得不错可多多start或fork，支持一下，正在比赛中 哈~~

3. 最后感谢党、感谢祖国、感谢Paddlehub、感谢Wechaty的支持
