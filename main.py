import os, glob
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class Window:
    def __init__(self) -> None:
        self.dir = None
        self.window = Tk()
        self.window.title('Tagger')
        self.window.geometry("1000x500")
        self.window.config(background = "white")
        self.button_explore = Button(self.window, text = "Browse Files", command = self.openFolder)
        self.button_explore.grid(column = 1, row = 1)  
        self.button_exit = Button(self.window, text = "Exit", command = exit)
        self.button_exit.grid(column = 2, row = 1)
        self.listFrame = Frame(self.window, width = 500, height = self.window.winfo_height() - self.button_explore.winfo_height())
        self.thumbFrame = Frame(self.window, width = 500, height = self.window.winfo_height() - self.button_explore.winfo_height())
        self.window.bind('<Configure>', self.frameResize)

    def openFolder(self):
        self.dir = filedialog.askdirectory(title = "Select folder to open")
        self.listFilesInFolder()

    def frameResize(self, event = None):
        self.listFrame.config(height=self.window.winfo_height() - self.button_explore.winfo_height(), width = self.window.winfo_width() / 2)
        self.thumbFrame.config(height=self.window.winfo_height() - self.button_explore.winfo_height(), width = self.window.winfo_width() / 2)
        self.thumbFrame.place(relx=0.5, y = self.button_explore.winfo_height())

    def onItemSelection(self, event):
        selection = self.the_listbox.curselection()[0]
        # TODO, change w,h formula
        w, h = (self.listFrame.winfo_width(), self.listFrame.winfo_height())
        thumb = Image.open(self.dir + '/' + self.the_listbox.get(selection))
        if thumb.height > thumb.width:
            w /= thumb.height / thumb.width
        else:
            h /= thumb.width / thumb.height
        thumb = thumb.resize((int(w), int(h)))
        tk_thumb = ImageTk.PhotoImage(thumb)
        for widgets in self.thumbFrame.winfo_children():
            widgets.destroy()
        label = Label(self.thumbFrame, image=tk_thumb)
        label.image = tk_thumb
        label.place(relx=0.5, rely=0.5, anchor=CENTER)


    def listFilesInFolder(self, event = None):
        self.frameResize()
        self.the_listbox = Listbox(self.listFrame, selectbackground="#F24FBF", font=("Calibri", "10"), background="white")
        the_scrollbar = Scrollbar(self.the_listbox,orient=VERTICAL,command=self.the_listbox.yview)
        the_scrollbar.pack(side=RIGHT, fill=Y)
        self.the_listbox.config(yscrollcommand=the_scrollbar.set)
        self.the_listbox.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        self.the_listbox.bind('<<ListboxSelect>>', self.onItemSelection)
        self.listFrame.place(x = 0, y = self.button_explore.winfo_height())


        files = list(filter(os.path.isfile, glob.glob(self.dir + "\*")))
        files.sort(key=os.path.getctime)
        files.reverse()
        files = [file.split("\\")[-1] for file in files]
#        files = os.listdir(os.path.abspath(self.dir))
        for file in files:
            self.the_listbox.insert(END, file)
        self.the_listbox.insert(END, "")
        self.the_listbox.insert(END, "Total Files: " + str(len(files)))

if __name__ == '__main__':
    window = Window()
    window.window.mainloop()