from asyncio import sleep
from user_agent import generate_user_agent
from aiogram import Bot
from bs4 import BeautifulSoup
from config import TOKEN

import aiohttp
import sqlite3


bot = Bot(TOKEN, parse_mode='HTML')

url_question = 'https://ask.okeit.edu/questions' 



async def submitting_question(question):
    data = {'question': str(question)}
    headers = {'User-Agent': generate_user_agent()}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://ask.okeit.edu/add_question.php', headers=headers, data=data, ssl=False) as response:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')
                text = soup.get_text()

    except Exception as e:
        await bot.send_message(chat_id='1701063338', text=f'Возникла ошибка с отправко вопроса на сайт\n\n<code>{str(e)}</code>')
        return 'error'


async def get_answer():
    html = await fetch_html('https://ask.okeit.edu/questions')
    soup = BeautifulSoup(html, 'html.parser')
    otvet = soup.find_all('div', class_='text-answer')
    ress = [otv.text.strip() for otv in otvet]
    return ress

async def get_question():
    html = await fetch_html('https://ask.okeit.edu/questions')
    soup = BeautifulSoup(html, 'html.parser')
    otvet = soup.find_all('div', class_='text-question')
    ress = [otv.text.strip() for otv in otvet]
    return ress
