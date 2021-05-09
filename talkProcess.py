import paddlehub as hub
from loveModule import love_module
from emoiModule import emoi_movie_module
from movieModule import movie_maker
from emotionModule import emotion_module
from crawlerModule import pic_crawler
from  cartonModule import cartoon_face
from landmarkModule import landmarker
from coupletModule import couplet_module
from roastModule import WordVector
import time
import cv2
import numpy as np
class talkManger():
    def __init__(self,outPath='pic/',tempPicPath='pic/',emoi_folder='data/emoi/',debug=False):
        self.splitNum=5
        self.love_module=love_module
        self.couplet_module=couplet_module
        self.landmarker=landmarker()
        self.cartoon_face=cartoon_face(self.landmarker)
        self.word_vector = WordVector()
        self.emoi_movie_maker=emoi_movie_module(emoi_folder, outPath, self.landmarker, debug)


        self.movie_maker=movie_maker(outPath,self.landmarker,self.cartoon_face)
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
            if result['positive_probs']>result['negative_probs'] and result['positive_probs']>result['neutral_probs']:

                userDictBot.emoition='positive'
                userDictBot.emoitionRatio = result['positive_probs']
            else:

                userDictBot.emoition='negative'
                userDictBot.emoitionRatio = max(result['negative_probs'],result['neutral_probs'])


            return userDictBot,{}
        elif package[:self.splitNum] == '#gst#':
            inputs=eval('userDictBot.'+package[self.splitNum:])
            # if package[self.splitNum:]=='abstract':
            #     inputs=userDictBot.abstract
            # elif package[self.splitNum:]=='description':
            #     inputs = userDictBot.description
            result = self.word_vector.simSentence(inputs)
            if len(result)>0:
                userDictBot.ganTextList.append(result)
                return userDictBot, {'str': result}
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
            try:
                inputs = eval('userDictBot.' + package[self.splitNum:])
            except:
                inputs='让我先装个B'
            if userDictBot.emoition == 'positive':
                emotion_flag=1
            else:
                emotion_flag=2
            print('emo inputs',[inputs],emotion_flag)

            userDictBot = self.emoi_movie_maker.run(userDictBot,[inputs],emotion_flag)
            # userDictBot.emoiMoviePath=result
            return userDictBot, {'mov': userDictBot.emoiMoviePath}

        elif package[:self.splitNum] == '#mov#':
            if userDictBot.emoition == 'positive':
                emotion_flag=1
            else:
                emotion_flag = 2
            userDictBot=self.movie_maker.run(userDictBot,emotion_flag)
            return userDictBot, {'mov': userDictBot.moviePath}
