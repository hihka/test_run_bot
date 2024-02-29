from asyncio import sleep
from user_agent import generate_user_agent
from aiogram import Bot
from bs4 import BeautifulSoup
from config import TOKEN

import aiohttp
import sqlite3


bot = Bot(TOKEN, parse_mode='HTML')

url_question = 'https://ask.oksei.ru/questions' 



async def submitting_question(question):
    data = {'question': str(question)}
    headers = {'User-Agent': generate_user_agent()}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://ask.oksei.ru/add_question.php', headers=headers, data=data, ssl=False) as response:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')
                text = soup.get_text()
                return str(text) + '. Вам придет уведомление когда Директор ответит на вопорос'
    except Exception as e:
        await bot.send_message(chat_id='1701063338', text=f'Возникла ошибка с отправко вопроса на сайт\n\n<code>{str(e)}</code>')
        return 'error'


# async def submitting_question(question):
    # data = {'question': str(question)}
    # headers = {'User-Agent': generate_user_agent()}
    
    # async with aiohttp.ClientSession() as session:
    #     async with session.post('https://ask.oksei.ru/add_question.php', headers=headers, data=data, ssl=False) as response:
    #         html_text = await response.text()
    #         soup = BeautifulSoup(html_text, 'html.parser')
    #         text = soup.get_text()


async def fetch_html(url):
    headers = {"User-Agent": generate_user_agent()}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=False) as response:
            return await response.text()


async def write_and_send_to_db():
    await sleep(10800)
    
    stop_while= 0

    while stop_while != 1:
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
                        cursore.execute("UPDATE db_question SET answer = ? WHERE question = ?", (answers[questions.index(i)], questions[questions.index(i)])) 
                        await bot.send_message(chat_id=rows[db_index][2], text=f'Директор ответил на ваш вопрос.\n\n<b>Вопрос: </b>{rows[db_index][1]}\n<b>Ответ: </b>{answers[questions.index(i)]}')
        db.commit()
        db.close()
        stop_while +=1 


async def get_answer():
    html = await fetch_html('https://ask.oksei.ru/questions')
    soup = BeautifulSoup(html, 'html.parser')
    otvet = soup.find_all('div', class_='text-answer')
    ress = [otv.text.strip() for otv in otvet]
    return ress

async def get_question():
    html = await fetch_html('https://ask.oksei.ru/questions')
    soup = BeautifulSoup(html, 'html.parser')
    otvet = soup.find_all('div', class_='text-question')
    ress = [otv.text.strip() for otv in otvet]
    return ress
