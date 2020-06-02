import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, StringVar,PhotoImage
import time
BACKGROUND_LIGHT = "Light"
BACKGROUND_DARK = "Dark"
class TimerDisplay(tk.Toplevel):
    def __init__(self,parent,bg=BACKGROUND_DARK,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)


        self.timer_running_flag = 0
        self.flash_color = 0
        s = ttk.Style()
        s.theme_use('clam')
        if bg == BACKGROUND_DARK:
            bg_color = 'deepskyblue4'
            s.configure('time.Label', background='deepskyblue4', foreground='snow', font=('arial', 30, 'bold'))
            s.configure('flash.Label', background='deepskyblue4', foreground='cyan', font=('arial', 60, 'bold'))
            s.configure('timer.Label', background='deepskyblue4', foreground='snow',
                        font=('arial', 60, 'bold'))
            s.configure('minutes.Label', background='deepskyblue4', foreground='snow',
                        font=('arial', 8, 'bold'))
            s.configure('timer.TButton', background='deepskyblue4', foreground='snow',borderwidth=0)
            s.map('timer.TButton', background=[('pressed', 'deepskyblue4'),('active', '!disabled', 'cyan') ],
                  foreground=[('pressed', 'snow'), ('active', 'snow')])
        else:
            bg_color = 'beige'
            s.configure('time.Label', background='beige', foreground='firebrick', font=('arial', 30, 'bold'))
            s.configure('flash.Label', background='beige', foreground='turquoise', font=('arial', 60, 'bold'))
            s.configure('timer.Label', background='beige', foreground='firebrick',
                        font=('arial', 60, 'bold'))
            s.configure('timer.TButton', background='beige', foreground='firebrick', borderwidth=0)
            s.map('timer.TButton', background=[('pressed', 'snow'), ('active', '!disabled', 'snow')],
                  foreground=[('pressed', 'firebrick'), ('active', 'firebrick')])


        self.configure(background=bg_color,borderwidth=2,relief=tk.GROOVE)
        #parent.configure(background=bg_color)
        self.time_val = StringVar()
        self.minutes_val = StringVar()
        self.minutes_val.set('00')
        self.time_label = ttk.Label(self,textvariable=self.time_val,style="time.Label")
        self.timer_control_label = ttk.Label(self, textvariable=self.minutes_val, style="timer.Label")
        self.minutes_label = ttk.Label(self, text="in minutes", style="minutes.Label")
        self.image_plus = PhotoImage(file="../images/signs_plus_real.png")
        self.image_minus = PhotoImage(file="../images/signs_minus_real.png")
        self.image_start = PhotoImage(file="../images/power-button.png")
        self.timer_plus_button = ttk.Button(self,text="",image=self.image_plus,style="timer.TButton",command=self.add_minutes)
        self.timer_minus_button = ttk.Button(self, text="", image=self.image_minus,style="timer.TButton",command=self.reduct_minutes)
        self.timer_start_button = ttk.Button(self, text="", image=self.image_start,style="timer.TButton",command=self.timer_control)
        self.time_display()
        self.minutes_label.pack(side=tk.BOTTOM, pady=5, padx=0)
        self.timer_start_button.pack(side=tk.BOTTOM, pady=0,anchor=tk.S)

        self.timer_minus_button.pack(side=tk.LEFT,pady = 30)

        self.timer_control_label.pack(side=tk.LEFT,pady= 2,padx=10)
        self.timer_plus_button.pack(side=tk.RIGHT, pady = 30)





    def add_minutes(self):
        minutes = int(self.minutes_val.get())
        if  minutes < 100 :
            if minutes < 9:
                self.minutes_val.set('0'+str(minutes+1))
            else:
                self.minutes_val.set(str(minutes+1))
        else:
            self.minutes_val.set('00')

    def reduct_minutes(self):
        minutes = int(self.minutes_val.get())
        if minutes > 0:
            if minutes < 10:
                self.minutes_val.set('0'+str(minutes - 1))
            else:
                self.minutes_val.set(str(minutes - 1))
        else:
            self.minutes_val.set(str('00'))

    def time_display(self):
        self.time_val.set(time.strftime("%I:%M %p"))
        self.time_label.pack()
        if (self.timer_running_flag == 1):
            if (self.flash_color == 0):
                self.timer_control_label.configure(style="flash.Label")
                self.flash_color = 1
            else:
                self.timer_control_label.configure(style="timer.Label")
                self.flash_color = 0
        else:
            self.timer_control_label.configure(style="timer.Label")
        self.after(1000,self.time_display)

    def timer_control(self):
        self.timer_running_flag = 1
        self.minutes_val.set(str(int(self.minutes_val.get()) + 1))
        self.run_timer()

    def run_timer(self):
        self.reduct_minutes()
        self.timer_start_button.configure(state="disabled")
        self.timer_minus_button.configure(state="disabled")
        self.timer_plus_button.configure(state="disabled")
        if (int(self.minutes_val.get()) == 0):
            self.timer_start_button.configure(state="normal")
            self.timer_minus_button.configure(state="normal")
            self.timer_plus_button.configure(state="normal")
            self.timer_running_flag = 0

            file_beep_path = os.path.abspath(os.path.join(os.getcwd(), "..", "images", "beep-12.wav"))

            if sys.platform == "win32":
                os.startfile(file_beep_path)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, file_beep_path])
            return

        self.after(60000, self.run_timer)


if __name__== "__main__":
    timer_app = tk.Tk()
    timer_app.title("Timer")
    timer_app.geometry("250x250")
    frame = TimerDisplay(timer_app)
    frame.pack()
    timer_app.mainloop()



