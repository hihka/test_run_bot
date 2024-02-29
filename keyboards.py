from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,

)

main_menu= ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Написать вопрос')
        ],
        [
            KeyboardButton(text='Лента вопросов'),
            KeyboardButton(text='Мои вопросы')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True

)