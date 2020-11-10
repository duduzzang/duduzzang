#!/usr/bin/env python
##############################################################################
# Copyright (c) 2012 Hajime Nakagami<nakagami@gmail.com>
# All rights reserved.
# Licensed under the New BSD License
# (http://www.freebsd.org/copyright/freebsd-license.html)
#
# A image viewer. Require Pillow ( https://pypi.python.org/pypi/Pillow/ ).
##############################################################################
import PIL.Image
import nibabel as nib

try:
    from Tkinter import *
    import tkFileDialog as filedialog
except ImportError:
    from tkinter import *
    from tkinter import filedialog
import PIL.ImageTk

class App(Frame):
    def chg_image(self):
        if self.im.mode == "1": # bitmap image
            self.img = PIL.ImageTk.BitmapImage(self.im, foreground="white")
        else:              # photo image
            self.img = PIL.ImageTk.PhotoImage(self.im)
        self.la.config(image=self.img, bg="#000000",
            width=self.img.width(), height=self.img.height())

    def open(self):
        filename = filedialog.askopenfilename()
        if filename != "":
            # 1. Proxy 불러오기
            proxy = nib.load(filename)

            # 2. Header 불러오기
            header = proxy.header

            # 3. 원하는 Header 불러오기 (내용이 문자열일 경우 숫자로 표현됨)
            header_size = header['sizeof_hdr']

            # 2. 전체 Image Array 불러오기
            arr = proxy.get_fdata() 

            # 3. 원하는 Image Array 영역만 불러오기
            sub_arr = proxy.dataobj[..., 0:5]
            sub_arr = sub_arr.reshape(sub_arr.shape[0], sub_arr.shape[1])

            self.im = PIL.Image.fromarray(sub_arr)
        self.chg_image()
        self.num_page=0
        self.num_page_tv.set(str(self.num_page+1))

    def seek_prev(self):
        self.num_page=self.num_page-1
        if self.num_page < 0:
            self.num_page = 0
        self.im.seek(self.num_page)
        self.chg_image()
        self.num_page_tv.set(str(self.num_page+1))

    def seek_next(self):
        self.num_page=self.num_page+1
        try:
            self.im.seek(self.num_page)
        except:
            self.num_page=self.num_page-1
        self.chg_image()
        self.num_page_tv.set(str(self.num_page+1))

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Image Viewer')

        self.num_page=0
        self.num_page_tv = StringVar()

        fram = Frame(self)
        Button(fram, text="Open File", command=self.open).pack(side=LEFT)
        Button(fram, text="Prev", command=self.seek_prev).pack(side=LEFT)
        Button(fram, text="Next", command=self.seek_next).pack(side=LEFT)
        Label(fram, textvariable=self.num_page_tv).pack(side=LEFT)
        fram.pack(side=TOP, fill=BOTH)

        self.la = Label(self)
        self.la.pack()

        self.pack()

if __name__ == "__main__":
    app = App(); app.mainloop()