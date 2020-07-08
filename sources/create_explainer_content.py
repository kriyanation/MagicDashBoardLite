import logging
import tkinter as tk
import traceback

from tkinter import ttk,messagebox,Toplevel


from PIL import Image, ImageTk

from Lesson_File_Manager_Create import LessonFileManager



from tkinter import Label, Frame, Entry, Button, Text, OptionMenu, StringVar, filedialog, IntVar, PhotoImage
import sqlite3, os,sys

logger = logging.getLogger("MagicLogger")
fileroot = os.path.abspath(os.path.join(os.getcwd(),".."))
db = fileroot+os.path.sep+"MagicRoom.db"
try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Lesson_Title from Magic_Science_Lessons"
    cur.execute(sql)
except(sqlite3.OperationalError):
    messagebox.showerror("DB Error", "Check your DB Configuration")
    logger.exception("There was an error in checkng for DB connection")
else:
    connection.close()


class MagicWizard(tk.Toplevel):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        logger.info("Inside Create Initialize")
        self.index = 0
        self.factual_index = 1
        self.factual_button_one = None
        self.data_collector = {}
        self.rowindex = 4
        self.title_frame = Frame(self)
        self.title_frame.configure(background='gray20')
        self.configure(background='gray20')

        s = ttk.Style()
        s.theme_use('clam')

        s.configure('Create.TLabelframe', background='gray22')
        s.configure('Create.TLabelframe.Label', font=('helvetica', 14, 'bold'))
        s.configure('Create.TLabelframe.Label', background='gray22',foreground='white')

        s.configure('Firebrick.Label',background='gray22',foreground='white',font=('helvetica', 9, 'bold'))

        s.configure('Create.TButton', background='steel blue', foreground='white',font=('helvetica', 12, 'bold'))
        s.configure('Green.TMenubutton', background='white', foreground='gray55')

        s.map('Create.TButton', background=[('active', '!disabled', 'dark turquoise'), ('pressed', 'white')],
              foreground=[('pressed', 'white'), ('active', 'white')])

        self.data_collector['Date'] = ''
        self.data_collector['Lesson_Type'] = 'Science'
        self.data_collector['Lesson_Template'] = 'Hogwarts'
        self.data_collector['Lesson_Title'] = ''
        self.data_collector['Title_Image'] = ''
        self.data_collector['Title_Video'] = ''
        self.data_collector['Title_Running_Notes'] = ''
        self.data_collector['Title_Running_Notes_Language'] = ''
        self.data_collector['Factual_Term1'] = ''
        self.data_collector['Factual_Term1_Description'] = ''
        self.data_collector['Factual_Term2'] = ''
        self.data_collector['Factual_Term2_Description'] = ''
        self.data_collector['Factual_Term3'] = ''
        self.data_collector['Factual_Term3_Description'] = ''
        self.data_collector['Factual_Image1'] = ''
        self.data_collector['Factual_Image2'] = ''
        self.data_collector['Factual_Image3'] = ''
        self.data_collector['Application_Mode'] = ''
        self.data_collector['Application_Steps_Number'] = 0
        self.data_collector['Application_Step_Description1'] = ''
        self.data_collector['Application_Step_Description2'] = ''
        self.data_collector['Application_Step_Description3'] = ''
        self.data_collector['Application_Step_Description4'] = ''
        self.data_collector['Application_Step_Description5'] = ''
        self.data_collector['Application_Step_Description6'] = ''
        self.data_collector['Application_Step_Description7'] = ''
        self.data_collector['Application_Step_Description8'] = ''
        self.data_collector['Application_Steps_Widget_1'] = ''
        self.data_collector['Application_Steps_Widget_2'] = ''
        self.data_collector['Application_Steps_Widget_3'] = ''
        self.data_collector['Application_Steps_Widget_4'] = ''
        self.data_collector['Application_Steps_Widget_5'] = ''
        self.data_collector['Application_Steps_Widget_6'] = ''
        self.data_collector['Application_Steps_Widget_7'] = ''
        self.data_collector['Application_Steps_Widget_8'] = ''
        self.data_collector['Answer_Key'] = ''
        self.data_collector['Video_Audio_Assessment_Flag'] = 0
        self.data_collector['Application_Video_Link'] = ''
        self.data_collector['Application_Video_Running_Notes'] = ''
        self.data_collector["Questions"] = ''
        self.data_collector["Number_Questions"] = 0
        self.title_image_display = None

        self.filename_vid_title_full= ""
        self.filename_img_title_full = ""

        self.filename_img_fact1_full= ""
        self.filename_img_fact2_full = ""
        self.filename_img_fact3_full = ""

        self.filename_img_app1_full= ""
        self.filename_img_app2_full = ""
        self.filename_img_app3_full = ""
        self.filename_img_app4_full= ""
        self.filename_img_app5_full = ""
        self.filename_img_app6_full = ""
        self.filename_img_app7_full= ""
        self.filename_img_app8_full = ""
        self.bottom_frame = Frame(self,background="gray22")
        self.factual_frame = Frame(self)
        self.factual_frame.configure(background='gray22')
        self.apply_frame = Frame(self)
        self.apply_frame.configure(background='gray22')
        self.apply_activity_frame = Frame(self.apply_frame)
        self.apply_activity_frame.configure(background='gray22')
        self.apply_activity_steps_frame = Frame(self.apply_activity_frame)
        self.apply_activity_steps_frame.configure(background='gray22')
        self.create_frame = Frame(self)
        self.create_frame.configure(background='gray22')
        self.factual_term_text1 = Entry(self.factual_frame)
        self.factual_term_desc_text1 = Text(self.factual_frame, wrap=tk.WORD, width=30, height=5)
        self.factual_term_text2 = Entry(self.factual_frame)
        self.factual_term_desc_text2 = Text(self.factual_frame, wrap=tk.WORD, width=30, height=5)
        self.factual_button = ttk.Button(self.factual_frame, text='Add One More', command=self.add_factual_one, style='Create.TButton')
        self.factual_button.grid(row=4, column=3)
        self.htmlvar = StringVar()
        self.header_var = StringVar()
        self.header_label = tk.Label(self, textvariable=self.header_var, font=("helvetica", 12, "bold"), foreground="aquamarine",
                                      background="gray22")  # style="Create.TLabelframe.Label"
        self.header_label.pack(pady=5)
        self.header_var.set(
            "Activate Prior Knowledge - Introduce, Ask Questions, Play a related Video and Show a related visual of the topic")
        self.var_video_audio = IntVar()
        self.question_text = Entry(self.create_frame, width=10)
        # create_test_entry = Entry(create_frame, width=20)
        self.create_question_text = Text(self.create_frame, wrap=tk.WORD, width=70, height=30)
        self.title_frame_create()
        self.add_factual()
        self.add_apply_frame()
        self.add_create_frame()
        self.next_button = ttk.Button(self.bottom_frame, text='Next', command=self.next_page, style='Create.TButton')
        self.back_button = ttk.Button(self.bottom_frame, text="Back", command=self.previous_page, style='Create.TButton')

        self.bottom_frame.pack(side='bottom')
        self.next_button.pack(side='right', padx=5)
        self.back_button.pack(side='left')



    def add_title_video(self):
        logger.info("Inside add_title_video of create widget")
        self.filename_vid_title_full = filedialog.askopenfilename(initialdir=fileroot,title='Select Video',parent=self)
        self.filename_vid_title = os.path.basename(self.filename_vid_title_full)
        print(self.filename_vid_title)
        if (self.filename_vid_title != ''):
            self.title_image_video_url.insert(0,self.filename_vid_title)
            self.data_collector['Title_Video'] = self.title_image_video_url.get()
    def add_title_image(self):
        logger.info("Inside add_title_image of create widget")
        self.filename_img_title_full = filedialog.askopenfilename(initialdir=fileroot,title='Select Image',parent=self)
        self.title_image = Image.open(self.filename_img_title_full)
        self.title_image.thumbnail((100,100))
        self.title_image_display = ImageTk.PhotoImage(self.title_image)
        self.filename_img_title = os.path.basename(self.filename_img_title_full)
        print(self.filename_img_title)
        if (self.filename_img_title != ''):
            self.img_title_label = ttk.Label(self.title_frame, image=self.title_image_display,background="gray22")#style="Create.TLabelframe.Label"
            self.img_title_label.grid(row=2,column=3,pady=2,padx = 2)
            self.data_collector['Title_Image'] = self.filename_img_title

    def title_frame_create(self):
        logger.info("Inside title frame of create widget")

        self.language_notes = StringVar()
        self.language_notes.set("English")
        self.title_doc = ttk.Label(self.title_frame, text="Welcome to the Learning Wizard. Here, we shall be creating your topic introduction page. Add an image and a video which "
                                                "you want to start your topic with.\nWe can also paste text in any language for introducing the topic."
                                                ,
                                                wraplength="300", style='Firebrick.Label')
        self.title_label = ttk.Label(self.title_frame, text="Title",style='Create.TLabelframe.Label')
        self.title_text = Entry(self.title_frame)
        self.title_image_label = ttk.Label(self.title_frame, text="Image Related to Title", style='Create.TLabelframe.Label')
        self.title_image_button = ttk.Button(self.title_frame, text="Add Image",command=self.add_title_image,style='Create.TButton')
        self.title_image_video_label = ttk.Label(self.title_frame, text="Video Related to Title", style='Create.TLabelframe.Label')
        self.title_video_button = ttk.Button(self.title_frame, text="Add Video",command=self.add_title_video,style='Create.TButton')
        self.title_image_url_label = ttk.Label(self.title_frame, text="(OR) youtube URL", style='Create.TLabelframe.Label')
        self.title_image_video_url = ttk.Entry(self.title_frame)
        self.title_video_notes_lang = ttk.OptionMenu(self.title_frame, self.language_notes,"English", "Hindi", "Kannada", "Tamil",style='Create.TButton')
        self.title_running_notes_label = ttk.Label(self.title_frame, text="Topic Introduction \n(2 to 3 sentences)", style='Create.TLabelframe.Label')
        self.title_running_notes = Text(self.title_frame,wrap=tk.WORD, width=30, height=5,pady=2)
        self.title_frame.pack()
        self.title_doc.grid(row=0, column=0,rowspan=4, pady=10,padx=50)
        self.title_label.grid(row=1, column=1,pady=50,sticky=tk.W)
        self.title_text.grid(row=1, column=2,pady=5,padx=5,sticky=tk.W)
        self.title_image_label.grid(row=2,column=1,pady=2,sticky=tk.W)
        self.title_image_button.grid(row=2,column=2,pady=2,padx=5,sticky=tk.W)
        self.title_image_video_label.grid(row=3,column=1,pady=2,sticky=tk.W)
        self.title_video_button.grid(row=3,column=2,pady=2,padx=5,sticky=tk.W)

        self.title_image_url_label.grid(row=3,column=3,pady=2,sticky=tk.W)
        self.title_image_video_url.grid(row=3,column=4,pady=2,padx=5,sticky=tk.W)
        self.title_running_notes_label.grid(row=4,column=1,pady=2,sticky=tk.W)
        self.title_running_notes.grid(row=4,column=2,pady=2,padx=5,columnspan=2,sticky=tk.W)
        #title_video_notes_lang.grid(row=3, column=2,pady=2,padx=2)










    def  add_factual_image(self,id):
        logger.info("Inside add_factual_image of create widget")
        self.filename_img_fact_full = filedialog.askopenfilename(initialdir=fileroot,title='Select Image',parent=self)
        filename_img_fact = os.path.basename(self.filename_img_fact_full)
        print(filename_img_fact)
        print("ID="+str(id))
        factual_image = None
        if (filename_img_fact != ''):
            factual_image = Image.open(self.filename_img_fact_full)
            factual_image.thumbnail((80, 80))


        if id == 0:
            self.factual_image_display1 = ImageTk.PhotoImage(factual_image)
            img_title_label = ttk.Label(self.factual_frame, image=self.factual_image_display1, background="beige")
            img_title_label.grid(row=3, column=1,pady=10,sticky=tk.W)
            self.data_collector['Factual_Image1'] = filename_img_fact
            self.filename_img_fact1_full = self.filename_img_fact_full
        elif id == 1:
            self.factual_image_display2 = ImageTk.PhotoImage(factual_image)
            img_title_label = ttk.Label(self.factual_frame, image=self.factual_image_display2, background="beige")

            img_title_label.grid(row=6, column=1,pady=10,sticky=tk.W)
            self.data_collector['Factual_Image2'] = filename_img_fact
            self.filename_img_fact2_full = self.filename_img_fact_full
        elif id == 2:
            self.factual_image_display3 = ImageTk.PhotoImage(factual_image)
            img_title_label = ttk.Label(self.factual_frame, image=self.factual_image_display3, background="beige")

            img_title_label.grid(row=9, column=1,pady=10,sticky=tk.W)
            self.data_collector['Factual_Image3'] = filename_img_fact
            self.filename_img_fact3_full = self.filename_img_fact_full


    def add_factual(self):
        logger.info("Inside add_factual method of create widget")
        self.factual_page_label = ttk.Label(self.factual_frame,
                  text="Here, we cover the facts or the knowledge aspects.We can introduce new terms or concepts.We can also introduce new vocabulary words."
                       "Each term shall be associated to an image and a short explanation.\n\n\nThree new terms/topcs can be intorduced here as part of one lesson."
                       "\n\n\nIf you need to cover more terms or topics we encourage you"
                       "to create a new lesson for the same. Let us go ahead and add our content!",
                  wraplength="300", style='Firebrick.Label')
        self.factual_term_label = ttk.Label(self.factual_frame, text="Definition or New Term",style='Create.TLabelframe.Label' )
        self.factual_term_text = Entry(self.factual_frame)
        self.factual_term_desc_label = ttk.Label(self.factual_frame, text="Description",style='Create.TLabelframe.Label')
        self.factual_term_desc_text = Text(self.factual_frame,wrap=tk.WORD, width=30, height=5)
        self.factual_term_image_button = ttk.Button(self.factual_frame, text='Add Image', command=lambda id=0: self.add_factual_image(id),style='Create.TButton')
        self.factual_page_label.grid(row=1, column=8,rowspan=10, pady=10,padx=200,sticky=tk.W)
        self.factual_term_label.grid(row=1, column=0,pady=20,sticky=tk.W)
        self.factual_term_text.grid(row=1, column=1,padx=5,sticky=tk.W)
        self.factual_term_desc_label.grid(row=2, column=0,sticky=tk.W)
        self.factual_term_desc_text.grid(row=2, column=1,padx=5,sticky=tk.W)
        self.factual_term_image_button.grid(row=3,column=0,sticky=tk.W)


    def add_factual_one(self):
        logger.info("Inside add_factual_one of create widget")

        self.factual_index += 1
        self.factual_term_label = ttk.Label(self.factual_frame, text="Definition or New Term",style='Create.TLabelframe.Label')

        self.factual_term_desc_label = ttk.Label(self.factual_frame, text="Description",style='Create.TLabelframe.Label')
        self.factual_term_image_button = ttk.Button(self.factual_frame, text='Add Image', command=lambda id=1: self.add_factual_image(id),style='Create.TButton')

        self.factual_term_label.grid(row=4, column=0, pady=10,sticky=tk.W)
        self.factual_term_text1.grid(row=4, column=1,padx=5,sticky=tk.W)
        self.factual_term_desc_label.grid(row=5, column=0,sticky=tk.W)
        self.factual_term_desc_text1.grid(row=5, column=1,padx=5,sticky=tk.W)
        print(self.factual_index)
        self.factual_button.grid_remove()
        self.factual_button_one = ttk.Button(self.factual_frame, text='Add One More', command=self.add_factual_two,style='Create.TButton')
        self.factual_button_one.grid(row=6, column=2,sticky=tk.W)
        self.factual_term_image_button.grid(row=6,column=0,padx=5,sticky=tk.W)






    def add_factual_two(self):
        logger.info("Inside add_factual_two of create widget")
        self.factual_index += 1
        self.factual_button_one.grid_remove()
        self.factual_term_label = ttk.Label(self.factual_frame, text="Definition or New Term", style='Create.TLabelframe.Label')

        factual_term_desc_label = ttk.Label(self.factual_frame, text="Description",style='Create.TLabelframe.Label')
        factual_term_image_button = ttk.Button(self.factual_frame, text='Add Image', command=lambda id=2: self.add_factual_image(id),style='Create.TButton')

        self.rowindex += 3
        print(self.rowindex)
        self.factual_term_label.grid(row=self.rowindex, column=0,pady=10,sticky=tk.W)
        self.factual_term_text2.grid(row=self.rowindex, column=1,padx=5,sticky=tk.W)
        self.rowindex += 1
        self.factual_term_desc_label.grid(row=self.rowindex, column=0,sticky=tk.W)
        self.factual_term_desc_text2.grid(row=self.rowindex, column=1,padx=5,sticky=tk.W)
        self.rowindex += 1
        factual_term_image_button.grid(row=self.rowindex,column=0,sticky=tk.W)
    # factual_button_one.grid(row=rowindex, column=2)


    def add_apply_frame(self):
        logger.info("Inside add_apply_frame of create widget")
        self.apply_page_label = ttk.Label(self.apply_frame,
                  text="Here, we focus on building the skill.\n"
                       
                       "We describe an activity and is a place of highest interaction.You are presented with a drawable whiteboard in the player which is connected to a set of steps. Each step allows an image to appear"
                       " in the whiteboard which can be moved around.\nAn example application can be an experiment which has a set of steps and each step has an image associated with it"
                       " another example is an activity in Language subject where each step is a important line from the poem followed by "
                       " a question.The images can be word or letter clues.You can refer to an external link to open related resources for the activity",
                        wraplength="200", style='Firebrick.Label')
        self.apply_page_label.grid(row=1, column=8,rowspan=10, pady=10,padx=200)
        # apply_term_label = ttk.Label(apply_frame, text="How would you want to show the application?",style='Create.TLabelframe.Label' )
        # selected = StringVar(magic_wizard)
        # selected.set('No Selection')
        # apply_dropdown = ttk.OptionMenu(apply_frame, selected, 'No Selection', 'Activity', 'Video', command=show_steps,style='Green.TMenubutton')
        # apply_term_label.grid(row=1, column=0,pady=10)
        # apply_dropdown.grid(row=1, column=1)
        # print(selected.get())
        self.show_steps('Activity')




    def show_steps(self,selected_string):
        self.step1_text_var = StringVar()
        self.step2_text_var = StringVar()
        self.step3_text_var = StringVar()
        self.step4_text_var = StringVar()
        self.step5_text_var = StringVar()
        self.step6_text_var = StringVar()
        self.step7_text_var = StringVar()
        self.step8_text_var = StringVar()
        if selected_string == 'Activity':
            self.data_collector['Application_Mode'] = selected_string
            for widget in self.apply_activity_frame.winfo_children():
                if widget != self.apply_activity_steps_frame:
                    widget.destroy()

            self.apply_steps_label = ttk.Label(self.apply_activity_frame, text="Number of Steps?", style='Create.TLabelframe.Label')
            self.selected_steps = StringVar()
            self.apply_steps_dropdown = ttk.OptionMenu(self.apply_activity_frame, self.selected_steps, '0', '1', '2', '3', '4', '5', '6', '7',
                                              '8',
                                              command=self.show_individual_steps,style='Green.TMenubutton')
            self.apply_steps_dropdown["menu"].configure(background="white")

            print(selected_string)

            self.selected_steps.set('0')
            self.apply_steps_label.grid(row=0, column=0,pady=10)
            self.apply_steps_dropdown.grid(row=0, column=1)

        if selected_string == 'Video':
            self.data_collector['Application_Mode'] = selected_string
            for widget in self.apply_activity_frame.winfo_children():
                if widget != self.apply_activity_steps_frame:
                    widget.destroy()
            if self.apply_activity_steps_frame is not None and len(self.apply_activity_steps_frame.children) > 1:
                for widget_steps in self.apply_activity_steps_frame.winfo_children():
                    widget_steps.destroy()
            self.video_link_label = ttk.Label(self.apply_activity_frame, text="Video Link",style='Create.TLabelframe.Label' )
            self.video_link_button = ttk.Button(self.apply_activity_frame, text='Add Video',
                                       command=lambda: self.add_video(self.apply_frame),style='Create.TButton')
            self.video_link_notes_label = ttk.Label(self.apply_activity_frame, text="Running Notes", style='Create.TLabelframe.Label' )
            self.video_link_running_notes = Text(self.apply_activity_frame,wrap=tk.WORD, width=30, height=5)
            self.video_link_label.grid(row=1, column=0,pady=10)
            self.video_link_button.grid(row=1, column=1)
            self.video_link_notes_label.grid(row=2, column=0,pady=10)
            self.video_link_running_notes.grid(row=2, column=1)


    def add_video(self,apply_frame):
        self.filename_vid_full = filedialog.askopenfilename(initialdir=fileroot,title='Select Video',parent=self)
        filename_vid = os.path.basename(self.filename_vid_full)
        print(filename_vid)
        if (filename_vid != ''):
            self.vid_label = ttk.Label(self.apply_activity_frame, text=filename_vid, style='Create.TLabelframe.Label')
            self.vid_label.grid(row=1, column=2,pady=3)
            self.data_collector['Application_Video_Link'] = filename_vid



    def show_individual_steps(self,selected_number):
        logger.info("Inside show_individual_steps of create widget")
        if hasattr(self, "number_of_steps"):
            self.data_collector["Application_Step_Description" + str(self.number_of_steps)] = eval("self.step" +
                                                                                                   str(
                                                                                                       self.number_of_steps) +
                                                                                                   "_text_var").get()

        for widget in self.apply_activity_steps_frame.winfo_children():
            widget.destroy()
        self.data_collector['Application_Steps_Number'] = int(selected_number)
        self.number_of_steps = int(selected_number)

        i = 0
        self.step1_label = ttk.Label(self.apply_activity_steps_frame
                                     )
        self.step2_label = ttk.Label(self.apply_activity_steps_frame
                                     )
        self.step3_label = ttk.Label(self.apply_activity_steps_frame
                                     )
        self.step4_label = ttk.Label(self.apply_activity_steps_frame
                                     )
        self.step5_label = ttk.Label(self.apply_activity_steps_frame
                                     )
        self.step6_label = ttk.Label(self.apply_activity_steps_frame
                                     )
        self.step7_label = ttk.Label(self.apply_activity_steps_frame
                                     )
        self.step8_label = ttk.Label(self.apply_activity_steps_frame
                                     )

        self.step_text1 = Entry(self.apply_activity_steps_frame,textvariable=self.step1_text_var)

        self.step_text2 = Entry(self.apply_activity_steps_frame,textvariable=self.step2_text_var)

        self.step_text3 = Entry(self.apply_activity_steps_frame,textvariable=self.step3_text_var)

        self.step_text4 = Entry(self.apply_activity_steps_frame,textvariable=self.step4_text_var)

        self.step_text5 = Entry(self.apply_activity_steps_frame,textvariable=self.step5_text_var)

        self.step_text6 = Entry(self.apply_activity_steps_frame,textvariable=self.step6_text_var)

        self.step_text7 = Entry(self.apply_activity_steps_frame,textvariable=self.step7_text_var)

        self.step_text8 = Entry(self.apply_activity_steps_frame,textvariable=self.step8_text_var)
        self.step_image_button1 = ttk.Button(self.apply_activity_steps_frame, text='Add Image',style='Create.TButton')
        self.step_image_button2 = ttk.Button(self.apply_activity_steps_frame, text='Add Image',style='Create.TButton')
        self.step_image_button3 = ttk.Button(self.apply_activity_steps_frame, text='Add Image',style='Create.TButton')
        self.step_image_button4 = ttk.Button(self.apply_activity_steps_frame, text='Add Image',style='Create.TButton')
        self.step_image_button5 = ttk.Button(self.apply_activity_steps_frame, text='Add Image',style='Create.TButton')
        self.step_image_button6 = ttk.Button(self.apply_activity_steps_frame, text='Add Image',style='Create.TButton')
        self.step_image_button7 = ttk.Button(self.apply_activity_steps_frame, text='Add Image',style='Create.TButton')
        self.step_image_button8 = ttk.Button(self.apply_activity_steps_frame, text='Add Image',style='Create.TButton')
        self.html_link = Entry(self.apply_activity_steps_frame,textvariable=self.htmlvar, width=20)
        self.link_label = ttk.Label(self.apply_activity_steps_frame, text="Add an external link", style='Create.TLabelframe.Label')
        i = 1
        for i in range(self.number_of_steps):
            self.step_label = ttk.Label(self.apply_activity_steps_frame, text="Step Description", style='Create.TLabelframe.Label')
            if i == 0:
                index1 = i
                self.step_text1.bind("<FocusOut>",lambda event, index = i: self.add_step(event,index1))
                self.step_image_button1.config(command=lambda row=i: self.add_image(self.apply_frame, index1))
                self.step_label.grid(row=i, column=0,pady=10,padx=5)
                self.step_text1.grid(row=i, column=1,padx=5)
                self.step_image_button1.grid(row=i, column=3)
                if hasattr(self,"apply_image_preview1") and self.apply_image_preview1 is not None:
                    self.step1_label.configure(image=self.apply_image_preview1)
                    self.step1_label.grid(row=i, column=4, padx=20, pady=10)

            if i == 1:
                index2 = i
                self.step_text2.bind("<FocusOut>",lambda event, index = i: self.add_step(event,index2))
                self.step_image_button2.config(command=lambda row=i: self.add_image(self.apply_frame, index2))
                self.step_label.grid(row=i, column=0,pady=10,padx=5)
                self.step_text2.grid(row=i, column=1,padx=5)
                self.step_image_button2.grid(row=i, column=3)
                if hasattr(self, "apply_image_preview2") and self.apply_image_preview2 is not None:
                    self.step2_label.configure(image=self.apply_image_preview2)
                    self.step2_label.grid(row=i, column=4, padx=20, pady=10)

            if i == 2:
                index3 = i
                self.step_text3.bind("<FocusOut>",lambda event, index = i: self.add_step(event,index3))
                self.step_image_button3.config(command=lambda row=i: self.add_image(self.apply_frame, index3))
                self.step_label.grid(row=i, column=0,pady=10,padx=5)
                self.step_text3.grid(row=i, column=1)
                self.step_image_button3.grid(row=i, column=3)
                if hasattr(self, "apply_image_preview3") and self.apply_image_preview3 is not None:
                    self.step3_label.configure(image=self.apply_image_preview3)
                    self.step3_label.grid(row=i, column=4, padx=20, pady=10)

            if i == 3:
                index4 = i
                self.step_text4.bind("<FocusOut>",lambda event, index = i: self.add_step(event,index4))
                self.step_image_button4.config(command=lambda row=i: self.add_image(self.apply_frame, index4))
                self.step_label.grid(row=i, column=0,pady=10,padx=5)
                self.step_text4.grid(row=i, column=1)
                self.step_image_button4.grid(row=i, column=3)
                if hasattr(self, "apply_image_preview4") and self.apply_image_preview4 is not None:
                    self.step4_label.configure(image=self.apply_image_preview4)
                    self.step4_label.grid(row=i, column=4, padx=20, pady=10)

            if i == 4:
                index5 = i
                self.step_text5.bind("<FocusOut>",lambda event, index = i: self.add_step(event,index5))
                self.step_image_button5.config(command=lambda row=i: self.add_image(self.apply_frame, index5))
                self.step_label.grid(row=i, column=0,pady=10,padx=5)
                self.step_text5.grid(row=i, column=1)
                self.step_image_button5.grid(row=i, column=3)
                if hasattr(self, "apply_image_preview5") and self.apply_image_preview5 is not None:
                    self.step5_label.configure(image=self.apply_image_preview5)
                    self.step5_label.grid(row=i, column=4, padx=20, pady=10)

            if i == 5:
                index6 = i
                self.step_text6.bind("<FocusOut>",lambda event, index = i: self.add_step(event,index6))
                self.step_image_button6.config(command=lambda row=i: self.add_image(self.apply_frame, index6))
                self.step_label.grid(row=i, column=0,pady=10,padx=5)
                self.step_text6.grid(row=i, column=1)
                self.step_image_button6.grid(row=i, column=3)
                if hasattr(self, "apply_image_preview6") and self.apply_image_preview6 is not None:
                    self.step6_label.configure(image=self.apply_image_preview6)
                    self.step6_label.grid(row=i, column=4, padx=20, pady=10)

            if i == 6:
                index7 = i
                self.step_text7.bind("<FocusOut>",lambda event, index = i: self.add_step(event,index7))
                self.step_image_button7.config(command=lambda row=i: self.add_image(self.apply_frame, index7))
                self.step_label.grid(row=i, column=0,pady=10,padx=5)
                self.step_text7.grid(row=i, column=1)
                self.step_image_button7.grid(row=i, column=3)
                if hasattr(self, "apply_image_preview7") and self.apply_image_preview7 is not None:
                    self.step7_label.configure(image=self.apply_image_preview7)
                    self.step7_label.grid(row=i, column=4, padx=20, pady=10)

            if i == 7:
                index8 = i
                self.step_text8.bind("<FocusOut>", lambda event, index=i: self.add_step(event, index8))
                self.step_image_button8.config(command=lambda row=i: self.add_image(self.apply_frame, index8))
                self.step_label.grid(row=i, column=0,pady=10,padx=5)
                self.step_text8.grid(row=i, column=1)
                self.step_image_button8.grid(row=i, column=3)
                if hasattr(self, "apply_image_preview8") and self.apply_image_preview8 is not None:
                    self.step8_label.configure(image=self.apply_image_preview8)
                    self.step8_label.grid(row=i, column=4, padx=20, pady=10)

            i += 1
        self.link_label.grid(row=i,column = 0,pady = 50)
        self.html_link.grid(row=i, column=1, pady=50,padx=20)


    def add_step(self,event, index):
        logger.info("Inside add_step of create widget")
        print("Index:"+str(index)+" Widget:"+event.widget.get())
        self.data_collector["Application_Step_Description"+str(index+1)] = event.widget.get()


    def add_image(self,apply_frame, index):
        logger.info("Inside add_image of create widget")
        if index == 0:

            filename_full = filedialog.askopenfilename(initialdir=fileroot,title='Select Image',parent=self)
            filename = os.path.basename(filename_full)
            self.filename_img_app1_full = filename_full
            self.data_collector['Application_Steps_Widget_1'] = filename

            try:
                apply_image = Image.open(self.filename_img_app1_full )
                apply_image.thumbnail((60, 60))
                self.apply_image_preview1 = ImageTk.PhotoImage(apply_image)
                self.step1_label.configure(image=self.apply_image_preview1)

                self.step1_label.grid(row=index, column=4, padx=20, pady=10)
            except:
                print("invalid image")

        elif index == 1:
            filename_full = filedialog.askopenfilename(initialdir=fileroot, title='Select Image', parent=self)
            filename = os.path.basename(filename_full)
            self.filename_img_app2_full = filename_full
            self.data_collector['Application_Steps_Widget_2'] = filename
            try:
                apply_image = Image.open(self.filename_img_app2_full)
                apply_image.thumbnail((60, 60))
                self.apply_image_preview2 = ImageTk.PhotoImage(apply_image)
                self.step2_label.configure(image=self.apply_image_preview2)
                self.step2_label.grid(row=index, column=4, padx=20, pady=10)
            except:
                print("invalid image")
        elif index == 2:
            filename_full = filedialog.askopenfilename(initialdir=fileroot,title='Select Image',parent=self)
            filename = os.path.basename(filename_full)
            self.filename_img_app3_full = filename_full
            self.data_collector['Application_Steps_Widget_3'] = filename

            try:
                apply_image = Image.open(self.filename_img_app3_full )
                apply_image.thumbnail((60, 60))
                self.apply_image_preview3 = ImageTk.PhotoImage(apply_image)
                self.step3_label.configure(image=self.apply_image_preview3)
                self.step3_label.grid(row=index, column=4, padx=20, pady=10)
            except:
                print("invalid image")
        elif index == 3:
            filename_full = filedialog.askopenfilename(initialdir=fileroot, title='Select Image', parent=self)
            filename = os.path.basename(filename_full)
            self.filename_img_app4_full = filename_full
            self.data_collector['Application_Steps_Widget_4'] = filename

            try:
                apply_image = Image.open(self.filename_img_app4_full)
                apply_image.thumbnail((60, 60))
                self.apply_image_preview4 = ImageTk.PhotoImage(apply_image)
                self.step4_label.configure(image=self.apply_image_preview4)
                self.step4_label.grid(row=index, column=4, padx=20, pady=10)
            except:
                print("invalid image")
        elif index == 4:
            filename_full = filedialog.askopenfilename(initialdir=fileroot,title='Select Image',parent=self)
            filename = os.path.basename(filename_full)
            self.filename_img_app5_full = filename_full
            self.data_collector['Application_Steps_Widget_5'] = filename


            try:
                apply_image = Image.open(self.filename_img_app5_full )
                apply_image.thumbnail((60, 60))
                self.apply_image_preview5 = ImageTk.PhotoImage(apply_image)
                self.step5_label.configure(image=self.apply_image_preview5)
                self.step5_label.grid(row=index, column=4, padx=20, pady=10)
            except:
                print("invalid image")
        elif index == 5:
            filename_full = filedialog.askopenfilename(initialdir=fileroot, title='Select Image', parent=self)
            filename = os.path.basename(filename_full)
            self.filename_img_app6_full = filename_full
            self.data_collector['Application_Steps_Widget_6'] = filename

            try:
                apply_image = Image.open(self.filename_img_app6_full)
                apply_image.thumbnail((60, 60))
                self.apply_image_preview6 = ImageTk.PhotoImage(apply_image)
                self.step6_label.configure(image=self.apply_image_preview6)
                self.step6_label.grid(row=index, column=4, padx=20, pady=10)
            except:
                print("invalid image")
        elif index == 6:
            filename_full = filedialog.askopenfilename(initialdir=fileroot, title='Select Image', parent=self)
            filename = os.path.basename(filename_full)
            self.filename_img_app7_full = filename_full
            self.data_collector['Application_Steps_Widget_7'] = filename

            try:
                apply_image = Image.open(self.filename_img_app7_full)
                apply_image.thumbnail((60, 60))
                self.apply_image_preview7 = ImageTk.PhotoImage(apply_image)
                self.step7_label.configure(image=self.apply_image_preview7)
                self.step7_label.grid(row=index, column=4, padx=20, pady=10)
            except:
                print("invalid image")
        elif index == 7:
            filename_full = filedialog.askopenfilename(initialdir=fileroot, title='Select Image', parent=self)
            filename = os.path.basename(filename_full)
            self.filename_img_app8_full = filename_full
            self.data_collector['Application_Steps_Widget_8'] = filename

            try:
                apply_image = Image.open(self.filename_img_app8_full)
                apply_image.thumbnail((60, 60))
                self.apply_image_preview8 = ImageTk.PhotoImage(apply_image)
                self.step8_label = ttk.Label(self.apply_activity_steps_frame, image=self.apply_image_preview8,
                                             )
                self.step8_label.configure(image=self.apply_image_preview8)
                self.step8_label.grid(row=index, column=4, padx=20, pady=10)
            except:
                print("invalid image")




    def add_create_frame(self):
        logger.info("Inside add_create_frame of create widget")

        self.create_question_page_Label = ttk.Label(self.create_frame, text='Here we add our questions for assessment.These are then displayed in the player and a PDF file for the same is generated.'
                                                                  , wraplength=600,
                                          style='Firebrick.Label')
        self.create_question_Label = ttk.Label(self.create_frame, text='Assessment Questions',wraplength= 300,style='Create.TLabelframe.Label')
        #create_test_label = ttk.Label(create_frame, text='Provide the Answer Key in this format(11, 23, 31,44, 52 - Would mean 1st Q - 11 option is correct, 2ndquestion 3rd option is correct and so on....)',wraplength=400,style='Create.TLabelframe.Label')

        #question_label = ttk.Label(create_frame, text='Total Number of questions?',style='Create.TLabelframe.Label')


        #create_test_label.grid(row=0, column=0)
        #create_test_entry.grid(row=0, column=1)
        self.create_question_page_Label.grid(row=0,column=0,columnspan=3,padx=5)
        self.create_question_Label.grid(row=1,column=0)
        self.create_question_text.grid(row=1,column=1,padx=5)
        #question_label.grid(row=2, column=0)
        #question_text.grid(row=2, column=1)





    def next_page(self):
        logger.info("Inside next_page of create widget")

        self.index += 1
        if self.index == 1:
            self.data_collector['Lesson_Title'] = self.title_text.get()
            self.data_collector["Application_Mode"] = ''
            self.data_collector["Title_Running_Notes"] = self.title_running_notes.get('1.0', tk.END)
            self.data_collector["Title_Running_Notes_Language"] = self.language_notes.get()
            self.data_collector['Title_Video'] = self.title_image_video_url.get()
            self.title_frame.pack_forget()
            self.factual_frame.pack(side='top')
            self.header_var.set(
                "Acquire New Knowledge - Introduce new terms, topics an definitions , add a visual cue for each")

        if self.index == 2:
            self.data_collector["Factual_Term1"] = self.factual_term_text.get()
            self.data_collector["Factual_Term1_Description"] = self.factual_term_desc_text.get('1.0', 'end')

            if self.factual_term_text1 is not None:
                self.data_collector['Factual_Term2'] = self.factual_term_text1.get()
            if self.factual_term_desc_text1 != None:
                self.data_collector['Factual_Term2_Description'] = self.factual_term_desc_text1.get('1.0', 'end')

            if self.factual_term_text2 != None:
                self.data_collector["Factual_Term3"] = self.factual_term_text2.get()
            if self.factual_term_desc_text2 != None:
                self.data_collector["Factual_Term3_Description"] = self.factual_term_desc_text2.get('1.0', 'end')

            self.factual_frame.pack_forget()
            self.apply_frame.pack(side='top')
            self.apply_activity_frame.grid(row=2, column=0, columnspan=2)
            self.header_var.set(
                "Application - Add a set of steps with an associated image. Use animation in the player later.e.g. Experiments or Stories and Activities")

            self.apply_activity_steps_frame.grid(row=3, column=0, columnspan=2)
        if self.index == 3:
            if self.data_collector['Application_Mode'] =='Video':
                self.data_collector['Application_Video_Link_Notes'] = self.video_link_running_notes.get('1.0', 'end')
            self.data_collector["Apply_External_Link"] = self.htmlvar.get()
            self.apply_frame.pack_forget()
            self.create_frame.pack()
            self.next_button.config(text='Submit')
            self.header_var.set("Assessment - Type your short questions to check for understanding")
        if self.index == 4:
            self.data_collector["Answer_Key"] = ""
            self.data_collector["Video_Audio_Assessment_Flag"] = 0
            self.data_collector["Questions"] = self.create_question_text.get('1.0','end')
            self.data_collector["Number_Questions"] = self.question_text.get()
            '''var_video_audio.get()'''
            self.save_data()

            #magic_wizard.destroy()
        print(self.data_collector)


    def save_data(self):

        logger.info("Inside save_data of create widget")


        self.lesson_file_manager = LessonFileManager(fileroot)
        self.lesson_file_manager.add_image_file(self.filename_img_title_full)

        if (self.filename_vid_title_full != ""):
            self.lesson_file_manager.add_video_file(self.filename_vid_title_full)


        self.lesson_file_manager.add_image_file(self.filename_img_fact1_full)
        self.lesson_file_manager.add_image_file(self.filename_img_fact2_full)
        self.lesson_file_manager.add_image_file(self.filename_img_fact3_full)


        if (self.filename_img_app1_full != ""):
            self.lesson_file_manager.add_image_file(self.filename_img_app1_full)
        if (self.filename_img_app2_full != ""):
            self.lesson_file_manager.add_image_file(self.filename_img_app2_full)
        if (self.filename_img_app3_full != ""):
            self.lesson_file_manager.add_image_file(self.filename_img_app3_full)
        if (self.filename_img_app4_full != ""):
            self.lesson_file_manager.add_image_file(self.filename_img_app4_full)
        if (self.filename_img_app5_full != ""):
            self.lesson_file_manager.add_image_file(self.filename_img_app5_full)
        if (self.filename_img_app6_full != ""):
            self.lesson_file_manager.add_image_file(self.filename_img_app6_full)
        if (self.filename_img_app7_full != ""):
            self.lesson_file_manager.add_image_file(self.filename_img_app7_full)
        if (self.filename_img_app8_full != ""):
            self.lesson_file_manager.add_image_file(self.filename_img_app8_full)


        try:
            connection = sqlite3.connect(db)
            cur = connection.cursor()
            sql = ('Insert into Magic_Science_Lessons (Lesson_Type, Lesson_Template, Lesson_Title,Title_Image,Title_Video,Title_Running_Notes,Title_Notes_Language,Factual_Term1,Factual_Term1_Description,Factual_Term2,Factual_Term2_Description,Factual_Term3,Factual_Term3_Description'
                   ', Application_Mode,Application_Steps_Number,Application_Step_Description_1,Application_Step_Description_2,Application_Step_Description_3,Application_Step_Description_4,Application_Step_Description_5, Application_Step_Description_6, Application_Step_Description_7, Application_Step_Description_8, Application_Steps_Widget_1'
                   ', Application_Steps_Widget_2, Application_Steps_Widget_3, Application_Steps_Widget_4, Application_Steps_Widget_5, Application_Steps_Widget_6, Application_Steps_Widget_7,Application_Steps_Widget_8,Answer_Key,Video_Audio_Assessment_Flag, Date, Factual_Image1, Factual_Image2, Factual_Image3'
                   ', Application_Video_Link , Application_Video_Running_Notes,IP_Questions,NumberOfQuestions,Apply_External_Link) values( :Lesson_Type, :Lesson_Template, :Lesson_Title, :Title_Image, :Title_Video, :Title_Running_Notes, :Title_Running_Notes_Language, :Factual_Term1'
                   ', :Factual_Term1_Description, :Factual_Term2, :Factual_Term2_Description, :Factual_Term3, :Factual_Term3_Description '
                   ', :Application_Mode, :Application_Steps_Number, :Application_Step_Description1'
                   ', :Application_Step_Description2, :Application_Step_Description3, :Application_Step_Description4, :Application_Step_Description5'
                   ', :Application_Step_Description6, :Application_Step_Description7, :Application_Step_Description8, :Application_Steps_Widget_1'
                   ', :Application_Steps_Widget_2, :Application_Steps_Widget_3, :Application_Steps_Widget_4, :Application_Steps_Widget_5, :Application_Steps_Widget_6'
                   ', :Application_Steps_Widget_7, :Application_Steps_Widget_8, :Answer_Key, :Video_Audio_Assessment_Flag, :Date,:Factual_Image1, :Factual_Image2, :Factual_Image3'
                   ', :Application_Video_Link, :Application_Video_Running_Notes, :Questions, :Number_Questions, :Apply_External_Link)')

            cur.execute(sql, self.data_collector)
            connection.commit()
        except (sqlite3.OperationalError):
             messagebox.showerror("Error Connecting to DB","Saving the Information met with an error")
             logger.exception("There was an error while saving the record")
        else:
             print("Database content created")

             messagebox.showinfo("Content Created","Content Created.\nLet us play it in the lesson player from the dashboard.\n\nThe assessment and the notes material is also ready."
                                                   "\n\nThis window shall close now",parent=self)
             logger.info("Created new lesson")
             self.destroy()



    def previous_page(self):
        logger.info("Inside previous_page of create widget")
        self.next_button.config(text='Next')
        if self.index == 1:
            self.index = 0
            self.factual_frame.pack_forget()
            self.title_frame.pack(side='top')
            self.header_var.set(
                "Activate Prior Knowledge - Introduce, Ask Questions, Play a related Video and Show a related visual of the topic")
        if self.index == 2:
            self.index = 1
            self.apply_frame.pack_forget()
            self.factual_frame.pack(side='top')
            self.header_var.set(
                "Acquire New Knowledge - Introduce new terms, topics an definitions , add a visual cue for each")
        if self.index == 3:
            self.index = 2
            self.create_frame.pack_forget()
            self.apply_frame.pack(side='top')
            self.header_var.set(
                "Application - Add a set of steps with an associated image. Use animation in the player later.e.g. Experiments or Stories and Activities")




#magic_wizard.mainloop()
