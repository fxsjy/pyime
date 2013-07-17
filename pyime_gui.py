from Tkinter import *
import os
import string
import tkFont
import pyime

alphabets='abcdefghijklmnopqrstuvwxyz'


def lookup_result(word):
    result = "\n".join( pyime.guess_words(word))
    return result

def on_press(event):
    global index,E1,T1
    word = E1.get().encode('utf-8')
    result = lookup_result(word)
    T1.delete(1.0,END)
    T1.insert(END,result)

def on_alt_d(event):
    global E1
    E1.focus_set()
    E1.select_range(0, END)

def on_esc(event):
    global E1
    E1.delete(0, END)

root = Tk()
root.title("pyime: a prototype of Chinese Input Method")
root.resizable(0,0)
try:
    root.wm_iconbitmap(os.path.normpath(os.path.join(os.getcwd(),_localDir,'icon')))
except:
    pass


frame1 = Frame(root,width=480,height=25)
frame1.pack_propagate(0)
frame1.pack()
frame2 = Frame(root,width=480,height=480)
frame2.pack_propagate(0)
frame2.pack()

L1 = Label(frame1,text=">>")
L1.pack(side=LEFT)
E1 = Entry(frame1,width=60,font=tkFont.Font(size=16,weight='bold'))
E1.pack(side=RIGHT,expand=True)
E1.focus_set()
T1 = Text(frame2,height=480,wrap='word')
T1.pack(expand=True)

E1.bind("<KeyRelease>",on_press)
root.bind("<Alt-d>",on_alt_d)
root.bind("<Escape>",on_esc)

if __name__ == "__main__":
    root.mainloop()
