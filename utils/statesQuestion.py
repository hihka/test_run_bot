from aiogram.fsm.state import StatesGroup, State

class StepsQuestion(StatesGroup):
    GET_QUESTION = State()