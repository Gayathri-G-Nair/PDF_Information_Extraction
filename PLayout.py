'''
Python implementation of Scholarly PDF Layout Analysis
GUI is created using Tkinter module, PIL
Packages used are os, sys, getopt, tkinter, pdfminer
Author  : Gayathri G. Nair
Date    : 08:04:2018
Purpose : Mini Project
'''

#Import neccessery packages of pdfminer for pdf to text conversion
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfrw import PdfReader
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from cStringIO import StringIO

import os
import sys, getopt

import re

#Import Tkinter 2.7 Python packages
import time
import Tkinter
import Tkinter as tk
from Tkinter import *
import tkMessageBox
import tkFileDialog
from PIL import ImageTk,Image
import PIL.Image

#Import Extract_email() from Metadata.py
from Metadata1 import Extract_email
from Metadata1 import *

#For pdf to text conversion
def converttotext(pdfFilename):
	text = convert(pdfFilename) 
	pdfFilename = pdfFilename.replace('.','')
	textFilename = pdfFilename+ ".txt"
	textFile = open(textFilename, "w+") 
	textFile.write(text)
	textFile.close() 
	
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text 
	
#Extract Title from pdf	
def Extract_title(pdfFilename):
	global originalpdf
	originalpdf = pdfFilename
	pdfFilename = pdfFilename.replace('.','')
	
	global filterd_textfile
	filterd_textfile = pdfFilename+"filterd"+".txt"
	filterd_file = open(filterd_textfile,"a+")
	
	global labelled_textfile
	labelled_textfile = pdfFilename+"labelled"+".txt"
	labelled_file = open(labelled_textfile,"a+")
	
	global Title
	Title = PdfReader(originalpdf).Info.Title
	tag = "Title"
	labelled_file.write("%s %s"%(tag,Title))
	labelled_file.write("\n")
	filterd_file.write("%s %s"%(tag,Title))
	filterd_file.write("\n")
	print "Ttile: ", Title
	print '\n'

	filterd_file.close()
	labelled_file.close()

#Extract Metadata from pdf	
def Extract_metadata(pdfFilename):
	originalpdf = pdfFilename
	pdfFilename = pdfFilename.replace('.','')
	
	global labelled_textfile
	labelled_textfile = pdfFilename+"labelled"+".txt"
	labelled_file = open(labelled_textfile,"a+")
	
	tag = "Metadata"
	global Author
	Author = PdfReader(originalpdf).Info.Author
	labelled_file.write("%s %s"%(tag,Author))
	labelled_file.write('\n')
	labelled_file.close()
	Extract_email(originalpdf) #Function call to Metadata.py

#Extract Abstract from pdf	
def Extract_abstract(pdfFilename):
	global textFilename
	pdfFilename = pdfFilename.replace('.','')
	textFilename = pdfFilename+ ".txt"

	global abstract_textfile
	global labelled_textfile
	global filterd_textfile
	abstract_textfile = pdfFilename+"abstract"+".txt"
	AbtextFile = open(abstract_textfile,"w+")
	
	labelled_textfile = pdfFilename+"labelled"+".txt"
	labelled_file = open(labelled_textfile,"a+")
	
	filterd_textfile = pdfFilename+"filterd"+".txt"
	filterd_file = open(filterd_textfile,"a+")

	Actual_textfile = open(textFilename,'r')
	line = Actual_textfile.readlines()
	no_of_lines = len(line)
	global abstract
	abstract = []
	tag = "Abstract"
	for x in xrange(no_of_lines):
		if ((line[x].find("Abstract")!=-1) or (line[x].find("Objectives")!=-1)):		
			while(line[x].find("Introduction") < 0):
	
				line[x] = line[x].lstrip('Abstract.')
				labelled_file.write("%s %s"%(tag,line[x]))
				filterd_file.write("%s %s"%(tag,line[x]))
				AbtextFile.write(line[x])
				abstract.append(line[x])
				x = x+1
			
			break
			
	AbtextFile.close()
	labelled_file.close()
	Actual_textfile.close()
	filterd_file.close()
	
#Extract Bodytext Content from pdf
def Extract_bodytext(pdfFilename):
	Author = PdfReader(pdfFilename).Info.Author
	Title = PdfReader(pdfFilename).Info.Title
	
	pdfFilename = pdfFilename.replace('.','')
	textFilename = pdfFilename+ ".txt"
	global bodytext_textfile
	global labelled_textfile
	global filterd_textfile
	bodytext_textfile = pdfFilename+"bodytext"+".txt"
	bodytextFile = open(bodytext_textfile,"w+")

	labelled_textfile = pdfFilename+"labelled"+".txt"
	labelled_file = open(labelled_textfile,"a+")
	
	filterd_textfile = pdfFilename+"filterd"+".txt"
	filterd_file = open(filterd_textfile,"a+")


	Actual_textfile = open(textFilename,'r')
	line = Actual_textfile.readlines()
	no_of_lines = len(line)
	global bodytext
	bodytext = []
	tag = "Bodytext"
	for x in xrange(no_of_lines):
		if (line[x].find("Introduction")!=-1):		
			while(line[x].find("Conclusion") < 0):
	
				
				if((len(line[x]))>5):
					if((line[x].find(Author)!=-1) or (line[x].find(Title)!=-1)):
						x=x+1
					else:
						labelled_file.write("%s %s"%(tag,line[x]))
						filterd_file.write("%s %s"%(tag,line[x]))
						bodytextFile.write(line[x])
						bodytext.append(line[x])
						x = x+1
				else:
					x=x+1
				
			break
			
	Actual_textfile.close()
	bodytextFile.close()
	labelled_file.close()
	filterd_file.close()
	
