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
        self.replyList=["""”图槽树洞“  这里是一个你可以倾诉对某人的心事，发泄吐槽某人的地方。
        你只需要发你要吐槽的人或想向他/她倾诉的人（on going)的照片或名字就可以开始了。
        我是一个机器人，你不用担心会泄漏出去噢。""",
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

        self.userBotDict[username]=self.addReplys( username, replys)
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
        ##跳出死循环
        if len(self.userBotDict[username].stepRecord)>=self.loopLimit:
            if sum(self.userBotDict[username].stepRecord[-1*self.loopLimit:])== \
                    self.userBotDict[username].stepRecord[-1]**self.loopLimit:
                self.userBotDict[username].step =100
        if self.userBotDict[username].step==0 or self.userBotDict[username].step==7 :

            self.userBotDict[username].param_init()
            print('0000', content)
            replys=["#str#"+self.replyList[0]]
            # print('replys',replys)
            self.userBotDict[username]=self.addReplys( username, replys)
            print('self.userBotDict[username].replys',self.userBotDict[username].replys)
            self.userBotDict[username].step+=1
            # print('self.userBotDict[username].step',self.userBotDict[username].step)
            # print('self.userBotDict[username]',self.userBotDict[username])
            return self.userBotDict[username]
        elif self.userBotDict[username].step==1:##问用户图片

            print('111',content)
            self.userBotDict[username].stepRecord.append(1)
            if content[:self.splitNum]!="#pic#":
                replys=['#str#让我趴他出来哈。。。',
                      '#cra#'+content[self.splitNum:],
                      '#str#是他吗？或者你也可以直接发他的照片？',
                      ]
                self.userBotDict[username]=self.addReplys( username, replys)
                self.userBotDict[username].img=[]

                # self.userBotDict[username] = face_movie.talkGif(self.userBotDict[username])
                # print('talk gif')
                self.userBotDict[username].step+=1
                return self.userBotDict[username]
            else:
                return self.get_target_img(username,content,3)

        elif self.userBotDict[username].step==2:#让用户确认图片
            print('22222')
            self.userBotDict[username].stepRecord.append(2)
            if content[:self.splitNum]!="#pic#":
                if self.userBotDict[username].stepRecord[-2]!=2:##第一次进入确认图片

                    if self.TrueFalse(content[self.splitNum:] ):
                        return self.get_target_img(username,content,3)
                    else:
                        replys=['#str#那请给出他/它更详细的名字，或者可直接发他/它的照片？']
                        self.userBotDict[username]=self.addReplys( username, replys)
                        return self.userBotDict[username]
                else:
                    if self.TrueFalse(content[self.splitNum:] ):
                        return self.get_target_img(username,content,3)
                    else:
                        replys = ['#cra#' + content[self.splitNum:],
                                  '#str#是他吗？或者你也可以直接发他的照片？',
                                  ]
                        self.userBotDict[username]=self.addReplys( username, replys)
                        self.userBotDict[username].img = []
                        return self.userBotDict[username]
            else:#用户直接发图片
                return self.get_target_img(username,content,3)
        elif self.userBotDict[username].step == 3:#已拿到吐槽的对象图片,现在拿描述摘要
            print('33333333')
            self.userBotDict[username].stepRecord.append(3)
            if content[:self.splitNum]=='#str#':
                self.userBotDict[username].abstract=content[self.splitNum:]
                replys=['#cla#'+content[self.splitNum:],'#gim#img',
                      '#str#嗯嗯，看他/她这样，我觉得你说得对，还有吗？']

                self.userBotDict[username].step =4
            else:
                replys=['#str#请用一两句文字描述你想说或想吐的槽吧']
            self.userBotDict[username]=self.addReplys( username, replys)
            return self.userBotDict[username]

        elif self.userBotDict[username].step == 4:#基于对话生成文字
            print('44444')
            self.userBotDict[username].stepRecord.append(4)
            if content[:self.splitNum] == '#str#':
                self.userBotDict[username].description.append( content[self.splitNum:])
                replys=['#str#让我想想','#gst#abstract','#emo#ganTextList[-1]','#str#要不要赏他两巴掌，把他扇成胖子哈']
                self.userBotDict[username].step = 5
            else:
                replys=['#str#请用文字描述你想说或吐槽的吧']
            self.userBotDict[username]=self.addReplys( username, replys)
            return self.userBotDict[username]
        elif self.userBotDict[username].step == 5:#基于对话生成视频
            print('5555')
            self.userBotDict[username].stepRecord.append(5)
            if content[:self.splitNum] == '#str#':
                self.userBotDict[username].description.append( content[self.splitNum:])
                replys=['#str#看我来','#mov#ganImgPath']
                self.userBotDict[username].step = 6
            else:
                replys=['#str#请用文字描述你想说或吐槽的吧']
            self.userBotDict[username]=self.addReplys( username, replys)
            return self.userBotDict[username]
        elif self.userBotDict[username].step == 6:#基于对话生成视频
            print('66666')
            self.userBotDict[username].stepRecord.append(6)
            if content[:self.splitNum] == '#str#':
                self.userBotDict[username].description.append( content[self.splitNum:])

            replys=['#str#好了，我有点困了，下次再聊咯']
            self.userBotDict[username]=self.addReplys( username, replys)
            self.userBotDict[username].step = 7
            return self.userBotDict[username]
        elif self.userBotDict[username].step == 100:#基于对话生成视频
            print('100')
            self.userBotDict[username].stepRecord.append(100)
            if content[:self.splitNum] == '#str#':
                self.userBotDict[username].description.append( content[self.splitNum:])

            replys=['#str#哎，跟你这人类无法交流，我挂了，8']
            self.userBotDict[username]=self.addReplys( username, replys)
            self.userBotDict[username].step = 7
            return self.userBotDict[username]
    def addReplys(self,username,replys):
        self.userBotDict[username].replys_index = len(replys)
        self.userBotDict[username].replys.append(replys)
        return self.userBotDict[username]
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


