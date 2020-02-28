import time
import requests
import json,os,re,threading

class BiliPicture:
    def __init__(self,frame,q):
        self.uid = frame.IUid.GetValue()
        self.frame = frame # 窗口对象
        self.q=q # 线程通信

    # 给标签获取内容
    def setContent(self,text):
        self.frame.TContent.SetLabel(text)

    # 设置进度
    def setprogress(self,value):
        self.frame.PNow.SetValue(value)

    # 开始下载
    def start(self):
        self.setContent("开始获取数据")
        page=0
        imglist=[]
        while self.q.empty():
            url="https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?uid="+self.uid+"&page_num="+str(page)+"&page_size=30&biz=all"
            page+=1
            response=requests.get(url,timeout=4).text
            try:
                lists=json.loads(response)
                imglist+=lists["data"]["items"]
                self.setContent("获取到"+str(len(imglist))+"条数据")
                if len(lists["data"]["items"])==0:
                    break
            except:
                self.setContent("获取数据失败")
        # 提取下载链接
        srclist=[]
        for img in imglist:
            for item in img["pictures"]:
                srclist.append(item["img_src"])
        self.setContent("提取到"+str(len(srclist))+"条下载链接")

        # 开始下载图片(创建文件夹)
        if not os.path.exists("imgs"):
            os.makedirs("imgs")

        # 多线程下载图片
        treads=[]
        for i in range(len(srclist)):
            if self.q.empty():
                # 进行延时避免被B站封ip
                time.sleep(0.5)
                self.setContent("正在下载第"+str(i)+"张图片(共张"+str(len(srclist))+"图片)")
                self.setprogress((i/len(srclist))*100)
                td=threading.Thread(target=self.download,args=(srclist[i],"imgs/"+str(i)+"."+self.getdot(srclist[i]),))
                td.start()
                treads.append(td)

        # 等待多线程退出
        self.setContent("等待图片全部下载完成。。。。")
        for item in treads:
            item.join()
        # 显示下载完成
        self.setprogress(100)
        self.setContent("下载完成！请到当前软件路径下的imgs文件夹查看")
        self.frame.BStart.SetLabel("开始爬取")


    # 下载图片
    def download(self,src,path):
        r = requests.get(src, stream=True)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=32):
                f.write(chunk)

    # 获取文件后缀
    def getdot(self,src):
        return re.search(".([a-z|A-Z]*?)$",src).group(1)



    def Stop(self):
        print(self.uid)
