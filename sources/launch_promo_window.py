import tkinter as tk
import webbrowser
from tkinter import ttk, Toplevel,PhotoImage




class MagicPromo(Toplevel):
    def __init__(self,parent,image,*args, **kwargs):
        Toplevel.__init__(self,parent,*args, **kwargs)
        self.title("Full Version Promo")
        self.transient(parent)
        self.parent = parent
        self.configure(background="gray20")
        s = ttk.Style(self)
        s.theme_use('clam')
        s.configure('Create.TButton', background='steel blue', foreground='white', font=('helvetica', 12, 'bold'))

        s.map('Create.TButton', background=[('active', '!disabled', 'dark turquoise'), ('pressed', 'white')],
              foreground=[('pressed', 'white'), ('active', 'white')])

        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.p_image = PhotoImage(file=image)
        self.screen_label = ttk.Label(self, image=self.p_image )
        self.website = ttk.Button(self,text="Get Full Version",style="Create.TButton",command=self.launch_wonder_sky)
        self.screen_label.grid(row=0,column=0)
        self.website.grid(row=1, column=0, columnspan=2,pady=10)


    def launch_wonder_sky(self):
        webbrowser.open("http://www.wondersky.in", new=2)
