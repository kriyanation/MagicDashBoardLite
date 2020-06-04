
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

def get_title_names():
    try:
        print (db)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select Lesson_ID, Lesson_Title from Magic_Science_Lessons"
        cur.execute(sql)
        title_list = cur.fetchall()
        connection.commit()
        connection.close()
        return title_list
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

def get_flash_names():
    try:
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select Lesson_ID,Factual_Term1 from Magic_Science_Lessons"
        cur.execute(sql)
        terms = cur.fetchall()
        connection.commit()
        connection.close()
        return terms
    except:
        logger.info("Exception in retrieving participant list information")
        logger.exception("Exception in participant List Retrieval")
