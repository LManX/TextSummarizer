import sys
from xml.etree.ElementTree import XML
import zipfile
from tkinter import *
from tkinter.filedialog import *
from os.path import splitext
from string import punctuation
import nltk
from RAKE import *


filename = None

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

#method to wipe 
def newFile():
    global filename
    filename = "Untitled"
    text.delete(0.0,END)

def saveFile():
    global filename
    if filename == None:
        filename = "Untitled"

    savename = filename
    savename += ".txt"
    t = text.get(0.0,END)
    f = open(savename, "w")
    f.write(t)
    f.close()

def saveAs():
    f = asksaveasfile(mode="w", defaultextension=".txt")
    t = text.get(0.0,END)
    try:
        f.write(t.rstrip())#try to write the text to the file, and remove whitespace after the last char
    except:
        showerror(title="Oops!", message="Unable to save file...")

def openFile():
    f = askopenfile(mode="r", filetypes=[("Text Files", '.txt'), ("Office Open XML", '.docx')])
    if f != None:
        ext = splitext(f.name)[1]
        if ext == ".txt":
            print(splitext(f.name,)[1])
            t = f.read()
            text.delete(0.0,END)
            text.insert(0.0,t)
        elif ext == ".docx":
            doc = zipfile.ZipFile(f.name)
            xml_Content = doc.read('word/document.xml')
            doc.close()
            tree = XML(xml_Content)

            paragraphs = []
            for paragraph in tree.getiterator(PARA):
                texts = [node.text
                         for node in paragraph.getiterator(TEXT)
                            if node.text]
                if texts:
                    paragraphs.append(''.join(texts))

            text.delete(0.0,END)
            text.insert(0.0,'\n\n'.join(paragraphs))
        else:
            print("Oops! not a supported file type.")

def TestRake():
    RAKE.test()


mGui = Tk() #make an instance of TK
mGui.title("My Python Text Editor/Analyzer")
mGui.minsize(width=400, height = 400)
mGui.maxsize(width=400, height = 400)

text = Text(mGui)
text.pack()

menubar = Menu(mGui)
mGui.config(menu=menubar)

filemenu = Menu(menubar)

filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As...", command=saveAs)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_separator()
filemenu.add_command(label="Test RAKE", command=TestRake)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=mGui.quit)

menubar.add_cascade(label="File", menu=filemenu)


mGui.mainloop()