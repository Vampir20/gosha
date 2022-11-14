from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from filters import IsPrivate
from main import dp
from states import registration


@dp.message_handler(IsPrivate(), Command('register'))
async def bot_register(message: types.Message):
    name = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f'{message.from_user.first_name}')],
            [KeyboardButton(text='Отменить регестрацию')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(f'привет\n'
                         f'для регистрации введи свое имя')

    await registration.name.set()


@dp.message_handler(IsPrivate(), state=registration.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    phone = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='отменить регестрацию  ')],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f'<b>{message.text}<b> Теперь пришли мне свой номер телефона чтобы мы могли связаться с тобой',
                         reply_markup=phone)
    await  registration.phone.set()


@dp.message_handler(IsPrivate(), state=registration.phone)
async def get_phone(message: types.Message, state: FSMContext):
    answer = message.text
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='отменить регистрацию')],
        ],
        resize_keyboard=True
    )
    try:
        if answer.replace('+', '').isnumeric():
            await state.update_data(phone=answer)
            await message.answer(f'теперь пришли мне свой возраст (цклым числом) ', reply_markup=markup)
            await registration.age.set()

        else:
            await message.answer('Введите корректный номер телефона', reply_markup=markup)

    except Exception:
        await message.answer('Введите корректный номер телефона')


@dp.message_handler(IsPrivate(), state=registration.age)
async def get_age(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.isnumeric():
        if int(answer) < 150:
            await state.update_data(age=answer)
            data = await state.get_data()
            name = data.get('name')
            phone = data.get('phone')
            age = data.get('age')
            await message.answer(f'Регистрация успешно завершена \n'
                                 f'Имя {name}\n'
                                 f'возраст {age}\n'
                                 f'номер телефона{phone}\n')


        else:
            await message.answer(f'введите корректный возраст')

    else:
        await message.answer(f'введите корректный возраст')
