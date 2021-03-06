import tkinter as tk
from tkinter import ttk,StringVar
import DataCaptureDashboard


class MagicLeaderBoard(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(background='')
        s = ttk.Style(self)
        s.configure('Red.TLabelframe', background='gray16')
        s.configure('Red.TLabelframe.Label', font=('courier', 12, 'bold','italic'))
        s.configure('Red.TLabelframe.Label', foreground='beige')
        s.configure('Red.TLabelframe.Label', background='gray16')

        s.configure('Blue.TButton', background='firebrick', foreground='snow')
        s.map('Blue.TButton', background=[('active', '!disabled', 'peru'), ('pressed', 'firebrick')],
              foreground=[('pressed', 'snow'), ('active', 'snow')])
        s.configure('TScrollbar', background='gray16', foreground='aquamarine')
        s.map('TScrollbar', background=[('active', '!disabled', 'gray16'), ('pressed', 'gray16')],
              foreground=[('pressed', 'aquamarine'), ('active', 'aquamarine')])



       # self.leaderboard = ttk.LabelFrame(self, text = "Class Leaderboard", width=parent.screen_width/4, height=parent.screen_height,borderwidth=8,relief=tk.GROOVE,style='Red.TLabelframe')
        self.c_canvas= tk.Canvas(self,background='gray16')

        self.c_canvas.grid(row=0,column=0,columnspan=3)
        self.leaderboard = tk.Frame(self.c_canvas, width=370,
                                          height=300,
                                          background='gray16')
        self.dataframe= tk.Frame(self.leaderboard)
        self.dataframe.configure(background='beige')
        self.refreshbutton = ttk.Button(self.dataframe,text="Refresh",style='Blue.TButton',command=self.refresh_data,cursor="arrow")
       # self.savebutton = ttk.Button(self.dataframe,text="Save",style='Blue.TButton',command=self.save_data,cursor="arrow")
        #self.dataframe.grid(row=0,column=0,columnspan=3)
        #self.refreshbutton.grid(row=0,column=0)
        #self.savebutton.grid(row=0,column=1,padx=5)

        self.scrollbar = ttk.Scrollbar(self, style='TScrollbar')
        self.c_canvas.config(yscrollcommand=self.scrollbar.set)

        self.c_canvas.create_window((0, 0), window=self.leaderboard, anchor='nw')
        self.leaderboard.bind("<Configure>", self.c_function)
        self.scrollbar.config(command=self.c_canvas.yview)
        #self.leaderboard.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.scrollbar.grid(row=0, column=3, sticky="nsew")

        self.headernamelabel = ttk.Label(self.leaderboard, text="Name", font = ('TkDefaultFont', 16),background='gray16', foreground = 'snow')
        self.headerbadgelabel = ttk.Label(self.leaderboard, text="Badge", font=('TkDefaultFont', 16),background='gray16', foreground='snow')
        self.headerpointslabel = ttk.Label(self.leaderboard, text="Points", font=('TkDefaultFont', 16),background='gray16', foreground='snow')

       # self.headernamelabel.grid(row=1, column=0, padx=10, pady=2)
       # self.headerbadgelabel.grid(row=1, column=1,padx=10, pady=2)
       # self.headerpointslabel.grid(row=1, column=2,padx=10, pady=2)
        self.refresh_data()

    def c_function(self,event):
       self.c_canvas.configure(scrollregion=self.c_canvas.bbox("all"),width=380,height=320)

    def refresh_data(self):

        self.spinboxvalue = []
        self.list_points = []
       # self.leaderboard.configure(state="normal")
        list_names = DataCaptureDashboard.class_info()
        rowindex = 0
        self.badge_image_medala = tk.PhotoImage(file= '../images/medala.png' )
        self.badge_image_medalb = tk.PhotoImage(file= '../images/medalb.png' )
        self.badge_image_medalc = tk.PhotoImage(file='../images/medalc.png')
        for element in list_names:
            self.datanamelabel = ttk.Label(self.leaderboard, text=element[0].strip(), font = ('TkDefaultFont', 12),
                                           foreground = 'aquamarine',wraplength = 100,background='gray16')
            if element[1].strip() == 'a':
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_medala,background='gray16')
            elif element[1].strip() == 'b':
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_medalb,background='gray16')
            else:
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_medalc,
                                                background='gray16')

            points = StringVar()
            points.set(str(element[2]))
            self.spinboxvalue.append(points)
            print("rowindex"+str(rowindex))
            self.datapointspinner = ttk.Spinbox(self.leaderboard,background='beige',foreground='brown',font=('TkDefaultFont', 12),
                                                from_=0,to=100,textvariable=self.spinboxvalue[rowindex],wrap=True,width=2)

            self.list_points.append((element[0],self.spinboxvalue[rowindex]))

           # self.datapointslabel = ttk.Label(self.leaderboard, text=element[2], font=('TkDefaultFont', 12),
           #                                foreground='PeachPuff2',background='dark slate gray')
            self.datanamelabel.grid(row=rowindex+2, column=0, padx=10, pady=3,sticky=tk.W)
            self.databadgelabel.grid(row=rowindex+2, column=1, padx=10, pady=3)
            self.datapointspinner.grid(row=rowindex+2, column=2, padx=10, pady=3)
            rowindex += 1
           # self.leaderboard.configure(state="disabled")





