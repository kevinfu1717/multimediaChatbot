
from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np
import moviepy.video.io.ImageSequenceClip
import time
from triangulation import measure_triangle, affine_triangle, morph_triangle
def saveGif(imgList,outputPath,fps=4):
    import imageio
    frames=[cv2.cvtColor(img,cv2.COLOR_BGR2RGB) for img in imgList]
    imageio.mimsave(outputPath+'dt.gif', frames, 'GIF', duration=1/fps)
def combineImg(front,background,pos,flip):
    if flip<2:
        front=cv2.flip(front,flip)
    x,y=pos
    height,width=front.shape[:2]
    mask=np.zeros((front.shape[0],front.shape[1],3),front.dtype)
    mask[:,:,0]=front[:,:,3]
    mask[:,:,1]=front[:,:,3]
    mask[:, :, 2] = front[:, :, 3]
    img=front[:,:,:3]
    result=background.copy()
    x1=max(0,int(x-width/2))
    x2=min(int(x+width/2),background.shape[1])
    y1=max(0,int(y-height/2))
    y2=min(int(y+height/2),background.shape[0])
    print(img[:y2-y1,:x2-x1,:].shape,result[y1:y2,x1:x2,:].shape,mask[:y2-y1,:x2-x1,:].shape)
    result[y1:y2,x1:x2,:]=\
        np.where(mask[:y2-y1,:x2-x1,:]>50,img[:y2-y1,:x2-x1,:],result[y1:y2,x1:x2,:])
    return result


def drawText(img,text,position,fontSize):
    ## Use simsum.ttc to write Chinese.
    fontpath = "resource/kaiu.ttf"  # <== 这里是宋体路径
    # fontpath= u"simsun.ttc"
    font = ImageFont.truetype(fontpath, fontSize)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=(0, 0, 0,0))
    img = np.array(img_pil)
    # cv2.imwrite('drawtext.jpg',img)
    return img

def morph_mouth_close1( src_img, src_points, dst_img, dst_points, alpha=1):
    morph_points = []
    res_img = -1 * np.ones(src_img.shape, src_img.dtype)
    #    cv2.imshow('src_img',src_img)
    #    cv2.imshow('dst_img',dst_img)
    # print('src_img',src_img)
    src_img = src_img.astype(np.float32)
    dst_img = dst_img.astype(np.float32)
    # print('src_imgxx',src_img)

    #    cv2.imshow('src_imgssss',src_img)
    #    cv2.imshow('dst_imgssss',dst_img)
    #    cv2.waitKey(0)

    #        alpha = 0.8
    beginPoint=48#只调嘴
    for i in range(beginPoint, len(src_points)):
        x = (1 - alpha) * src_points[i][0] + alpha * dst_points[i][0]
        y = (1 - alpha) * src_points[i][1] + alpha * dst_points[i][1]
        morph_points.append((x, y))
    ##

    dt = measure_triangle(src_img, morph_points)
    alpha = 0.75
    for i in range(0, len(dt)):
        t1 = []
        t2 = []
        t = []

        for j in range(0, 3):
            t1.append(src_points[dt[i][j]])
            t2.append(dst_points[dt[i][j]])
            t.append(morph_points[dt[i][j]])
        # print( t)
        morph_triangle(src_img, dst_img, res_img, t1, t2, t, alpha)
        ##调试时打开
    #        self.DebugOutput(res_img,src_img,dst_points,src_points)

    mask_img=np.where(res_img==-1,0,255)
    res_img=mask_img.copy()
    res_img=np.array(res_img,dtype='uint8')
    # print('res_img',res_img.shape,np.max(res_img))
    mouthh = int((src_points[56, 1] + src_points[58, 1] - src_points[50, 1] - src_points[52, 1]) /5)
    res_img=cv2.line(res_img,(src_points[48][0],src_points[48][1]),
                     (src_points[54][0],src_points[54][1]),[0,0,0],thickness=mouthh)

    return res_img,mask_img
def morph_mouth_close( src_img, src_points):
    morph_points = []
    res_img =np.array(255*np.ones(src_img.shape), src_img.dtype)
    mask_img=np.zeros(src_img.shape, src_img.dtype)
    # src_img=np.array(src_img,dtype=np.uint8)[:,:,0]


    mask_img=cv2.fillConvexPoly(mask_img, src_points[48:60,:], (255, 255, 255))
    arr=np.sum(mask_img[:,:,0],axis=1)
    beginH=(arr!=0).argmax(axis=0)
    arr=np.flipud(arr)
    endH=len(arr)-(arr!=0).argmax(axis=0)
    mouthh = int((endH-beginH)/4)
    # cv2.imwrite(str(mouthh)+'res_img.jpg', res_img)
    res_img=cv2.line(res_img,(src_points[48][0],src_points[48][1]),
                     (src_points[54][0],src_points[54][1]),[0,0,0],thickness=mouthh)
    # cv2.imwrite('res_img1.jpg', res_img)
    res_img=np.where(mask_img>0,res_img,src_img)
    return res_img,mask_img
def roiChoice(landmarks,img,perspect_size):
    if img.shape[0] >= 256 and img.shape[1] >= 256:
        area = []
        mid_x = []
        mid_y = []
        width = []
        height = []
        for ii, landmark in enumerate(landmarks):
            landmark_array = np.array(landmark)
            width.append(np.max(landmark_array[:, 0]) - np.min(landmark_array[:, 0]))
            height.append(np.max(landmark_array[:, 1]) - np.min(landmark_array[:, 1]))
            mid_x.append(int((np.max(landmark_array[:, 0]) + np.min(landmark_array[:, 0])) / 2))
            mid_y.append(int((np.max(landmark_array[:, 1]) + np.min(landmark_array[:, 1])) / 2))
            area.append(width[ii] * height[ii])
        index = area.index(max(area))
        ratio = 256 / 3 / width[index]  ## 1/3 width of pic may seen look better
        roi_img = cv2.resize(img, (0, 0), fx=ratio, fy=ratio)
        landmark = landmarks[index]
        mid_x = mid_x[index]
        mid_y = mid_y[index]
        x_begin = max(0, int(ratio * mid_x - 128))
        x_end = min(roi_img.shape[1], int(perspect_size - (ratio * mid_x - x_begin) + ratio * mid_x))
        y_begin = max(0, int(ratio * mid_y - 128))
        y_end = min(roi_img.shape[0], int(perspect_size - (ratio * mid_y - y_begin) + ratio * mid_y))
        roi_img = roi_img[y_begin:y_end, x_begin:x_end, :]
    else:
        roi_img = cv2.resize(img, (256, int(img.shape[0] * 256 / img.shape[1])))
    return roi_img

def makeMovie(imgList,outputPath='',fps=4):

    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(imgList, fps=fps)
    path=outputPath+'video'+str(time.time())+'.mp4'
    clip.write_videofile(path)
    return path