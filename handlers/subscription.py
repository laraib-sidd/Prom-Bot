from misc import dp
from db.functions import db_func, lists
from functions import func


from aiogram import types
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    phone = State()     # Will be represteted in storage as 'Form:surname'
    age = State()   # Will be represented in storage as 'Form:age'
    city = State()  # Will be represented in storage as 'Form:city'
    region = State()  # Will be represented in storage as 'Form:country'
    promo = State()     # Will be represented in storage as 'Form:promo'


@dp.callback_query_handler(text="register")
async def subscribe_msg_handler(query: types.CallbackQuery):
    print('You are in the Subscribe block')
    await query.message.answer("So,Let's start with you registration",
                               reply_markup=types.ReplyKeyboardRemove())

    """
    Conversation's entry point
    """
    # Set state
    await Form.name.set()
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                selective=True,
                                                one_time_keyboard=True)
    keyboard_markup.add('Cancel')
    await query.message.answer("Hi there! What's your name?",
                               reply_markup=keyboard_markup)


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process name
    """
    func.data['name'] = str(message.text)
    await Form.next()
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                selective=True,
                                                one_time_keyboard=True)
    keyboard_markup.add('Cancel')
    await message.answer("What is Phone Number?",
                         reply_markup=keyboard_markup)


# Check Phone Number. Phone number gotta be in digits digit
@dp.message_handler(lambda message: not message.text.isdigit(),
                    state=Form.phone)
async def process_number_invalid(message: types.Message):
    """
    If Phone number is invalid
    """
    return await message.answer("Phone Number gotta be a number.\n"
                                "Try Again(digits only)")


# Check length of Phone Number
@dp.message_handler(lambda message: len(message.text) < 10, state=Form.phone)
async def process_number_length(message: types.Message):
    """
    If Phone number is of invalid length
    """
    return await message.answer("Phone Number gotta be of 10 digits.\n"
                                "Try again (10 digits)")


# Check Country code
@dp.message_handler(lambda message: message.text[:2] != "05", state=Form.phone)
async def check_country_code(message: types.Message):
    """
    If Phone number is of invalid length
    """
    return await message.answer("The Number should start with 05"
                                "\nTry Agian")

@dp.message_handler(state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    """
    Process Phone Numeber name
    """
    func.data['phone'] = int(message.text)

    await Form.next()
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                selective=True,
                                                one_time_keyboard=True)
    keyboard_markup.add('Cancel')
    await message.answer("How old are you?",
                         reply_markup=keyboard_markup)


# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    """
    If age is invalid
    """
    return await message.answer("Age Should be a number.\n "
                                "How old are you? (digits only)")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data

    func.data['age'] = int(message.text)

    await Form.next()
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                selective=True,
                                                one_time_keyboard=True)
    keyboard_markup.add('Cancel')
    await message.answer("What city you reside in ?",
                         reply_markup=keyboard_markup)


@dp.message_handler(state=Form.city)
async def process_city(message: types.Message, state: FSMContext):
    # Update state and data

    func.data['city'] = str(message.text)
    await Form.next()
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                selective=True,
                                                one_time_keyboard=True)
    keyboard_markup.add('Cancel')
    await message.answer("What is your Region you reside in ?",
                         reply_markup=keyboard_markup)


@dp.message_handler(state=Form.region)
async def process_region(message: types.Message, state: FSMContext):
    # Update state and data
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)

    func.data['region'] = str(message.text)
    text_and_data = (
        ('Yes!', 'yes'),
        ('No!', 'no'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text,
                data in text_and_data)

    keyboard_markup.row(*row_btns)

    reply_text = "Do you have a Promo Code ?"
    await message.answer(reply_text, reply_markup=keyboard_markup)
    await Form.next()


@dp.message_handler(state=Form.promo)
async def promo_yes(message: types.Message, state: FSMContext):
    res = func.check_referal(message.text)
    print(res)

    if res:
        await message.answer("Your Promo Code is found")
        name = lists.name_list[lists.promo_list.index(message.text)]
        await message.answer(f"You have been referred by {name}")
        await Form.next()
    else:
        await message.answer("Your Promo Code is not found, Check it again?")
        await Form.next()
    func.data['user_id'] = int(message.chat.id)
    func.data['promo_code'] = func.get_promo_code()
    await message.answer("Your Profile is created",
                         reply_markup=types.ReplyKeyboardRemove())
    db_func.save_to_database(func.data)
    await dp.bot.send_message(
                        message.chat.id,
                        md.text(
                                md.text("Your Name ",
                                        md.bold(func.data['name'])),
                                md.text("Your Phone Number ",
                                        md.bold(func.data['phone'])),
                                md.text("Your Age ",
                                        md.bold(func.data['age'])),
                                md.text("Your City ",
                                        md.bold(func.data['city'])),
                                md.text("Your Region ",
                                        md.bold(func.data['region'])),
                                md.text("Your PromoCode is ",
                                        md.bold(func.data['promo_code'])),
                                sep='\n'),
                        parse_mode=ParseMode.MARKDOWN)

    await state.finish()

    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                selective=True,
                                                one_time_keyboard=True)
    keyboard_markup.add('Menu')
    await message.answer('Your data is saved in the database',
                         reply_markup=keyboard_markup)



@dp.callback_query_handler(text='no', state=Form.promo)  # if cb.data == 'no'
@dp.callback_query_handler(text='yes', state=Form.promo)  # if cb.data == 'yes'
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    await query.answer(f'You answered with {answer_data!r}')
    print("I am in the inline block")
    if answer_data == 'yes':
        await query.message.answer("Enter The promo code: ",
                                   reply_markup=types.ReplyKeyboardRemove())                     
        await promo_yes(query.message.text, state=Form.promo)
    elif answer_data == 'no':
        func.check_referal("not_found")
        func.data['user_id'] = int(query.message.chat.id)
        func.data['promo_code'] = func.get_promo_code()
        await query.message.answer("Your Profile is created",
                                   reply_markup=types.ReplyKeyboardRemove())
        db_func.save_to_database(func.data)
        await dp.bot.send_message(
                            query.message.chat.id,
                            md.text(
                                    md.text("Your Name ",
                                            md.bold(func.data['name'])),
                                    md.text("Your Phone Number ",
                                            md.bold(func.data['phone'])),
                                    md.text("Your Age ",
                                            md.bold(func.data['age'])),
                                    md.text("Your City ",
                                            md.bold(func.data['city'])),
                                    md.text("Your Region ",
                                            md.bold(func.data['region'])),
                                    md.text("Your PromoCode is ",
                                            md.bold(func.data['promo_code'])),
                                    sep='\n'),
                            parse_mode=ParseMode.MARKDOWN)

        await state.finish()

        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                    selective=True,
                                                    one_time_keyboard=True)
        keyboard_markup.add('Menu')
        await query.message.answer('Your data is saved in the database',
                                   reply_markup=keyboard_markup)
