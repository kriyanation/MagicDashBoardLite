import logging
import os, sys
import sqlite3
import traceback
from tkinter import messagebox
from shutil import copyfile
logger = logging.getLogger("MagicLogger")
class LessonFileManager():
    def __init__(self,file_root):
        print(file_root)
        try:


            connection = sqlite3.connect(file_root+os.path.sep+"MagicRoom.db")
            cur = connection.cursor()
            sql = "SELECT Lesson_ID FROM Magic_Science_Lessons ORDER BY Lesson_ID Desc Limit 1"
            cur.execute(sql)
            rows = cur.fetchone()
            self.new_id = rows[0] + 1
        except sqlite3.OperationalError:
            messagebox.showerror("DB Error", "Cannot Connect to Database")
            logger.exception("cannot connect to database")


        try:
            if not os.path.exists(file_root+os.path.sep+"Lessons"):
                os.makedirs('Lessons')
            self.lesson_dir = file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(self.new_id)
            if not os.path.exists(self.lesson_dir):
                os.makedirs(file_root + os.path.sep + "Lessons"+os.path.sep+"Lesson"+str(self.new_id))

            self.image_path = file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
                self.new_id) + os.path.sep + "images"
            self.video_path = file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
                self.new_id) + os.path.sep + "videos"
            self.save_path = file_root + os.path.sep + "Lessons" + os.path.sep + "Lesson" + str(
                self.new_id) + os.path.sep + "saved_boards"

            if not os.path.exists(self.image_path):
                os.makedirs(self.image_path)
            if not os.path.exists(self.video_path):
                os.makedirs(self.video_path)
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
        except (OSError, IOError):
            print("Directory could not be created")
            logger.exception("directory could not be created")



    def add_image_file(self,filepath):
        try:
            copyfile(filepath,self.image_path+os.path.sep+os.path.basename(filepath))
        except (IOError, OSError):
            print("Image File could not be copied")
            logger.exception("Image file could not be copied")

    def add_video_file(self,filepath):
        try:
            copyfile(filepath, self.video_path + os.path.sep + os.path.basename(filepath))
        except (IOError, OSError):
            print("Video File could not be copied")
            logger.exception("Video file could not be copied")
