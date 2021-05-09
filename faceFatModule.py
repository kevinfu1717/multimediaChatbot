import paddlehub as hub

import cv2
import numpy as np
import math
import CVTools
face_landmark = hub.Module(name="face_landmark_localization")


def landmark_dec_fun(img_src):
    # img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    #
    land_marks = []
    #
    # rects = detector(img_gray, 0)

    # for i in range(len(rects)):
    #
    #     land_marks.append(land_marks_node)
    results = face_landmark.keypoint_detection(images=[img_src],
                                                    paths=None,
                                                    batch_size=1,
                                                    use_gpu=False,
                                                    output_dir='face_landmark_output',
                                                    visualization=False)
    # print('emoi baidu landmark',len(results),len(results[0]))
    for result in results:  # one result for one pic
        # print(len(result['data']))
        land_marks.append(result['data'])
    return land_marks[0]#one pic for one element


'''
方法： Interactive Image Warping 局部平移算法
'''

def localTranslationWarp(srcImg, startX, startY, endX, endY, radius):
    ddradius = float(radius * radius)
    copyImg = np.zeros(srcImg.shape, np.uint8)
    copyImg = srcImg.copy()

    # 计算公式中的|m-c|^2
    ddmc = (endX - startX) * (endX - startX) + (endY - startY) * (endY - startY)
    H, W, C = srcImg.shape
    for i in range(W):
        for j in range(H):
            # 计算该点是否在形变圆的范围之内
            # 优化，第一步，直接判断是会在（startX,startY)的矩阵框中
            if math.fabs(i - startX) > radius and math.fabs(j - startY) > radius:
                continue

            distance = (i - startX) * (i - startX) + (j - startY) * (j - startY)

            if (distance < ddradius):
                # 计算出（i,j）坐标的原坐标
                # 计算公式中右边平方号里的部分
                ratio = (ddradius - distance) / (ddradius - distance + ddmc)
                ratio = ratio * ratio

                # 映射原位置
                UX = i - ratio * (endX - startX)
                UY = j - ratio * (endY - startY)

                # 根据双线性插值法得到UX，UY的值
                value = BilinearInsert(srcImg, UX, UY)
                # 改变当前 i ，j的值
                copyImg[j, i] = value

    return copyImg


def translationFaceWarp(srcImg, startX, startY, endX, endY, radius):
    ddradius = float(radius * radius)
    copyImg = np.zeros(srcImg.shape, np.uint8)
    copyImg = srcImg.copy()

    # 计算公式中的|m-c|^2
    ddmc = (endX - startX) * (endX - startX) + (endY - startY) * (endY - startY)
    H, W, C = srcImg.shape
    for i in range(W):
        for j in range(H):
            # 计算该点是否在形变圆的范围之内
            # 优化，第一步，直接判断是会在（startX,startY)的矩阵框中
            if math.fabs(i - startX) > radius and math.fabs(j - startY) > radius:
                continue

            distance = (i - startX) * (i - startX) + (j - startY) * (j - startY)

            if (distance < ddradius):
                # 计算出（i,j）坐标的原坐标
                # 计算公式中右边平方号里的部分
                ratio = (ddradius - distance) / (ddradius - distance + ddmc)
                ratio = ratio * ratio

                # 映射原位置
                UX = i + ratio * (endX - startX)
                UY = j + ratio * (endY - startY)

                # 根据双线性插值法得到UX，UY的值
                value = BilinearInsert(srcImg, UX, UY)
                # 改变当前 i ，j的值
                copyImg[j, i] = value

    return copyImg


# 双线性插值法
def BilinearInsert(src, ux, uy):
    w, h, c = src.shape
    if c == 3:
        x1 = int(ux)
        x2 = x1 + 1
        y1 = int(uy)
        y2 = y1 + 1

        part1 = src[y1, x1].astype(np.float) * (float(x2) - ux) * (float(y2) - uy)
        part2 = src[y1, x2].astype(np.float) * (ux - float(x1)) * (float(y2) - uy)
        part3 = src[y2, x1].astype(np.float) * (float(x2) - ux) * (uy - float(y1))
        part4 = src[y2, x2].astype(np.float) * (ux - float(x1)) * (uy - float(y1))

        insertValue = part1 + part2 + part3 + part4

        return insertValue.astype(np.int8)

def find_biggest_face(landmarks):
    areaList=[]
    for landmark in landmarks:
        lan=np.array(landmark)
        areaList.append(np.max(lan)*np.min(lan))
    print('areaList',areaList)
    index=areaList.index(max(areaList))
    index=0
    return landmarks[index]

