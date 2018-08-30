#！/usr/bin/env python
#coding:utf-8
import tkinter
import tkinter.messagebox,tkinter.simpledialog
import os
import os.path
import threading

class niupeng:
	def __init__(self):
		self.root = tkinter.Tk()
		self.rubbishExt = ['.tmp','.bak','.old','.wbk','.xlk','._mp','.log','.gid',
		'.chk','.syd','.$$$','.@@@','.~*`']
		#创建菜单
		menu = tkinter.Menu(self.root)
		#创建系统子菜单
		submenu = tkinter.Menu(menu,tearoff=0)
		submenu.add_command(label="关于...",command=self.MenuAbout)
		submenu.add_separator()
		submenu.add_command(label="退出",command=self.MenuExit)
		menu.add_cascade(label="系统",menu=submenu)
		#创建清理子菜单
		submenu = tkinter.Menu(menu,tearoff=0)
		submenu.add_command(label="扫描垃圾文件",command=self.MenuScanRubbish)
		submenu.add_command(label="删除垃圾文件",command=self.MenuDeRubbish)
		menu.add_cascade(label="清理",menu=submenu)
		#创建查找子菜单
		submenu = tkinter.Menu(menu,tearoff=0)
		submenu.add_command(label="搜索大文件",command=self.MenuScanBigFile)
		submenu.add_separator()
		submenu.add_command(label="按名称搜索文件",command=self.MenuSearchFile)
		menu.add_cascade(label="搜索",menu=submenu)
		self.root.config(menu=menu)
		#创建标签，用于显示状态信息
		self.progress = tkinter.Label(self.root,anchor = tkinter.W,
			text = '状态',bitmap = 'hourglass',compound = 'left')
		self.progress.place(x=10,y=370,width = 480,height = 15)
		#创建文本框,显示文件列表
		self.flist = tkinter.Text(self.root)
		self.flist.place(x=10,y=10,width =480,height = 250)
		#为文本框添加垂直宫东条
		self.vscroll = tkinter.Scrollbar(self.flist)
		self.vscroll.pack(side = 'right',fill = 'y')
		self.flist['yscrollcommand'] = self.vscroll.set
		self.vscroll['command'] = self.flist.yview
	#"关于"菜单
	def MenuAbout(self):
		tkinter.messagebox.showinfo('Findfat',"这里是用python编写的windows优化程序.\n欢迎提出宝贵意见")
	#"退出"菜单
	def MenuExit(self):
		self.root.quit()
	#"扫描垃圾文件"菜单
	def MenuScanRubbish(self):
		result = tkinter.messagebox.askquestion('Findfat',"扫描垃圾文件需要较长时间，是否继续")
		if result == 'no':
			return
		tkinter.messagebox.showinfo('Findfat',"马上开始扫描垃圾文件")
		#self.ScanRubbish()
		t = threading.Thread(target=self.ScanRubbish)
		t.start()

	#"删除来及文件"菜单
	def MenuDeRubbish(self):
		result = tkinter.messagebox.askquestion('Findfat',"删除垃圾文件需要较长时间，是否继续")
		if result == 'no':
			return
		tkinter.messagebox.showinfo('Findfat',"马上开始删除垃圾文件")
		t = threading.Thread(target=self.DeleteRubbish)
		t.start()
	#"搜索大文件"菜单
	def MenuScanBigFile(self):
		s = tkinter.simpledialog.askinteger('Findfat','请设置文件的大小')
		t = threading.Thread(target=self.ScanBigFile,args=(s,))
		t.start()
	#"按名称"菜单
	def MenuSearchFile(self):
		s = tkinter.simpledialog.askstring('Findfat','请输入文件名的部分字符')
		t = threading.Thread(target=self.SearchFile,args=(s,))
		t.start()
	###"扫描垃圾文件"功能
	def ScanRubbish(self):
		total = 0
		filesize = 0
		for root,dirs,files in os.walk("C:/"):
			try:
				for file in files:
					filesplit = os.path.splitext(file)
					if filesplit[1] == '':
						continue
					try:
						if self.rubbishExt.index(filesplit[1]) >= 0:
							fname = os.path.join(os.path.abspath(root),file)
							filesize += os.path.getsize(fname)
							if total % 20 == 0:
								self.flist.delete(0.0,tkinter.END)
							self.flist.insert(tkinter.END,fname + '\n')
							l = len(fname)
							if l>60:
								self.progress['text'] = fnam[:30] + '....' + fname[l-30:1]
							else:
								self.progress['text'] = fname
								total += 1
					except ValueError:
						pass
			except Exception as e:
				print(e)
				pass
		self.progress['text'] = "找到 %s 个文件，共占用 %.2f M 磁盘空间" %(total,filesize/1024/1024)
	#删除垃圾文件功能
	def DeleteRubbish(self):
		total = 0
		filesize = 0
		for root,dirs,files in os.walk('c:/'):
			try:
				for file in files:
					filesplit = os.path.splitext(file)
					if filesplit[1] == '':
						continue
					try:
						if self.rubbishExt.index(filesplit[1]) >= 0:
							fname = os.path.join(os.path.abspath(root),file)
							filesize += os.path.getsize(fname)
							try:
								os.remove(fname)
								self.flist.delete(0.0,tkinter.END)
								self.flist.insert(tkinter.END,'Deletesd' + fname +'\n')
								self.progress['text'] = fname
								total += 1
							except:
								pass
					except ValueError:
						pass
			except Exception as e:
				print(e)
				pass
		self.progress['text'] = "删除 %s 个垃圾文件,收回 %.2f M 磁盘空间" %(total,filesize/1024/1024)
	#搜索大文件功能
	def ScanBigFile(self,filesize):
		total = 0
		filesize = filesize*1024*1024
		for root,dirs,files in os.walk('C:/'):
			for file in files:
				try:
					fname = os.path.abspath(os.path.join(root,file))
					fsize = os.path.getsize(fname)
					self.progress['text'] = fname
					if fsize >= filesize:
						total += 1
						self.flist.insert(tkinter.END,'%s,[%.2f M]\n' %(fname,fsize/1024/1024))
				except:
					pass
		self.progress['text'] = "找到 %s 个超过 %sM 的大文件" %(total,filesize/1024/1024)
	#按名称搜索文件
	def SearchFile(self,fname):
		total = 0
		fname = fname.upper()
		for root,dirs,files in os.walk('C:/'):
			for file in files:
				try:
					fn = oa.path.abspath(os.path.join(root,file))
					self.progress['text'] = fn
					if file.upper().find(fname) >= 0:
						total += 1
						self.flist.insert(tkinter.END,fn + '\n')
				except:
					pass
		self.progress['text'] = "找到 %s 个文件" %(total)
	def MainLoop(self):
		self.root.title('Findfat')
		self.root.minsize(500,400)
		self.root.maxsize(500,400)
		self.root.mainloop()
if __name__ == "__main__":
	ttt = niupeng()
	ttt.MainLoop()
	