#Extract Conclusion Part from pdf	
def Extract_conclusion(pdfFilename):
	pdfFilename = pdfFilename.replace('.','')
	textFilename = pdfFilename+ ".txt"
	global conclusion_textfile
	global labelled_textfile
	global filterd_textfile
	conclusion_textfile = pdfFilename+"conclusion"+".txt"
	conclusiontextFile = open(conclusion_textfile,"w+")

	labelled_textfile = pdfFilename+"labelled"+".txt"
	labelled_file = open(labelled_textfile,"a+")
	
	filterd_textfile = pdfFilename+"filterd"+".txt"
	filterd_file = open(filterd_textfile,"a+")

	Actual_textfile = open(textFilename,'r')
	line = Actual_textfile.readlines()
	no_of_lines = len(line)
	conclusion = []
	tag = "Conclusion"
	for x in xrange(no_of_lines):
		if (line[x].find("Conclusion")!=-1)or(line[x].find("Conclusion and future works")!=-1):		
			while(line[x].find("Acknowledgement") < 0):
				if((len(line[x]))>1):
					if((line[x].find("223"))!=-1):
						x=x+1
					else:
						line[x] = line[x].lstrip('Conclusion.')
						labelled_file.write("%s %s"%(tag,line[x]))
						filterd_file.write("%s %s"%(tag,line[x]))
						conclusiontextFile.write(line[x])
						conclusion.append(line[x])
						x = x+1
				else:
					x=x+1
			break
			
	Actual_textfile.close()
	labelled_file.close()
	conclusiontextFile.close()
	filterd_file.close()

#Extract References from pdf	
def Extract_references(pdfFilename):
	pdfFilename = pdfFilename.replace('.','')
	textFilename = pdfFilename+ ".txt"
	
	global reference_textfile
	reference_textfile = pdfFilename+"reference"+".txt"
	referencetextfile = open(reference_textfile,"w+")
	
	global labelled_textfile
	global filterd_textfile
	labelled_textfile = pdfFilename+"labelled"+".txt"
	labelled_file = open(labelled_textfile,"a+")
	
	filterd_textfile = pdfFilename+"filterd"+".txt"
	filterd_file = open(filterd_textfile,"a+")

	Actual_textfile = open(textFilename,'r')
	line = Actual_textfile.readlines()
	no_of_lines = len(line)
	global references
	references = []
	tag = "References"
	
	for x in xrange(no_of_lines):
		
		if (line[x].find("References")!=-1):		
			while(x < no_of_lines):
				if((len(line[x]))>1):
					line[x] = line[x].lstrip('References')
					labelled_file.write("%s %s"%(tag,line[x]))
					filterd_file.write("%s %s"%(tag,line[x]))
					referencetextfile.write(line[x])
					references.append(line[x])
					x = x+1
				else:
					x=x+1
			
			break
			
	Actual_textfile.close()
	referencetextfile.close()
	labelled_file.close()
	filterd_file.close()
		
#To perform functionalities when the file is chosen
def choose_file():
	global Filename
	Filename = tkFileDialog.askopenfilename(filetypes = (("Pdf Files","*.pdf"),("all files","*.*"))) #To read file path
	E1.delete(0, END)
	E1.insert(0, Filename)
	time.sleep(3)
	tkMessageBox.showinfo("Wait", "Please Wait a moment!")
	
	#Set All buttons Enable
	TitleBut['state'] = 'normal'
	AbstractBut['state'] = 'normal'
	BodytextBut['state'] = 'normal'
	ConclusionBut['state'] = 'normal'
	ReferencesBut['state'] = 'normal'
	pdftotextBut['state'] = 'normal'
	MetadataBut['state'] = 'normal'
	OutputBut['state'] = 'normal'
	FilterBut['state'] = 'normal'
	
	#Function calls
	converttotext(Filename)
	Extract_title(Filename)
	Extract_metadata(Filename)
	Extract_abstract(Filename)
	Extract_bodytext(Filename)
	Extract_conclusion(Filename)
	Extract_references(Filename)

#To display Title	
def Display_Title():
	ResultBox.delete(1.0, END)
	ResultBox.insert(END, Title)