def swap_face(src,landmarks_node,ratio=0.8):
    left_landmark = landmarks_node[3]
    left_landmark_down = landmarks_node[31]

    right_landmark = landmarks_node[13]
    right_landmark_down = landmarks_node[31]

    endPtleft = landmarks_node[33]
    endPtright = landmarks_node[33]

    # 计算第4个点到第6个点的距离作为瘦脸距离
    r_left = math.sqrt(
        (left_landmark[0] - left_landmark_down[0]) * (left_landmark[0] - left_landmark_down[0]) +
        (left_landmark[1] - left_landmark_down[1]) * (left_landmark[1] - left_landmark_down[1]))

    # 计算第14个点到第16个点的距离作为瘦脸距离
    r_right = math.sqrt(
        (right_landmark[0] - right_landmark_down[0]) * (right_landmark[0] - right_landmark_down[0]) +
        (right_landmark[1] - right_landmark_down[1]) * (right_landmark[1] - right_landmark_down[1]))
    r_right *=( max(0.8,ratio)+0)
    r_left *=( max(0.8,ratio)+0)
    print(r_right, r_left)
    # 瘦左边脸
    thin_image = translationFaceWarp(src, left_landmark[0], left_landmark[1], endPtleft[0],
                                       endPtleft[1], r_left)
    # thin_image = localWiderWarp(src, left_landmark[ 0], left_landmark[ 1],
    #                             (endPtleft[ 0]+left_landmark[ 0])/2, (left_landmark[ 1]+endPtleft[ 1])/2,
    #                                   r_left)
    # 瘦右边脸
    thin_image = translationFaceWarp(thin_image, right_landmark[0], right_landmark[1], endPtright[0],
                                       endPtright[1], r_right)
    # thin_image = localWiderWarp(thin_image, right_landmark[ 0], right_landmark[ 1],
    #                             (endPtright[ 0]+right_landmark[ 0])/2, (right_landmark[ 1]+endPtright[ 1])/2,
    #                                   r_left)
    return thin_image

class face_morph():
    def __init__(self,landmarker,cartoon_maker):
        self.landmarker=landmarker
        self.cartoon_maker=cartoon_maker
        self.perspect_size=256
    def run(self,user_bot=None,src_img=[],morph_img=[]):
        landmark=[]


        # user_bot.roiImg
        if len(src_img)!=0:
            landmarks = self.landmarker.run(src_img)
        else:
            img=cv2.imread(user_bot.imgPath)
            landmarks = self.landmarker.run(img)


        # 如果未检测到人脸关键点，就不进行瘦脸
        if len(landmarks) == 0:
            return user_bot
        landmarks_node=find_biggest_face(landmarks)

        ratio=user_bot.emoitionRatio

        # for landmarks_node in landmarks:
        if user_bot is not None:

            morph_image = swap_face(img, landmarks_node, ratio)
            # landmarks_node=np.array(landmarks_node)
            inputImg = CVTools.roiChoice([landmarks_node], morph_image, self.perspect_size)

            morph_image=self.cartoon_maker.process(inputImg)
        else:
            if len(morph_img)!=0:
                inputImg=morph_img
            else:
                inputImg=src_img
            morph_image = swap_face(inputImg, landmarks_node, ratio)

        # print(cv2.imwrite('roi.jpg',user_bot.roiImg))
        # print(cv2.imwrite('inputImg.jpg',inputImg))

    ##
        if user_bot is not None:
            user_bot.specialImg=morph_image
            return user_bot
        else:
            return morph_image
    # 显示
    # cv2.imshow('thin', thin_image)
    # cv2.imwrite('thin.jpg', thin_image)
    # cv2.imwrite('mask.jpg',mask)


if __name__=='__main__':
    from landmarkModule import landmarker
    from cartonModule import  cartoon_face

    la=landmarker(False)
    cm = cartoon_face(la)
    cf=face_morph(la,cm)
    src_img=cv2.imread('roi.jpg')
    from botClass import bot
    user_bot=bot()
    user_bot.imgPath='pic/25033812051166452013.jpg'
    # user_bot.roiCartoon=cv2.imread('inputImg.jpg')
    out=cf.run(user_bot)
    # print('in',image.shape,'out',out.shape)
    # cv2.imwrite('../facefatter.jpg', out.specialImg)
    # print('time', time.time() - t1)

    #
    # src = cv2.imread('a10.png')[:,:,:3]
    # src = cv2.imread('wuyifan.jpg')[:,:,:3]
    #
    # face_thin_auto(src)