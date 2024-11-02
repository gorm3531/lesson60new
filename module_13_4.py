from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
api = '7705832901:AAFlAOrIVady3Xcx3X9VWeIqm2U7EFVIsKg'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.")


@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age= message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    formula = (10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']) - 161)
    await message.answer(f"Ваша норма каллорий: {formula}")
    await state.finish()

@dp.message_handler()
async def start(message: types.Message):
    await message.answer('Привет! Хочешь узнать свою норму калорий? Тогда напиши Calories')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

#10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161







#data = await state.get_data()