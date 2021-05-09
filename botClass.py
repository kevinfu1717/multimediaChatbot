from collections import deque
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
if __name__=="__main__":
    bb=bot()
    print(type(bb.stepRecord))