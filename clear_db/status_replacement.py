import schedule    
import time 
import sqlite3

def status():
    db = sqlite3.connect('main.db')
    c = db.cursor()
    old = 'old'
    c.execute('SELECT answer, status_question FROM db_question')
    sql_status = c.fetchall()

    for sql_none in sql_status:
        if sql_none[0] == 'None':
            c.execute('UPDATE db_question SET status_question = ? WHERE answer = ?', (old, 'None'))
    db.commit()
    db.close()

schedule.every(6).day.do(status) 

while True:
    schedule.run_pending()
    time.sleep(1)