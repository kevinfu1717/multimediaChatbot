# 百度爬取'福'的图片
# 参考https://blog.csdn.net/qq_45880822/article/details/109872504
import requests
import re
import os

class pic_crawler():
##
    def __init__(self,outputPatn):

        pages = 1  ##看我们要下多少页的数据
        self.pages_1 = int(pages)+1
        self.outputPath=outputPatn
        self.crawlNum=1

    # 图片爬取函数
    def run(self,search_words=''):
        search_words=search_words+' 正脸照 半身'
        print('search word',search_words)
        if len(search_words)==0:return []
        result = []
        for page in range(1, self.pages_1):
            url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={}&pn={}'.format(search_words, page)
            # url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1600582955784_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word=%E9%81%93%E8%B7%AF%E7%A6%81%E6%AD%A2%E8%B7%AF%E6%A0%87'
            # 伪装浏览器请求头
            headers = {
                'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 84.0 .4147.89Safari / 537.36'
            }

            # 获取网站源码
            html = requests.get(url, headers=headers)
            # 获取真实的url
            urls_real = re.findall('"thumbURL":"(.*?)",', html.text)
            print('图片url数量', len(urls_real))
            # print(urls_real)
            # 筛选资源url，并返回元组
            # urls = re.findall(r'<img alt="" src="(http://.*?.jpg)" ',html.text)

            # print(urls_real)

            for index,i in enumerate(urls_real):
                if index==self.crawlNum:break
                subname = i.split('/')[-1]  # 资源存放名称 eg:'u=4117662774,1210746205&fm=193'
                filename = re.findall(r"=(.+?)&", subname)[0].replace(',', '')
                path = self.outputPath + filename + '.jpg'  # 资源存放点+资源存放名称
                # print(path)
                image_data = requests.get(i, headers=headers)
                with open(path, 'wb')as f:  # 将图片以二进制写入
                    f.write(image_data.content)
                result.append(path)
        return result
if __name__=='__main__':
    pc=pic_crawler('pic/')
    print(pc.run('特朗普'))