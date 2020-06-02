
import sqlite3
import configparser, os
from tkinter import StringVar,messagebox
import traceback
import logging

TEST_ROW = 16
logger = logging.getLogger("MagicLogger")

file_root = os.path.abspath(os.getcwd())
db = file_root+os.path.sep+".."+os.path.sep+"MagicRoom.db"
lesson_root = file_root+os.path.sep+".."+os.path.sep+"Lessons"




def class_info():
    try:
        list_names = []
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select * from Magic_Class_Info"
        cur.execute(sql)
        rows = cur.fetchall()
        for element in rows:
            list_names.append(element)

        connection.commit()
        connection.close()
        return list_names
    except:
        logger.info("Exception in retrieving class information")
        logger.info(traceback.print_exc())



def get_Lessons_count():
    try:
        print (db)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select count(*) from Magic_Science_Lessons"
        cur.execute(sql)
        count = cur.fetchone()
        print(count)
        connection.commit()
        connection.close()
        return count
    except:
        logger.info("Exception in retrieving lessons information")
        logger.info(traceback.print_exc())


def get_participants_count():
    try:
        print (db)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select count(*) from Magic_Class_Info"
        cur.execute(sql)
        count = cur.fetchone()
        print(count)
        connection.commit()
        connection.close()
        return count
    except:
        logger.info("Exception in retrieving lessons information")
        logger.info(traceback.print_exc())


def get_skill_steps_count():
    try:
        print (db)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select sum(Application_Steps_Number) from Magic_Science_Lessons"
        cur.execute(sql)
        sum = cur.fetchone()
        print(sum)
        connection.commit()
        connection.close()
        return sum
    except:
        logger.info("Exception in retrieving lessons information")
        logger.info(traceback.print_exc())

def get_badge_1_count():
    try:
        print (db)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select Name from Magic_Class_Info where Badge = 'a'"
        cur.execute(sql)
        names = cur.fetchall()
        print(sum)
        connection.commit()
        connection.close()
        return names
    except:
        logger.info("Exception in retrieving lessons information")
        logger.info(traceback.print_exc())

def get_title_images():
    try:
        print (db)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select Lesson_ID, Title_Image from Magic_Science_Lessons"
        cur.execute(sql)
        image_list = cur.fetchall()
        connection.commit()
        connection.close()
        return image_list
    except:
        logger.info("Exception in retrieving image list information")
        logger.exception("Exception in Image List Retrieval")


def get_participants():
    try:
        print(db)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select Name from Magic_Class_Info"
        cur.execute(sql)
        participant_list = cur.fetchall()
        connection.commit()
        connection.close()
        return participant_list
    except:
        logger.info("Exception in retrieving participant list information")
        logger.exception("Exception in participant List Retrieval")

def get_flash_images():

    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Lesson_ID,Factual_Image1 from Magic_Science_Lessons"
    cur.execute(sql)
    images = cur.fetchall()
    connection.commit()
    connection.close()
    return images