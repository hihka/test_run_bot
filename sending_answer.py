import asyncio
from user_agent import generate_user_agent
from aiogram import Bot
from bs4 import BeautifulSoup
from config import TOKEN

import aiohttp
import sqlite3


bot = Bot(TOKEN, parse_mode='HTML')

url_question = 'https://ask.okeit.edu/questions' 



async def fetch_html(url):
    headers = {"User-Agent": generate_user_agent()}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=False) as response:
            return await response.text()



async def main():
    while True:
        await write_and_send_to_db()
        await asyncio.sleep(3600)  

async def write_and_send_to_db():
    html = await fetch_html(url_question)

    soup = BeautifulSoup(html, 'html.parser')
    question = soup.find_all('div', class_='text-question')
    questions = [vppp.text.strip() for vppp in question]

    answer = soup.find_all('div', class_='text-answer')
    answers = [otv.text.strip() for otv in answer]

    db = sqlite3.connect('main.db')
    cursore = db.cursor()

    cursore.execute("SELECT rowid, question, id, answer FROM db_question;")
    rows = cursore.fetchall()

    for db_index in range(len(rows)):
        for i in questions:
            if i in rows[db_index][1]:
                if rows[db_index][3] == 'None':
                    await bot.send_message(chat_id=rows[db_index][2], text=f'Директор ответил на ваш вопрос.\n\n<b>Вопрос: </b>{rows[db_index][1]}\n\n<b>Ответ: </b>{answers[questions.index(i)]}')
                    
                    cursore.execute("DELETE FROM db_question WHERE question = ?",(rows[db_index][1], ))


    db.commit()
    db.close()

asyncio.run(main())