#To display Abstract	
def Display_Abstract():
	ResultBox.delete(1.0, END)
	f = open(abstract_textfile, 'r') 
	ResultBox.insert(END, " ".join(line.strip() for line in f))
	f.close()

#To display Metadata	
def Display_Metadata():
	name = Filename.replace('.','')
	Metafile = name+"metadatas"+".txt"
	ResultBox.delete(1.0, END)
	ResultBox.insert(END, Author)
	ResultBox.insert(END,'\n')
	f = open(Metafile,"r")
	ResultBox.insert(END, " ".join(line.strip() for line in f))
	f.close()
	
	
#To display Bodytext		
def Display_Bodytext():
	ResultBox.delete(1.0, END)
	for element in bodytext:
		ResultBox.insert(END, element)
	os.system(bodytext_textfile)

#To display Conclusion	
def Display_Conclusion():
	ResultBox.delete(1.0, END)
	f = open(conclusion_textfile, 'r')
	if (f==-1):
		tkMessageBox.showinfo("Conclusion Error", "There is no Conclusion!!")
	else:
		ResultBox.insert(END, " ".join(line.strip() for line in f))
		f.close()

#To display References		
def Display_References():
	ResultBox.delete(1.0, END)
	for element in references:
		ResultBox.insert(END, element)
	os.system(reference_textfile)

#To display pdf to text file	
def Display_pdftotext():
	ResultBox.delete(1.0, END)
	f = open(textFilename, 'r') 
	for line in f:
		ResultBox.insert(END,line)
	f.close()
	os.system(textFilename)

#To display the labelled pdf text file	
def Display_Output():
	ResultBox.delete(1.0, END)
	f = open(labelled_textfile, 'r') 
	
	for line in f:
		ResultBox.insert(END, line)
	f.close()
	os.system(labelled_textfile)
	
#To display the filterd_file	
def Display_filter():
	ResultBox.delete(1.0, END)
	f = open(filterd_textfile, 'r') 
	for line in f:
		ResultBox.insert(END, line)
	f.close()
	os.system(filterd_textfile)

#For GUI design	
window = Tkinter.Tk()
window.title('PDF Layout Analysis')
window.geometry("1920x1080")
window.resizable(width=True, height=True)
width=1920
height=1080

#Set Background Image
image = PIL.Image.open('lt.jpg')
if image.size != (width, height):
    image = image.resize((width, height), PIL.Image.ANTIALIAS)
image = ImageTk.PhotoImage(image)
bg_label = Tkinter.Label(window, image = image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = image

L1 = Label(window, text="PLayout: Scholarly PDF Layout Analysis",fg='darkviolet')
Labelfont = ('times', 40, 'bold','italic')
L1.config(font=Labelfont)
L1.place(x=300, y=30)

L2 = Label(window, text="Select PDF",fg='Blue',padx = 1, pady = 5)
L2.place(x=100, y=120)
labelfont = ('times', 13, 'bold')
L2.config(font=labelfont)

dirBut = Button(window, text='Choose File', command = choose_file, highlightcolor='yellow')
dirBut.place(x=220, y=120)

E1 = Entry(window, bd =10,width=30)
E1.place(x=300, y=120)

TitleBut = Button(window, text='Title',command = Display_Title ,state=DISABLED, highlightcolor='blue',bg='yellow',)
TitleBut.place(x=400, y=200)

AbstractBut = Button(window, text='Abstract',command = Display_Abstract ,state=DISABLED, highlightcolor='blue',bg='yellow')
AbstractBut.place(x=500, y=200)

MetadataBut = Button(window, text='Metadata',command = Display_Metadata ,state=DISABLED, highlightcolor='blue',bg='yellow')
MetadataBut.place(x=600, y=200)

BodytextBut = Button(window, text='Bodytext',command = Display_Bodytext ,state=DISABLED, highlightcolor='blue',bg='yellow')
BodytextBut.place(x=700, y=200)

ConclusionBut = Button(window, text='Conclusion',command = Display_Conclusion ,state=DISABLED, highlightcolor='blue',bg='yellow')
ConclusionBut.place(x=800, y=200)

ReferencesBut = Button(window, text='References',command = Display_References ,state=DISABLED, highlightcolor='blue',bg='yellow')
ReferencesBut.place(x=900, y=200)

pdftotextBut = Button(window, text='Pdf To Text',command = Display_pdftotext ,state=DISABLED, highlightcolor='blue',bg='yellow')
pdftotextBut.place(x=600, y=300)

OutputBut = Button(window, text='Labelled Text',command = Display_Output ,state=DISABLED, highlightcolor='blue',bg='yellow')
OutputBut.place(x=700, y=300)

FilterBut = Button(window, text='Filtered Text',command = Display_filter ,state=DISABLED, highlightcolor='blue',bg='yellow')
FilterBut.place(x=800, y=300)

ResultBox = Text(window, height=50, width=150)
ResultBox.place(x=90, y=400)

window.mainloop()		
		
print("Pdf layout analysis is successfully done!")




