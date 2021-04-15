import os
import time
import math
import codecs
import win32com
import shutil
import pythoncom
from win32com.client import Dispatch, constants, gencache, DispatchEx
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter, A4, landscape  
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import inch  
from reportlab.pdfgen import canvas
from reportlab import rl_settings

SAVE_DIR = r'/upfile/stagingConvertFiles/'
# ppt转化为pdf入口
def ppt2pdf_entrance(ppt_path, pdf_save_dir):
	ppt_path = ppt_path
	save_dir = pdf_save_dir + SAVE_DIR

	ppt_dir, suffix_filename = os.path.split(ppt_path)
	file_name = os.path.splitext(suffix_filename)[0]

	img_file = os.path.join(ppt_dir, file_name+'.png')

	ppt2png(ppt_path,img_file)
	img_dir = os.path.join(ppt_dir, file_name)

	imgFileList = os.listdir(img_dir)

	imgFileList = [os.path.join(img_dir, f) for f in imgFileList]
	imgFileList.sort(key=lambda x: os.path.getmtime(x))

	topdf(path=img_dir, save=save_dir)
	shutil.rmtree(img_dir)
	
	return SAVE_DIR + file_name +'.pdf'

#PPT转成PNG文件
def ppt2png(filename,dst_filename):
	pythoncom.CoInitialize()
	ppt = win32com.client.Dispatch('PowerPoint.Application')
	#ppt.DisplayAlerts = False
	pptSel = ppt.Presentations.Open(filename, WithWindow = False)
	# print(dst_filename)
	pptSel.SaveAs(dst_filename,18); #with 17, jpeg
	ppt.Quit()

#合并输出PDF
def topdf(path,recursion=None,pictureType=None,sizeMode=None,width=None,height=None,fit=None,save=None):
	"""
	Parameters
	----------
	path : string
		   path of the pictures
	pictureType : list
				  type of pictures,for example :jpg,png...
	sizeMode : int 
		   None or 0 for pdf's pagesize is the biggest of all the pictures
		   1 for pdf's pagesize is the min of all the pictures
		   2 for pdf's pagesize is the given value of width and height
		   to choose how to determine the size of pdf
	width : int
			width of the pdf page
	height : int
			height of the pdf page
	fit : boolean
		   None or False for fit the picture size to pagesize
		   True for keep the size of the pictures
		   wether to keep the picture size or not
	save : string 
		   path to save the pdf 
	"""

	filelist = os.listdir(path)
	filelist = [os.path.join(path, f) for f in filelist]
	filelist.sort(key=lambda x: os.path.getmtime(x))

	maxw = 0
	maxh = 0
	if sizeMode == None or sizeMode == 0:
		for i in filelist:
			#print('----'+i)
			im = Image.open(i)
			if maxw < im.size[0]:
				maxw = im.size[0]
			if maxh < im.size[1]:
				maxh = im.size[1]
	elif sizeMode == 1:
		maxw = 999999
		maxh = 999999
		for i in filelist:
			im = Image2.open(i)
			if maxw > im.size[0]:
				maxw = im.size[0]
			if maxh > im.size[1]:
				maxh = im.size[1]
	else:
		if width == None or height == None:
			raise Exception("no width or height provid")
		maxw = width
		maxh = height

	maxsize = (maxw,maxh)
	if save == None:
		filename_pdf = os.path.join(path, path.split('\\')[-1])
	else:
		filename_pdf = os.path.join(save, path.split('\\')[-1])

	filename_pdf = filename_pdf + '.pdf'
	c = canvas.Canvas(filename_pdf, pagesize=maxsize )
	 
	l = len(filelist)
	for i in range(l): 
		# print(filelist[i])
		(w, h) =maxsize
		width, height = letter 
		if fit == True:
			c.drawImage(filelist[i] , 0,0) 
		else:
			c.drawImage(filelist[i] , 0,0,maxw,maxh) 
		c.showPage()  
	c.save()

# word转化为pdf的入口
def word2pdf_entrance(wordPath, pdf_save_path):
	wordPath = wordPath
	pdf_save_path = pdf_save_path + SAVE_DIR
	word_file_name = os.path.splitext(os.path.split(wordPath)[1])[0]
	pdfPath = os.path.join(pdf_save_path, word_file_name)
	pythoncom.CoInitialize()
	word = gencache.EnsureDispatch('Word.Application')  #
	doc = word.Documents.Open(wordPath, ReadOnly=1)
	doc.ExportAsFixedFormat(pdfPath,
							constants.wdExportFormatPDF,
							Item=constants.wdExportDocumentWithMarkup,
							CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
	word.Quit(constants.wdDoNotSaveChanges)
	
	return SAVE_DIR + word_file_name + '.pdf'

# excel转化为pdf的入口
def excel2pdf_entrance(excelPath, pdf_save_path):
	excelPath = excelPath
	excel_file_name = os.path.splitext(os.path.split(excelPath)[1])[0]
	pdf_save_path = pdf_save_path + SAVE_DIR
	pdfPath = os.path.join(pdf_save_path, excel_file_name)
	pythoncom.CoInitialize()
	xlApp = DispatchEx("Excel.Application")
	xlApp.Visible = False    
	xlApp.DisplayAlerts = 0   
	books = xlApp.Workbooks.Open(excelPath,False)
	books.ExportAsFixedFormat(0, pdfPath)
	books.Close(False)
	xlApp.Quit()

	return SAVE_DIR + excel_file_name + '.pdf'