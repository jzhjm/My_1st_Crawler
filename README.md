# My_1st_Crawler

这是我学习python后，参照案例写的第一只爬虫

**里面的urllib、RE正则表达式 仍需熟悉掌握**

爬取的是《[百思不得姐](http://www.budejie.com/video/)》上的视频

GUI使用的是 TKinter模块
- 真的好难用，几乎找不到文档
- 准备下次使用 pyqt 或者 wxpython

最终使用pyinstaller打包
- 一次打包，生成spec文件，同时也生成可执行程序：
`pyinstaller --windowed --onefile --clean --noconfirm main.py`

- 修改spec文件参数，通过spec文件打包
`pyinstaller --clean --noconfirm --windowed --onefile main.spec`

遇到的几个问题
Q1:编译后无法获取文件自身所在路径
A1:path = os.path.split(sys.argv[0])[0] #编译后能获取文件正确路径

