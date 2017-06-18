# -*- coding: cp936 -*-
import os
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
import sys
sys.path.append('../')
import StepPackage
from StepPackage.Step_5_VCodeAPI import startValidate

### ͼ�ν���Ӧ����
class Application(tkinter.Tk):
    ## ��ʼ������
    def __init__(self):
        super().__init__() # �е��൱��tk.Tk()
        # self.geometry("500x300")  # ���ô��ڴ�С
        self.center_window()# ˮƽ����
        self.createWidgets()#��������

    ## ��������
    def createWidgets(self):
        self.title('��֤��ʶ��')
        self.columnconfigure(0, minsize=50)

        # �������ð�ť�ͱ�ǩ��frame
        first_frame = tkinter.Frame(self, height=80)
        first_frame.pack(side=tkinter.TOP)
        # ������ʾ��֤��ͼƬ��ʶ������frame
        self.second_frame = tkinter.Frame(self, height=80)
        self.second_frame.pack()

        # ���尴ť�ͱ�ǩ
        choose_button = Button(first_frame, command=self.openImage, text='����˴�ѡ����֤��ͼƬ')
        img_path_label = Label(first_frame, text='��ǰ��֤��ͼƬ·��:')
        # cur_image_path = Label(first_frame, text='��ǰû��·����Ϣ')
        cur_image_path = Entry(first_frame, borderwidth = 3, relief = 'sunken', state = 'disabled',\
                               width=56, font = ('����', '10', 'bold'))
        self.pre_image_btn = Button(first_frame, command=self.preImage, text='��һ��ͼƬ')
        self.next_image_btn = Button(first_frame, command=self.nextImage, text='��һ��ͼƬ')
        img_name_label = Label(self.second_frame, text='��֤��ͼƬ��', font = ('����', '15', 'bold'))
        img_label = Label(self.second_frame, text="��ǰ��ͼƬ", relief='flat', borderwidth=10)
        interval = Label(self.second_frame, text='  ')
        img_res_label = Label(self.second_frame, text='ʶ����:', font = ('����', '15', 'bold'))
        res_label = Label(self.second_frame, relief='flat', text='����', borderwidth=10)
        btn_quit = Button(self.second_frame, text='�˳�', font = ('����', '15', 'bold'), command=self.colseProgram)

        # ��̬��ʾ��ǰ��֤��·��
        self.img_path_txt = StringVar() # �洢��֤��·��
        cur_image_path["textvariable"] = self.img_path_txt
        self.img_path_txt.set('��ǰû��·����Ϣ')

        # ���õ�λ��
        choose_button.grid(row=0, rowspan=3, column = 3, sticky=tkinter.E+tkinter.W, padx=5, pady=20)

        img_path_label.grid(row=3, rowspan=3, column=0, pady=20)
        cur_image_path.grid(row=3, rowspan=3, column=2, columnspan=8, padx=5, pady=20)

        self.pre_image_btn.grid(row=6, rowspan=3, column=2, padx=5, pady=20)
        self.next_image_btn.grid(row=6, rowspan=3, column=4, padx=5, pady=20)

        img_name_label.grid(row=0, column=0, pady=60)
        img_label.grid(row=0, column=1, columnspan=2, pady=60, sticky=tkinter.W)
        interval.grid(row=0, column=3)
        img_res_label.grid(row=0, column=4, pady=60, sticky=tkinter.E)
        res_label.grid(row=0, column=5, columnspan=2, pady=60, sticky=tkinter.W)
        btn_quit.grid(row = 3, column=2, columnspan=2, pady=100)

    ## ���������ж���
    def center_window(self):
        width, height = 800, 600

        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()

        self.maxsize(screenwidth, screenheight)
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

        size = '{}x{}+{}+{}'.format(width, height, int((screenwidth-width)/2), int((screenheight-height)/2))
        self.geometry(size)

    ## ��ͼƬ
    def openImage(self):
        # ѡ��·��
        dirname = filedialog.askopenfilename(\
            filetypes=[("jpg��ʽ", "jpg"), ("png��ʽ", "png")], initialdir='../')

        # ������
        if not dirname:
            tkinter.messagebox.showerror('����', '��δѡ���ļ���')
            return

        self.img_path_txt.set(dirname)#����·��
        self.cur_img_name = dirname# �洢��ǰͼƬ��·��

        ## �и�·�� �õ���ǰͼƬ�����ļ���
        list = dirname.split('/')
        rootdir = ''
        for i in range(len(list) - 1):
            rootdir += (list[i] + '/')
        # print(rootdir)

        ## �ҵ���ǰ�ļ���������ͼƬ
        self.filenames = []  # ͼƬ���Ƽ���
        for parent, dirnames, _filenames in os.walk(rootdir):
            _filenames.sort(key=lambda x: int(x[:-4]))
            for name in _filenames:
                self.filenames.append(parent+name)

        ### �򿪵�ǰͼƬ
        load = Image.open(dirname)
        load = load.resize((200,100))
        img = ImageTk.PhotoImage(load)
        ##��ʾͼƬ
        self.img_label = Label(self.second_frame, image=img)
        self.img_label.image = img
        ##��ʾʶ����
        res_label = Label(self.second_frame, font = ('����', '20', 'bold'))
        self.res_txt = StringVar()
        res_label["textvariable"] = self.res_txt
        ## ����λ��
        self.img_label.grid(row=0, column=1, columnspan=2, pady=60, sticky=tkinter.W)
        res_label.grid(row=0, column=5, columnspan=2, pady=60, sticky=tkinter.W)
        #�����߼�����ʶ��
        ori_image = Image.open(dirname)
        result = startValidate(ori_image)
        self.res_txt.set(result)

    ## ʶ����һ��ͼƬ
    def preImage(self):
        #��ǰͼƬ�ڵ�ǰͼƬ�ļ���list�е�λ���±�
        try:
            cur_num = self.filenames.index(self.cur_img_name)
        except:
            messagebox.showerror('����', '��δѡ��ͼƬ��')
            return

        # ��Ե����1��ͼƬ����
        if cur_num == 0:
            tkinter.messagebox.showwarning('��ʾ', '�Ѿ��ǵ�1��ͼƬ��')
            self.pre_image_btn['state'] = DISABLED
            return

        #������һ�Ű�ť
        if cur_num == len(self.filenames)-1:
            self.next_image_btn['state'] = NORMAL

        #�ҵ�ǰһ��ͼƬ����·��
        self.cur_img_name = self.filenames[cur_num - 1]
        #����·��
        self.img_path_txt.set(self.cur_img_name)
        #��ʾͼƬ
        self.showImg(self.cur_img_name)

    ## ʶ����һ��ͼƬ
    def nextImage(self):
        # ��ǰͼƬ�ڵ�ǰͼƬ�ļ���list�е�λ���±�
        try:
            cur_num = self.filenames.index(self.cur_img_name)
        except:
            messagebox.showerror('����', '��δѡ��ͼƬ��')
            return
        # ��Ե������һ��ͼƬ����
        if cur_num == len(self.filenames)-1:
            tkinter.messagebox.showwarning('��ʾ', '�Ѿ������һ��ͼƬ��')
            self.next_image_btn['state'] = DISABLED
            return

        # ������һ�Ű�ť
        if cur_num == 0:
            self.pre_image_btn['state'] = NORMAL

        # �ҵ���һ��ͼƬ����·��
        self.cur_img_name = self.filenames[cur_num + 1]
        # ����·��
        self.img_path_txt.set(self.cur_img_name)
        # ��ʾͼƬ
        self.showImg(self.cur_img_name)

    ## ��ʾͼƬ
    def showImg(self, path):
        # ����ͼƬ
        load = Image.open(path)
        load = load.resize((200, 100), Image.ANTIALIAS)
        self.next_img = ImageTk.PhotoImage(load)
        # �л�ͼƬ
        self.img_label.configure(image=self.next_img)
        # �����߼�����ʶ��
        ori_image = Image.open(path)
        result = startValidate(ori_image)
        # print('result', result)
        self.res_txt.set(result)

    ## ��Ӳ˵���
    def addmenu(self, Menu):
        Menu(self)#��ӵ�ǰ

    ## �˳�
    def colseProgram(self):
        self.quit()

### �˵���
class MyMenu():
    ## ��ʼ��
    def __init__(self, root):
        self.menubar = tkinter.Menu(root) # �����˵���
        # �������ļ��������˵�
        filemenu = tkinter.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="��", command=root.openImage)
        filemenu.add_separator()
        filemenu.add_command(label="�˳�", command=root.quit)
        # ��ǰ�������˵��ӵ��˵���
        self.menubar.add_cascade(label="�ļ�", menu=filemenu)
        self.menubar.add_cascade(label="����", command=self.help_about)
        # ����ٽ��˵��������ӵ����� root
        root.config(menu=self.menubar)

    ## �����˵�
    def help_about(self):
        messagebox.showinfo('����', '���ߣ�����ʤ \n�汾�� Version 1.0 \n���䣺husen@hemingsheng.cn \n\n\t\t\t��л����ʹ�ã� \n\n\n\t��Ȩ����@2017')  # ������Ϣ��ʾ��


if __name__ == '__main__':
    #### ��֤��ʶ���ͼ�λ�����
    application = Application()  # ʵ����Application
    application.addmenu(MyMenu)  # ��Ӳ˵�
    application.mainloop()  # ����Ϣѭ��
