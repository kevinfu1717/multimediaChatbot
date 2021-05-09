import cv2
import numpy as np
import CVTools

def ProcessPoints(dst_points):  # 拉开 dlib/paddle 68脸部landmark中，嘴唇眼镜上下部分重合的点

    eyepairs = [(37, 41), (38, 40), (43, 47), (44, 46)]  # 从0开始  #Add(50, 61), (51, 62), (52, 63)
    # 调节上下嘴唇的顺序不反过来
    slipUpperpairs = [(50, 61), (51, 62), (52, 63)]
    slippairs = [(61, 67), (62, 66), (63, 65)]
    slipDownpairs = [(67, 58), (66, 57), (65, 56)]
    facepairs = [(0, 16), (1, 15)]
    centers = 29
    # a会往上下移动点，与b只往下移点 调用顺序不能反了

    limit = 4
    for pp in slippairs:
        #            print('dst_points',dst_points[pp[0]][1],dst_points[pp[1]][1])
        dy = dst_points[pp[1]][1] - dst_points[pp[0]][1]
        ##上下反了
        if dy <= 0:
            avr = int((dst_points[pp[0]][1] + dst_points[pp[1]][1]) / 2)
            dst_points[pp[0]] = (dst_points[pp[0]][0], avr)  # shift one pixel in y direction   #origin -1 -2 0 +2
            dst_points[pp[1]] = (dst_points[pp[1]][0], avr + limit)  # shift one pixel in y direction
        # 上下点贴得太靠近
        elif dy < limit:  # origin 1
            dst_points[pp[0]] = (
            dst_points[pp[0]][0], dst_points[pp[0]][1])  # shift one pixel in y direction  #origin 0 -2 0 +1
            dst_points[pp[1]] = (
            dst_points[pp[1]][0], dst_points[pp[1]][1] + (limit - dy))  # shift one pixel in y direction

    limit = 8
    for pp in (slipUpperpairs):
        #            print('dst_points',dst_points[pp[0]][1],dst_points[pp[1]][1])
        dy = dst_points[pp[1]][1] - dst_points[pp[0]][1]

        ##上下反了
        if dy <= 0:
            avr = (dst_points[pp[0]][1] + dst_points[pp[1]][1]) / 2
            dst_points[pp[0]] = (
            dst_points[pp[0]][0], avr - int(limit))  # shift one pixel in y direction   #origin -1 -2 0 +2
            dst_points[pp[1]] = (dst_points[pp[1]][0], avr)  # shift one pixel in y direction
        # 上下点贴得太靠近
        elif dy < limit:  # origin 1
            dst_points[pp[0]] = (dst_points[pp[0]][0], dst_points[pp[0]][1] - int(
                (limit - dy) / 2))  # shift one pixel in y direction  #origin 0 -2 0 +1
            dst_points[pp[1]] = (dst_points[pp[1]][0], dst_points[pp[1]][1])  # shift one pixel in y direction

    limit = 8  # 以下的点基本不会改动
    for pp in (slipDownpairs):
        #            print('dst_points',dst_points[pp[0]][1],dst_points[pp[1]][1])
        dy = dst_points[pp[1]][1] - dst_points[pp[0]][1]

        ##上下反了
        if dy <= 0:
            avr = (dst_points[pp[0]][1] + dst_points[pp[1]][1]) / 2
            dst_points[pp[0]] = (dst_points[pp[0]][0], avr)  # shift one pixel in y direction   #origin -1 -2 0 +2
            dst_points[pp[1]] = (dst_points[pp[1]][0], avr + int(limit))  # shift one pixel in y direction
        # 上下点贴得太靠近
        elif dy < limit:  # origin 1
            dst_points[pp[0]] = (
            dst_points[pp[0]][0], dst_points[pp[0]][1])  # shift one pixel in y direction  #origin 0 -2 0 +1
            dst_points[pp[1]] = (dst_points[pp[1]][0],
                                 dst_points[pp[1]][1] + int((limit - dy) / 2))  # shift one pixel in y direction

    limit = 2
    # a会往上下移动点，与b只往下移点 调用顺序不能反了
    for pp in (eyepairs):
        #            print('dst_points',dst_points[pp[0]][1],dst_points[pp[1]][1])
        dy = dst_points[pp[1]][1] - dst_points[pp[0]][1]
        ##上下反了
        if dy <= 0:
            avr = (dst_points[pp[0]][1] + dst_points[pp[1]][1]) / 2
            dst_points[pp[0]] = (
            dst_points[pp[0]][0], avr - int(limit / 2))  # shift one pixel in y direction   #origin -1 -2 0 +2
            dst_points[pp[1]] = (dst_points[pp[1]][0], avr + int(limit / 2))  # shift one pixel in y direction
        # 上下点贴得太靠近
        elif dy < limit:  # origin 1
            dst_points[pp[0]] = (dst_points[pp[0]][0], dst_points[pp[0]][1] - int(
                limit / 2))  # shift one pixel in y direction  #origin 0 -2 0 +1
            dst_points[pp[1]] = (
            dst_points[pp[1]][0], dst_points[pp[1]][1] + int(limit / 2))  # shift one pixel in y direction
    # b仅往下移动点

    return dst_points

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
