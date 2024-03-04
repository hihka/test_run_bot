import time 
import sqlite3
import asyncio

from aiogram import Bot
from config import TOKEN

bot = Bot(TOKEN, parse_mode='HTML')

async def main():
    while True:
        time.sleep(604800)    
        delet()


async def delet():
    db = sqlite3.connect('main.db')
    c = db.cursor()

    c.execute('SELECT rowid, answer, question, id FROM db_question')
    sql_delet = c.fetchall()

    for rowid, answer, question, id in sql_delet:
        if answer == 'None':
            await bot.send_message(chat_id=id, text=f"Директор забыл про ваш вопрос:\n\n{question}")
            c.execute('DELETE FROM db_question WHERE rowid = ?', (rowid,))
    db.commit()
    db.close()


asyncio.run(main())