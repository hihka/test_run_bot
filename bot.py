from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.statesQuestion import StepsQuestion

from config import TOKEN

import asyncio 
import sqlite3
import app
import keyboards


bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f"Здравствуй {message.from_user.first_name}.", reply_markup=keyboards.main_menu)


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Возник вопрос или предложение на пиши @feedback666_bot.')


@dp.message(F.text == 'Написать вопрос')
async def write_questions(message: Message, state: FSMContext):
    await message.answer('Напишите свой вопрос.', reply_markup=keyboards.back)
    await state.set_state(StepsQuestion.GET_QUESTION)


@dp.message(F.text == 'Назад')
async def back(message: Message):
    await message.answer('Вы вернулись в главное меню.', reply_markup=keyboards.main_menu)


@dp.message(F.text == 'Мои вопросы')
async def my_questions(message: Message):
    db = sqlite3.connect('main.db')
    cursore = db.cursor()

    id = message.chat.id
    cursore.execute("SELECT EXISTS(SELECT * FROM db_question WHERE id = ?);", (id,))
    exists = cursore.fetchone()[0]

    if exists == 1:
        cursore.execute('SELECT question, answer FROM db_question WHERE id = ?;', (id,))
        answer = cursore.fetchall()

        for i in answer:
            question_none = 'Ответа ещё нету.' if i[1] == 'None' else i[1]
            await message.answer(f'<b>Вопрос:</b> {i[0]}\n\n<b>Ответ: </b>{question_none}', reply_markup=keyboards.main_menu)
            await asyncio.sleep(0.5)
        db.close()
    else:
        await message.answer('Вы ещё не задали вопросов!', reply_markup=keyboards.main_menu)


@dp.message(F.text == 'Лента вопросов')
async def question_feed(message: Message):
    question = await app.get_question()
    answer = await app.get_answer()

    for questions, answers in zip(question, answer):
        await message.answer(f'<b>Вопрос:</b>\n{questions}\n\n<b>Ответ:</b>\n{answers}', reply_markup=keyboards.main_menu)
        await asyncio.sleep(0.5)


@dp.message(StepsQuestion.GET_QUESTION)
async def get_vp(message: Message, state: FSMContext):
    if message.text != None:
        context_data = await state.update_data(vp = message.text)
        vpp = context_data.get('vp')

        output_submitting_question = await app.submitting_question(vpp)
        if output_submitting_question == 'error':
            await message.answer('Произошла ошибка над ней уже работают. Отправте ворпос позже.', reply_markup=keyboards.back)
        else:
            db = sqlite3.connect('main.db')
            c = db.cursor()
            c.execute(f"INSERT INTO db_question VALUES ('{message.chat.id}', '{vpp}', 'None', 'new')")

            db.commit()
            db.close()
            
            await message.answer(await app.submitting_question(vpp), reply_markup=keyboards.back)

            await app.write_and_send_to_db()
            await state.clear()
    else:
        await message.reply("Напиши текст!", reply_markup=keyboards.back)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())