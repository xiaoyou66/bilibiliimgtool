# -*- coding: utf-8 -*-

import queue
import wx
import wx.xrc
from BiliPicture import BiliPicture
import threading

class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"B站壁纸小工具(by:小游)", pos=wx.DefaultPosition,
                          size=wx.Size(283, 139),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        fgSizer2 = wx.FlexGridSizer(3, 3, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"B站uid:", wx.Point(-1, -1), wx.DefaultSize,
                                           wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText4.Wrap(-1)

        fgSizer2.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.IUid = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.IUid, 0, wx.ALL, 5)

        self.BStart = wx.Button(self, wx.ID_ANY, u"开始爬取", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.BStart, 0, wx.ALL, 5)
        bSizer1.Add(fgSizer2, 1, wx.EXPAND, 5)

        self.TContent = wx.StaticText(self, wx.ID_ANY, u"就绪", wx.DefaultPosition, wx.DefaultSize, 0)
        self.TContent.Wrap(-1)

        bSizer1.Add(self.TContent, 0, wx.ALL, 5)

        self.PNow = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.PNow.SetValue(0)
        bSizer1.Add(self.PNow, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def start(self, e):
        self.TContent.SetLabel(self.IUid.GetValue())
        self.PNow.SetValue(50)
        self.BStart.GetLabel()
        self.IUid.GetValue()


# 全局变量
frame = None
tred=None
q = queue.Queue() # 线程通信



def startc():
    global frame,q
    B=BiliPicture(frame,q)
    B.start()


def start(e):
    global frame,q,tred
    if frame.BStart.GetLabel() == '开始爬取':
        if frame.IUid.GetValue()=="":
            frame.TContent.SetLabel("Uid不能为空")
            return
        # 采用多线程来爬取图片
        tred=threading.Thread(target=startc)
        tred.start()
        frame.BStart.SetLabel("取消爬取")
    else:
        q.put("停止")
        tred.join()
        frame.BStart.SetLabel("开始爬取")


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame1(None)
    # 绑定事件并进行处理
    frame.BStart.Bind(wx.EVT_BUTTON, start)
    frame.Show(True)
    # start the applications
    app.MainLoop()

