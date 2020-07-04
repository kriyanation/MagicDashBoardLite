import logging
import os
import subprocess
import traceback
import webbrowser
from logging.handlers import RotatingFileHandler

import sys
import tkinter as tk

from tkinter import ttk, PhotoImage, simpledialog

import DataCaptureDashboard

import Timer_Display


import create_explainer_content
import launch_promo_window

import magiccontainer



from PIL import Image, ImageTk

handler = RotatingFileHandler("../MagicLogs.log", maxBytes=1 * 1024 * 1024,
                              backupCount=3)
form = logging.Formatter("%(asctime)s- %(name)s: %(message)s")
logger = logging.getLogger("MagicLogger")
handler.setFormatter(form)
logger.setLevel(logging.WARNING)
logger.addHandler(handler)

BACKGROUND_COLOR = "gray18"
BOX_BACKGROUND_COLOR = "gray21"
BOX_FOREGROUND_COLOR = "white"
FOREGROUND_COLOR = "peachpuff2"
ACTIVE_BUTTON_COLOR = "gray44"
BOX_BUTTON_BACKGROUND_COLOR="dark slate gray"
BOX_BUTTON_FOREGROUND_COLOR= "white"
ACTIVE_BOX_BUTTON_COLOR= "slate gray"


class MagicDashboard(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        logger.info("Entering MagicDashboard Initialize")
        self.configure(background=BACKGROUND_COLOR)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Blue.TButton', background='white', foreground='royalblue4', font=('helvetica', 10, 'bold'),
                    bordercolor="royalblue4")
        s.map('Blue.TButton', background=[('active', '!disabled', 'cyan'), ('pressed', 'white')],
              foreground=[('pressed', 'royalblue4'), ('active', 'royalblue4')])

        s.configure('time.Label', background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        s.configure("dash.TButton",background=BACKGROUND_COLOR,foreground=FOREGROUND_COLOR)
        s.map('dash.TButton', background=[('pressed', FOREGROUND_COLOR), ('active', '!disabled', ACTIVE_BUTTON_COLOR)],
              foreground=[('pressed', FOREGROUND_COLOR), ('active', FOREGROUND_COLOR)])
        s.map('dash1.TButton', background=[('active', '!disabled', ACTIVE_BUTTON_COLOR), ('pressed', FOREGROUND_COLOR)],
             foreground=[('pressed', FOREGROUND_COLOR), ('active', FOREGROUND_COLOR)])

        s.configure('dash.TLabelframe', background=BACKGROUND_COLOR,bordercolor=FOREGROUND_COLOR,borderwidth=3)
        s.configure('dash.TLabelframe.Label', font=('courier', 12, 'bold', 'italic'))
        s.configure('dash.TLabelframe.Label', foreground=FOREGROUND_COLOR,background=BACKGROUND_COLOR)
        s.configure('dashheader.Label', background='steel blue', foreground='snow', font=('courier', 10, 'bold','italic'))
        s.configure('dashdata.Label', background='steel blue', foreground='snow', font=('courier', 50, 'bold'))
        s.configure('dash2header.Label', background='gray16', foreground='snow',
                    font=('comic sans', 12, 'bold', 'italic'))
        s.configure('dash3data.Label', background='steel blue', foreground='snow',
                    font=('courier', 20, 'bold', 'italic'))
        s.configure('dash2data.Label', background='gray16', foreground='snow', font=('courier', 40, 'bold'))
        s.configure('dash4header.Label', background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR,
                    font=('comic sans', 10, 'bold', 'italic'))
        s.configure('dashboxheader.Label', background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR,
                    font=('comic sans', 8, 'bold'))
        s.configure('dashboxbutton.TButton', background=BOX_BUTTON_BACKGROUND_COLOR, foreground=BOX_BUTTON_FOREGROUND_COLOR,
                    font=('comic sans', 8, 'bold'))
        s.map('dashboxbutton.TButton', background=[('active', '!disabled', ACTIVE_BOX_BUTTON_COLOR), ('pressed', BOX_BUTTON_FOREGROUND_COLOR)],
              foreground=[('pressed', BOX_BUTTON_FOREGROUND_COLOR), ('active', BOX_BUTTON_FOREGROUND_COLOR)])
        self.image_logo = PhotoImage(file="../images/logo_bg.png")
        self.logo_button = ttk.Button(self, text="", image=self.image_logo,
                                       style="dash.TButton",width=5,
                                       command=self.launch_website)
        self.Lessons_Frame_Create()
        self.Participants_Frame_Create()
        self.tools_frame_create()
        self.flash_frame_create()
        self.star_frame_create()
        self.logo_button.grid(row=0, column=0,columnspan=2, sticky=tk.N)

    def Participants_Frame_Create(self):
        logger.info("Entering Participants Frame")
        self.participants_group_frame = tk.Frame(self, padx=10, pady=10, highlightthickness=3,
                                            highlightbackground="gray30", highlightcolor="gray30", background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.participants_group_frame.grid(row=2, column=0, pady=10,padx=10,sticky=tk.N)
        self.image_participants = PhotoImage(file="../images/business-class.png")
        self.participants_header_label = tk.Label(self.participants_group_frame, compound=tk.LEFT, image=self.image_participants,
                                             borderwidth=3, highlightcolor="gray18", anchor=tk.W,
                                             text=" Participants", font=("Helvetica", 12, 'bold'),
                                             background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.participants_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)
        self.participants_names_scroll_frame = tk.Frame(self.participants_group_frame,
                                                   background="gray18")
        self.participants_names_scroll_frame.rowconfigure(0, weight=1)
        self.participants_names_scroll_frame.columnconfigure(0, weight=1)
        self.participants_names_scroll_frame.grid(row=1, columnspan=3, sticky=tk.NSEW)
        self.participant_list = DataCaptureDashboard.get_participants()
        participants_index = 0
        self.show_participants_names(self.participants_names_scroll_frame, self.participant_list, participants_index)
        self.class_button = ttk.Button(self.participants_group_frame, text="Maintain",
                                        width=8,
                                        command=self.launch_class_data, style="dashboxbutton.TButton")
        self.bday_button = ttk.Button(self.participants_group_frame, text="Play",
                                      width=8,
                                      command=self.bday_play, style="dashboxbutton.TButton")


        self.class_label = tk.Label(self.participants_group_frame,
                                     borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=20,
                                     text="Classroom Info",
                                     font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                     foreground=BOX_FOREGROUND_COLOR)
        self.bday_label = tk.Label(self.participants_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=20,
                                   text="B'Day Song",
                                   font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)

        self.class_label.grid(row=2, column=1, pady=5)
        self.class_button.grid(row=2, column=2, pady=5)
        self.bday_label.grid(row=3, column=1, pady=5)
        self.bday_button.grid(row=3, column=2, pady=5)
      


    def Lessons_Frame_Create(self):
        logger.info("Entering Lessons Frame Create")
        self.lessons_group_frame = tk.Frame(self, padx=10, pady=10, highlightthickness=3,
                                            highlightbackground="gray30", highlightcolor="gray30", background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.lessons_group_frame.grid(row=1, column=0, padx=10,sticky=tk.N)
        self.image_lessons = PhotoImage(file="../images/books.png")
        self.lessons_header_label = tk.Label(self.lessons_group_frame, compound=tk.LEFT, image=self.image_lessons,
                                             borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=250,
                                             text=" Lessons", font=("Helvetica", 12, 'bold'),
                                             background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.lessons_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)
        self.lessons_image_scroll_frame = tk.Frame(self.lessons_group_frame,
                                                   background="gray18")
        self.lessons_image_scroll_frame.rowconfigure(0, weight=1)
        self.lessons_image_scroll_frame.columnconfigure(0, weight=1)
        self.lessons_image_scroll_frame.grid(row=1, columnspan=3, sticky=tk.NSEW)
        self.title_list = DataCaptureDashboard.get_title_names()
        title_list_index = 0
        self.lesson_image_display_scroll(self.lessons_image_scroll_frame, self.title_list, title_list_index)
        self.create_button = ttk.Button(self.lessons_group_frame, text="Create",
                                        width=6,
                                        command=self.create_lesson, style="dashboxbutton.TButton")
        self.edit_button = ttk.Button(self.lessons_group_frame, text="Edit",
                                      width=6,
                                      command=self.launch_lesson_edit, style="dashboxbutton.TButton")
        self.view_button = ttk.Button(self.lessons_group_frame, text="View",
                                      width=6,
                                      command=self.lessons_list, style="dashboxbutton.TButton")
        self.create_label = tk.Label(self.lessons_group_frame,
                                     borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=20,
                                     text="Create a New Lesson",
                                     font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                     foreground=BOX_FOREGROUND_COLOR)
        self.edit_label = tk.Label(self.lessons_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=20,
                                   text="Edit your Lessons",
                                   font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)
        self.lessons_label = tk.Label(self.lessons_group_frame,
                                      borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=20,
                                      text="List all Lessons",
                                      font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                      foreground=BOX_FOREGROUND_COLOR)
        self.create_label.grid(row=2, column=1, pady=5)
        self.create_button.grid(row=2, column=2, pady=5)
        self.edit_label.grid(row=3, column=1, pady=5)
        self.edit_button.grid(row=3, column=2, pady=5)
        self.lessons_label.grid(row=4, column=1, pady=5)
        self.view_button.grid(row=4, column=2, pady=5)

    def show_participants_names(self, frame,list, n_index):
        logger.info("Entering Show Participants Names")
        if len(list) == 0:
            return
        if (hasattr(self,"participants_names_display")) and self.participants_names_display is not None:
            self.participants_names_display.grid_forget()
        self.participants_names_display = tk.Label(frame, text=list[n_index][0],borderwidth=3, highlightcolor="gray18",
                                             font=("Helvetica", 14, 'bold'),width=20,height=1,
                                             background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        self.participants_names_display.grid(row=0, column=0)
        if (n_index == len(list)-1):
            return
        else:
           n_index += 1

        self.after(5000, self.show_participants_names, frame, list, n_index)



    def flash_image_display_scroll(self,frame,list,index):
        logger.info("Entering Flash Image Display")
        try:
            if hasattr(self,"flash_display_lessons"):
                self.flash_display_lessons.grid_forget()
            self.flash_display_lessons = tk.Label(frame,text=list[index][1],width=20,height=1,
                                             font=("Helvetica", 14, 'bold'),
                                             background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
            self.flash_display_lessons.grid(row=0,column=0)
        except:
            logger.info("Flash Term could not be found")
            logger.exception("Flash Term not be opened - Flashcards Dashboard")
        if index == len(list) - 1:
            return
        else:
            index += 1
        self.after(10000,self.flash_image_display_scroll,frame,list,index)

    def lesson_image_display_scroll(self,frame,list,index):
        logger.info("Entering Lesson Image Display Scroll")
       
        try:
            if hasattr(self,"image_display_lessons"):
                self.image_display_lessons.grid_forget()
            self.image_display_lessons = tk.Label(frame,text=list[index][1],width=20,height=1,
                                             font=("Helvetica", 14, 'bold'),
                                             background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
            self.image_display_lessons.grid(row=0,column=0)
        except:
            logger.info("Title Lesson not be found or opened")
            logger.exception("Lesson Title could not be opened")
        if index == len(list) - 1:
            return
        else:
            index += 1
        self.after(7000,self.lesson_image_display_scroll,frame,list,index)

    def launch_content(self):
        lp = launch_promo_window.MagicPromo(self,image="../images/repository_screen.png")


    def launch_website(self):
        webbrowser.open_new_tab("http://www.wondersky.in/")


    def bday_play(self):
        lp = launch_promo_window.MagicPromo(self, image="../images/bday_screen.png")

    def show_names(self,frame, names,n_index):
            logger.info("Entering show names for starts")
            if(n_index == len(names)):
                return
            if len(names) == 0:
                return
            self.leader_data_label = tk.Label(frame,text=names[n_index][0],borderwidth=3, highlightcolor="gray16", width=25,
                                             font=("Helvetica", 10, 'bold'),height=1,
                                             background="gray16", foreground=FOREGROUND_COLOR)
            self.leader_data_label.grid(row=1,column=0)
            self.after(6000,self.show_names,frame,names,n_index+1)

    def launch_lesson_edit(self):
        lp = launch_promo_window.MagicPromo(self,image="../images/edit_screen.png")


    def launch_flashcard(self):
        lp = launch_promo_window.MagicPromo(self,image="../images/flashcard_screen.png")

    def launch_assessment_pdf(self):
        lp = launch_promo_window.MagicPromo(self,image="../images/assessment_screen.png")
    def launch_class_data(self):
        lp = launch_promo_window.MagicPromo(self, image="../images/leader_quote_screen.png")

    def launch_player(self):
        launch_player = magiccontainer.MagicApplication(self)
        launch_player.geometry("1400x800+120+20")

    def launch_pdf_notes(self):
        lp = launch_promo_window.MagicPromo(self,image="../images/audio_print_screen.png")

    def lessons_list(self):
        lp = launch_promo_window.MagicPromo(self,image="../images/lesson_screen.png")

    def create_lesson(self):
        launch_Create = create_explainer_content.MagicWizard(self)
        launch_Create.geometry("1300x700+20+20")

    def launch_timer(self):
        launch_timer = Timer_Display.TimerDisplay(self)
        launch_timer.resizable(width=False,height=False)
        launch_timer.attributes("-topmost", True)
        launch_timer.geometry("240x250+20+20")

    def tools_frame_create(self):
        logger.info("Entering Tools Frame Create")
        self.tools_group_frame = tk.Frame(self, padx=10, pady=10,highlightthickness=3,
                                                 highlightbackground="gray30", highlightcolor="gray30",
                                                 background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.tools_group_frame.grid(row=2, column=1, padx=10,pady = 10,sticky=tk.N)
        self.image_tools = PhotoImage(file="../images/tools.png")
        self.tools_header_label = tk.Label(self.tools_group_frame, compound=tk.LEFT,
                                                  image=self.image_tools,
                                                  borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=250,
                                                  text=" Teacher Tools", font=("Helvetica", 12, 'bold'),
                                                  background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.tools_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)

        self.content_button = ttk.Button(self.tools_group_frame, text="Save",
                                       width=8,
                                       command=self.launch_content, style="dashboxbutton.TButton")
        self.print_notes_button = ttk.Button(self.tools_group_frame, text="Notes",
                                      width=8,
                                      command=self.launch_pdf_notes, style="dashboxbutton.TButton")
        self.print_assessment_button = ttk.Button(self.tools_group_frame, text="Assess",
                                             width=8,
                                             command=self.launch_assessment_pdf, style="dashboxbutton.TButton")


        self.content_label = tk.Label(self.tools_group_frame,
                                    borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                    text="Images and Videos",
                                    font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                    foreground=BOX_FOREGROUND_COLOR)
       

        self.notes_label = tk.Label(self.tools_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="Audio and Print Notes",
                                   font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)

        self.assessment_label = tk.Label(self.tools_group_frame, borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="Assessments",
                                   font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)

        self.content_label.grid(row=1, column=0, pady=5)
        self.content_button.grid(row=1, column=1, pady=5)



        self.notes_label.grid(row=4, column=0, pady=5)
        self.print_notes_button.grid(row=4, column=1, pady=5)

        self.assessment_label.grid(row=5, column=0, pady=5)
        self.print_assessment_button.grid(row=5, column=1, pady=5)

    def flash_frame_create(self):
        logger.info("Entering Flash Card Frame Create")
        self.flash_group_frame = tk.Frame(self, padx=10, pady=10,highlightthickness=3,
                                                 highlightbackground="gray30", highlightcolor="gray30",
                                                 background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.flash_group_frame.grid(row=1, column=1, padx=10,pady = 0,sticky=tk.N)
        self.image_flash = PhotoImage(file="../images/chalkboard.png")
        self.flash_header_label = tk.Label(self.flash_group_frame, compound=tk.LEFT,
                                                  image=self.image_flash,
                                                  borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=250,
                                                  text=" Interactions", font=("Helvetica", 12, 'bold'),
                                                  background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.flash_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)
        self.flash_image_scroll_frame = tk.Frame(self.flash_group_frame,
                                                   background="gray18")
        self.flash_image_scroll_frame.rowconfigure(0, weight=1)
        self.flash_image_scroll_frame.columnconfigure(0, weight=1)
        self.flash_image_scroll_frame.grid(row=1, columnspan=3, sticky=tk.NSEW)
        self.flash_list = DataCaptureDashboard.get_flash_names()
        flash_list_index = 0
        self.flash_image_display_scroll(self.flash_image_scroll_frame, self.flash_list, flash_list_index)
        self.play_button = ttk.Button(self.flash_group_frame, text="Start",
                                       width=7,
                                       command=self.launch_player, style="dashboxbutton.TButton")
        self.cards_button = ttk.Button(self.flash_group_frame, text="Play",
                                      width=7,
                                      command=self.launch_flashcard, style="dashboxbutton.TButton")


        self.play_label = tk.Label(self.flash_group_frame,
                                    borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                    text="Lesson for your Class",
                                    font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                    foreground=BOX_FOREGROUND_COLOR)
        self.cards_label = tk.Label(self.flash_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="A game of Flashcards",
                                   font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)
        self.timer_button = ttk.Button(self.flash_group_frame, text="Timer",
                                                  width=8,
                                                  command=self.launch_timer, style="dashboxbutton.TButton")
        self.timer_label = tk.Label(self.flash_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="Launch Timer",
                                   font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)
        self.play_label.grid(row=2, column=0, pady=5)
        self.play_button.grid(row=2, column=1, pady=5)

        self.cards_label.grid(row=3, column=0, pady=5)
        self.cards_button.grid(row=3, column=1, pady=5)

        self.timer_label.grid(row=4,column=0,pady=5)
        self.timer_button.grid(row=4,column=1,pady=5)

    def star_frame_create(self):
        logger.info("Entering Starts Frame Create")
        self.star_group_frame = tk.Frame(self, padx=10, pady=10, highlightthickness=3,
                                                 highlightbackground="gray30", highlightcolor="gray30",
                                                 background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.star_group_frame.grid(row=3, column=0,columnspan=3,sticky=tk.N)
        self.image_star = PhotoImage(file="../images/cup_icon.png")
        self.star_header_label = tk.Label(self.star_group_frame, compound=tk.LEFT,
                                                  image=self.image_star,
                                                  borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=250,
                                                  text=" Celebrate", font=("Helvetica", 12, 'bold'),
                                                  background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.star_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)
        self.star_image_frame = tk.Frame(self.star_group_frame,
                                                   background="gray16")
        self.star_image_frame.rowconfigure(0, weight=1)
        self.star_image_frame.columnconfigure(0, weight=1)
        self.star_image_frame.grid(row=1, columnspan=3, sticky=tk.NSEW)
        self.star_list = DataCaptureDashboard.get_badge_1_count()
        self.star_image = PhotoImage(file="../images/stars.png")
        self.star_image_display=tk.Label(self.star_image_frame,image=self.star_image,borderwidth=3, highlightcolor="gray16",
                                           background="gray16", foreground=BOX_FOREGROUND_COLOR)
        self.star_image_display.grid(row=0,column=0,pady=2)
        star_image_index = 0
        self.show_names(self.star_image_frame, self.star_list, star_image_index)




if __name__== "__main__":
    dashboard_app = tk.Tk()
    dashboard_app.configure(background="gray18")
    dashboard_app.title("Learning Room Dashboard")
    screen_width = dashboard_app.winfo_screenwidth()
    screen_height = dashboard_app.winfo_screenheight()

    screen_half_width = int(dashboard_app.winfo_screenwidth())
    screen_half_height = int(dashboard_app.winfo_screenheight())
    dashboard_app.geometry("1300x850+200+20")
    frame = MagicDashboard(dashboard_app)

    #dashboard_app.rowconfigure(0,weight=1)
    dashboard_app.columnconfigure(0, weight=1)
    frame.grid(row=0,column=0,sticky=tk.EW)
    dashboard_app.mainloop()

