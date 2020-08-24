import tkinter
from tkinter import *
import os
import os.path
import tkinter.filedialog
from shutil import copyfile
from pathlib import Path
from tkinter import messagebox
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
class surface():
    def __init__(self):
       self.top = tkinter.Tk()
       self.top.title("文件处理")
       self.top.geometry()
       self.v1 = StringVar()
       self.v2 = StringVar()
       self.v3 = StringVar()
       self.allFile=[]
       self.pathtext=""
       self.check_buttons = list()
       self.allFilePath=[]
       self.PageSize=0
       vart = StringVar()
       vart.set("路径：")
       tkinter.Label(self.top,textvariable=vart,justify=LEFT,padx=1)
       e1t = Entry(self.top, textvariable=self.v1)
       e1t.grid(row=0, column=2, padx=10, pady=5)  # sss
       self.top.colormapwindows
       B = tkinter.Button(self.top, text ="选择路径",command=lambda:self.getFile())
       B.grid(row=0,column=3,padx=10,pady=5)
       e1ts = Entry(self.top, textvariable=self.v3)
       e1ts.grid(row=0, column=4, padx=10, pady=5)  # sss
       B3 = tkinter.Button(self.top, text="选择保存路径", command=lambda: self.getSaveFile())
       B3.grid(row=0, column=5, padx=10, pady=5)

       B4 = tkinter.Button(self.top, text="删除", command=lambda: self.detelFile())
       B4.grid(row=0, column=6, padx=10, pady=5)
       #分析
       B1 = tkinter.Button(self.top, text="复制", command=lambda: self.CopyfileThread())
       B1.grid(row=0, column=7, padx=10, pady=5)
       vartr = StringVar()
       vartr.set("要查找的字以“,”分开：")
       tkinter.Label(self.top,textvariable=vartr,justify=LEFT,padx=10)
       self.top.mainloop()
    def getFile(self):
        default_dir="文件路径"
        fname=tkinter.filedialog.askdirectory(title='选择文件',initialdir=(os.path.expanduser((default_dir))))
        self.getAllPathFile(fname)
        self.getThread()
        self.v1.set(fname)
    def getThread(self):
        with ThreadPoolExecutor(10) as executor:
            executor.submit(self.createCheckButton())
    def createCheckButton(self):
        c=1
        for girl in self.allFile:
            var = IntVar()
            ss = Checkbutton(self.top, text=girl, variable=var)
            if c%4 !=0:
                ss.grid(row=int(c / 4)+1, column=c%4+1, padx=1, pady=1,sticky=W)  # 左对齐
            c = c + 1
            var.set(0)
            self.allFile.remove(girl)
            if c %30==0:
                self.PageSize = int(c / 4) + 2
                self.setpage()
                break
            self.check_buttons.append([var,girl,ss])
        self.top.update()
    def setpage(self):
        Bt = tkinter.Button(self.top, text="下一页", command=lambda: self.getThread())
        Bt.grid(row=self.PageSize, column=3, padx=10, pady=5)
    def detelFile(self):
        for filepath in self.allFilePath:
            enpaths=Path(filepath)
            if enpaths.is_file():
                allPath = os.path.basename(filepath)
                for checked in self.check_buttons:
                    if checked[0].get() == 1:
                        enpath = checked[1]
                        if allPath == enpath:
                            z = checked[2]
                            z.destroy()
                            os.remove(filepath)
                            self.allFilePath.remove(filepath)
                            self.allFile.remove(enpath)
        result = messagebox.showinfo(title='信息提示！', message='删除成功')


    def getSaveFile(self):
        default_dir = "文件路径"
        fname = tkinter.filedialog.askdirectory(title='选择文件', initialdir=(os.path.expanduser((default_dir))))
        self.v3.set(fname)

    def CopyfileThread(self):
        with ThreadPoolExecutor(10) as executor:
            executor.submit(self.Copyfile())
    def Copyfile(self):
        for filepath in self.allFilePath:
            allPath=os.path.basename(filepath)
            for checked in self.check_buttons:
                if checked[0].get() == 1:
                    enpath=checked[1]
                    if allPath==enpath:
                        a,filepathdir=os.path.dirname(filepath).split(":",1)
                        if filepathdir is not None:
                            copypath=Path(self.v3.get() + filepathdir)
                            if copypath.is_dir()==False:
                               os.makedirs(self.v3.get()+filepathdir)
                            copyzuFail= self.v3.get()+"/" + filepathdir + "/" + checked[1];
                            finallpath=Path(self.v3.get() + "/" + filepathdir + "/" + checked[1])
                            if finallpath.is_file()==False:
                              file = open(copyzuFail,W)
                            self.pathtext = self.pathtext + "\r\n" + copyzuFail
                            copyfile(filepath, copyzuFail)
        result = messagebox.showinfo(title='信息提示！', message='复制成功')
    def getAllPathFile(self,filepath):
        paths=Path(filepath)
        if paths.is_dir():
            pathdir = os.listdir(filepath)
            for path in pathdir:
                pathReal = filepath + "/" + path
                paths = pathReal.replace("'", "")
                self.getAllPathFile(paths)
        else:
            getpaths = os.path.basename(filepath)
            self.allFile.append(getpaths)
            self.allFilePath.append(filepath)
            return



