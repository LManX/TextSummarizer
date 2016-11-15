import sys
from xml.etree.ElementTree import XML
import zipfile
from tkinter import *
from tkinter.filedialog import *
from os.path import splitext
from string import punctuation
import nltk
from RAKE import *
from SemanticSimilarity import *


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
            t = f.read()
            text.delete(0.0,END)
            t = t.encode("latin-1", "replace")
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
            t = '\n\n'.join(paragraphs)
            print(paragraphs)
            text.insert(0.0,'\n\n'.join(paragraphs))
        else:
            print("Oops! not a supported file type.")

def TestRake():
    if text.index(END) != 0: # check if we have text to check
        RAKE.test(text.get(0.0,END))

def copy(event=None):
    text.clipboard_clear()
    t = text.get("sel.first", "sel.last")
    text.clipboard_append(t)
    
def cut(event):
    copy()
    text.delete("sel.first", "sel.last")

def paste(event):
    t = text.selection_get(selection='CLIPBOARD')
    #try:
    t = t.encode("latin-1", "replace")
    #except:     
    text.insert('insert', t)
    return "break"


mGui = Tk() #make an instance of TK
mGui.title("My Python Text Editor/Analyzer")

text = Text(mGui)
text.bind('<Control-c>', copy)
text.bind('<Control-x>', cut)
text.bind('<Control-v>', paste)

scroll = Scrollbar(mGui)
scroll.pack(side=RIGHT, fill=Y)
text.pack(side=LEFT, fill=BOTH, expand=1)

scroll.config(command=text.yview)
text.config(yscrollcommand=scroll.set)

menubar = Menu(mGui)
mGui.config(menu=menubar)

filemenu = Menu(menubar)

filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As...", command=saveAs)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_separator()
filemenu.add_command(label="Run RAKE", command=TestRake)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=mGui.quit)

menubar.add_cascade(label="File", menu=filemenu)


mGui.mainloop()