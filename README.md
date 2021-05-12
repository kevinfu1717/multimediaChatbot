# Paddlehub+Wechaty微信聊天机器人--多轮情景吐槽,emoi及打肿脸视频动态实时生成并回复

## 项目描述
构建了可用于多个对话框架的场景型对话的聊天机器人。支持吐槽类情景及情感倾诉型情景。使用wechaty，结合Paddlehub的人脸特征点、动漫人脸生成、对联生成、情感分类，ernie迁移，人脸变胖

## 项目结构
```
-|data
-|resource
-README.MD
```
## 使用方式
A：在AI Studio的脚本任务上[运行本项目](https://aistudio.baidu.com/aistudio/projectdetail/1904532?shared=1)
B：在配置比较好的服务器上运行

#  吐槽树洞——让机器人陪你一起吐槽、倾诉

效果可见b站视频(建议右键新建窗口打开）: [b站视频](https://www.bilibili.com/video/BV1nA41157i2?share_source=copy_web)

# A.摘要

##  1.功能简介

本项目构建了一个用于场景型多轮对话，这里可用于让人们吐槽（图嘈）发泄，以及情感倾诉。根据对话内容，分析对话者是情感倾诉还是要吐槽发泄，会进入多轮对话文本、爬虫获取信息、卡通人脸生成、吐槽对称句生成、变胖人脸生成、情话生成、动态个性化表情动图生成、视频合成等多模块组合到一个聊天模块下，可方便根据聊天情景快速切换到自己的场景使用

本项目中对话为特定情景下的引导性对话，非开放性闲聊对话。但多资源反馈部分，也可以接入开放性闲聊对话，增加对话乐趣。

##  2.整体流程



| 序号 | 内容 | 简述 |
| -------- | -------- | -------- |
| 1     | 经Wechaty获取用户输入    | 定义用户输入的内容，进行触发，并判断用户输入内容是图片还是文本进行encode给到机器人框架    |
|2     | 基于机器人框架获取用户信息并获取回复内容  |根据设定的多轮逻辑，及当前用户信息及回复阶段，获得应回复的内容     |
| 3    | 基于回复内容调用各技能模块     | 回复逻辑已预设好回复的多媒体类别，进行decode后调用各模块  |
|4     | 各生成模块生成文件或文本    | 各模块的模型根据当前的用户信息，生成动图、视频、文本等个性化回复内容。各模块见A-3     |
| 5     | 机器人框架载入这些文件或文本     | 进行汇总，可以一次回复包含多个或多类别内容   |
| 6     | 通过Wechaty回复用户     | 真实发到微信上  |


补充说明：

1 botProces中的bot_manager使用类似“简易工厂模式”。（熟悉工厂模式的筒子可以忽略本段）。每一个触发聊天的用户都会生成一个user_bot,用户的输入就好像工厂里面的原材料，经过bot_manager分配到各个工序的工人(各个技能模块，如：卡通人脸生成、爬虫、变胖人脸等）进行处理，最终组装好的产品给到用户。不同用户的输入就像不同的原材料，不断送进工厂处理，流水的bot铁打不变的bot_manager，而每个user_bot装载的是整个聊天过程中的所有对话。以上纯属个人胡扯，工厂模式正规解释具体见：[https://www.cnblogs.com/wly923/archive/2013/05/10/3068313.html](http://https://www.cnblogs.com/wly923/archive/2013/05/10/3068313.html)

2 talkProcess中会把botProcess中返回的对话内容，“翻译”成真正发给用户的内容。例如：是文本的直接返回，要生成cartoon图的将调用卡通图生成模块生成，要生成被打肿了的脸的则调对应的模块生成视频，然后把资源地址给到botmanger，botManger再读取文件发动图、表情gif或视频给用户。


##  3.各模块单独效果及简介

调用Paddlehub来丰富chatbot的技能，直接使用或自己的算法结合Paddlehub模型来使用：




| 序号 | 模块 | 简介 |  效果 | 主要脚本 |调用的Paddlehub模型 |
| ---- | -------- | -------- | -------- | ------------ | ----------------- |
| 3.1 | 情感分类<br>模块     | 获取用户输入内容的情感倾向及程度（置信度） |       | emotionModule.py      |结合emotion_detection_textcnn<br>模型      |
| 3.2 | 漫画人脸<br>生成     | 调整图片尺寸或增加图片的纹理复杂度，<br>中值滤波，再卡通生成（不然脸上会很花） |  ![](https://ai-studio-static-online.cdn.bcebos.com/e509e94f3b9c4482b7b2c8806d10dd29e54aba4bfc3f47d19f50b1b0b39888cb)    | cartonModule.py    | 结合AnimeGan模型      |
| 3.3 | 对偶句生成     | 根据用户的吐槽语句，生成吐槽的语句 |     | coupletModule.py      |  ernie_gen_couplet/ernie_gen<br>模型     |
| 3.4 | 情话生成     | 根据用户的倾诉,生成一些情话，安抚用户 |      | loveModule.py     |ernie_gen_lover_words模型     | 
| 3.5 | 人脸特征点     | 在多个人脸变形或口型或换脸中使用 |   ![](https://ai-studio-static-online.cdn.bcebos.com/62ffe830a6fa40a1a99ed53229fb1dcd58fc691948e6496d8473510039c1ac58)  |landmarkModule.py     | face_landmark_localization模型     |
| 3.6 | 百度爬虫     | 爬取用户想要吐槽对象的图片或相关信息 |     |crawlerModule.py     |  自己弄     |  
| 3.7 | 人脸变胖     | 使用类似瘦脸的反向算法，让人变成胖子 |  ![](https://ai-studio-static-online.cdn.bcebos.com/53d0ffe790a84d768c43dee3aa538b1ef105e7ee47514c15b83fb9857bf76222) | faceFatModule.py     | 自己弄   |
| 3.8 | 人脸五官迁<br>移到动态<br>表情包     | 1.下载网上一些表情，用Paddlehub的ocr截<br>取文字内容及区域<br>2.提取吐槽对象的人脸的五官并得到二值<br>化的黑白五官<br>3.该五官与表情包原来的五官进行对齐，<br>并替换原来的五官<br>4.基于新的五官生成闭嘴的图，与原开口的图<br>组合起来成gif或视频<br>5.在原来文字的位置写上新的吐槽语句 |![](https://ai-studio-static-online.cdn.bcebos.com/268d1cbd3026461d95d60d0a5cfda9eb2b7a1caea5e34dfd9305fc2e233e4cf9)      | emoiModule.py     |  自己弄     |
| 3.9 | 视频/动图<br>生成     |使用类似瘦脸的反向算法，让人变成胖子 |      |movieModule.py    |  自己弄    | 
| 3.10 | 词向量匹配     | 1.我收集了吐槽大会的几百句经典语录。<br>2.对经典吐槽语句的句子的n系列词性的词组<br>建立句子vector向量库<br>3.对用户的输入句子进行相似计算，<br>匹配相似度高的经典吐槽语录。 |  还记得你之前跟我说，我能及格猪都能上树。<br>可教练我拿到驾照了，猪不仅能上树还能上高速<br>，我再给你来个倒车入库，压线了难受不？<br>以前我不敢顶撞你，现在顶撞你可抗不住。    | roastModule.py     |  w2v_weibo_target_word-word_<br>dim300词向量     |
| 3.11 | 微信机器人<br>框架   | 现在唯一还可用的微信聊天机器人框架Wechaty |     | run_bot.py     |  Wechaty     | 



    

# B. 主要功能脚本简述（只介绍部分代码，具体请参见项目内脚本）

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


#  5. 被打胖视频movieModule.py

1.首先，生成人脸变胖的图片：

——1.1 对用户发的图像进行人脸识别，获取人脸特征点

——1.2 使用类似瘦脸算法反向胖脸，参数可以根据之前emotion的检测到的强度来调节。卡通图真人图都可以，关键前一步拿较好的图片来识别人脸特征点。

![](https://ai-studio-static-online.cdn.bcebos.com/c2e28a1a642248b9a71311fe8c4361892a209669c7a646cc8c6998ec07fc17fc)
![](https://ai-studio-static-online.cdn.bcebos.com/7e4f8bcd25a64fb8a1bdd6d9e451a5a1bb6ee4c7879440a2b96bb10e26dc3ec0)


——1.3 与几张手掌的png进行前后景融合，生成掌刮的图

![](https://ai-studio-static-online.cdn.bcebos.com/92ff2a4075324b51a0c132282fe603bb058915a9427840aa9aaff495b03778ef)


——1.4利用上述生成的图片，用imageio或moviepy生成gif或视频mp4

## 6 人脸动漫化

AnimeGan可能训练的数据中，人脸特写的比较少。当遇到人脸特写或人脸所占像素较大时，且人脸光影比较明显时，会生成的人脸上很多一道道的线条。（像某个生成的李云龙那样）

所以，需要对图片进行预处理再生成，下面左图为直接生成，右图为缩小人脸分辨率，并进行磨皮，之后再加背景图增加纹理后再生成

![](https://ai-studio-static-online.cdn.bcebos.com/9cf64cc3747c435c9b7dfbbf26924f8df4c6d28b64194fde9bc09d962b8daaea)
![](https://ai-studio-static-online.cdn.bcebos.com/24b4173d905143939dc766899dad08f186600f5284ef47c494a4a28ef313c045)

增加纹路的操作如下：
把图贴到复杂的背景图上去生成漫画化，最后再截取原来我们需要的部分

![](https://ai-studio-static-online.cdn.bcebos.com/554d571ce84647d7978b61a8afabdce9982aa0f61091470180f700de3588710a)

但本项目中，无需这么复杂，只需：

1.截取人脸附近位置

2.调整截取图片分辨率到256像素左右

3.再均值滤波

4.调用AnimeGan生成即可

**详见cartonModule.py**



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

4.本项目参考了细菌,GT的项目，在此表示感谢

