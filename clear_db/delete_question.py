import schedule    
import time 
import sqlite3


def delet():
    db = sqlite3.connect('main.db')
    c = db.cursor()

    c.execute('SELECT rowid, status_question FROM db_question')
    sql_delet = c.fetchall()

    for rowid, status_question in sql_delet:
        if status_question == 'old':
            c.execute('DELETE FROM db_question WHERE rowid = ?', (rowid,))
    db.commit()
    db.close()

schedule.every(1).weeks.do(delet) 

while True:
    schedule.run_pending()
    time.sleep(1)