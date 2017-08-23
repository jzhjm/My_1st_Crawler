#!/usr/bin/env python  
# -*- coding: UTF-8 -*-

from Tkinter import *
from ScrolledText import ScrolledText
import urllib,requests
import re
import threading
import os
import tkFileDialog #文件选择模块
from tkFileDialog import askdirectory #文件夹选择模块

# path = os.path.dirname(sys.argv[0])
# path = os.path.split(os.path.realpath(__file__))[0]
# path = os.path.split(sys.argv[0])[0] #编译后能获取文件正确路径



url_name = [] #url+name
a = 1 #页
id = 1
beg = False

def get():
	global a
	hd = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
	url = 'http://www.budejie.com/video/'+str(a)
	varl.set('已经获取到第%s页视频'%(a))
	# a += 1
	html = requests.get(url,headers=hd).text # .text-获取源码
	# print html
	url_content = re.compile(r'<div class="j-r-list-c">.*?</div>.*?</div>',re.S)
	url_contents = re.findall(url_content,html)
	# print url_contents
	for i in url_contents:
		url_reg = re.compile(r'data-mp4="(.*?)">') #匹配视频URL
		url_items = re.findall(url_reg,i)
		# print url_items
		if url_items:
			name_reg = re.compile(r'<a href="/detail-.{8}?.html">(.*?)</\w',re.S)
			name_items = re.findall(name_reg,i)
			# print name_items
			for i,j in zip(name_items,url_items):
				url_name.append([i,j])
				# print i,j
	return url_name

def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    # print '%.2f%%' % per
    # print '.' * (int(per)/2)
    progress = '进度：|%s'%('.'*int(per))
    varl.set(progress.ljust(106)+'|%.2f%%' % per)


# id = 1
def write():
	global id
	# print id
	tmp = get()
	while id > len(tmp):
		print id
		global a
		a += 1
		tmp = get()
		print '第二页'

	url_name = tmp
	for i in url_name:
		local = os.path.join('video','%s.mp4'%(i[0]))
		urllib.urlretrieve(i[1],local,Schedule) # .decode('utf-8').encode('gbk')
		text.insert(END,str(id)+'.'+i[1]+'\n'+i[0]+'\n\n')
		url_name.pop(0)
		id -= 1
		varl.set('')
		if id <= 0:
			break
	# print 'over'
	varl.set('视频抓取完毕，over')
	os.system('open video')
	frame2.grid(row = 1, column = 0)
	B.set('继续爬去')
	global beg
	beg = True

path_= ''

def begin():
	global id
	id = Scale.get()
	# print id
	th = threading.Thread(target=write)
	th.start()
	frame2.grid_forget()
	B.set('停止爬取')
	global beg
	beg = False

def stop():
	os._exit(0)

def selectPath():
	global path_
	path_ = askdirectory()
	os.chdir(str(path_))
	if not os.path.isdir('video'):
		os.mkdir('video')
	# frame3.grid_forget()

def button():
	global path_
	global beg
	# while path_ == '':
	# 	selectPath()
	if path_ == '':
		varl.set('请选择存储路径')
		selectPath()
		varl.set('请选择爬去目标数量,视频存储目标路径:'+path_)
		B.set('开始爬取')
		beg = True
	else:
		if beg:
			begin()
		else:
			stop()
	# varl.set('请选择爬去目标数量,视频存储目标路径:'+path_)
	# B.set('开始爬取')
	# begin()


#GUI Tkinter
root = Tk()
root.title('test')
root.geometry('500x315+100+100')
root.resizable(width=False, height=False)

frame1 = Frame()
frame2 = Frame()
frame3 = Frame()
frame4 = Frame()

	#frame1
# path = StringVar()
text = ScrolledText(frame1, font=('华文细黑',10))

	#frame2
Scale = Scale(frame2,from_=1,to=100,orient = HORIZONTAL,label='选择爬取视频数量:',font=('华文细黑',10))

	#frame3
B = StringVar()
B.set('路径选择')
button = Button(frame3,textvariable=B,font=('华文细黑',10),command=button)
# button2 = Button(frame3,text='停止爬去',font=('华文细黑',10),command=stop)

	#frame4
varl = StringVar()
varl.set('请选择存储路径')
label = Label(frame4,font=('华文细黑',10),fg='red',textvariable = varl)
# entry = Entry(frame3, textvariable=path, state = 'readonly')
# button2 = Button(frame3, text = "路径选择", command = selectPath)
# label2 = Label(frame3,text = "目标路径:")

# 布局
frame1.grid(columnspan=2, padx=0, pady=0)
text.grid(row = 0, column = 0)

frame2.grid(row = 1, column = 0, padx=0, pady=0)
Scale.grid(row=0, column=0)

frame3.grid(row = 1, column = 1, padx=0, pady=0)
button.grid(row = 0, column = 0)
# button2.grid(row = 1,column = 0)

frame4.grid(row = 2,column = 0,columnspan=2, padx=0, pady=0)
label.grid(row = 0, column = 0)
# label2.grid(row = 0, column = 0)
# entry.grid(row = 0, column = 1)
# button2.grid(row = 0, column = 2)
root.mainloop()


