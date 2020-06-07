
from misc import dp
from db.functions import lists, db_func

import logging
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as md
from aiogram.types import ParseMode


@dp.message_handler(state="*", commands='start')
async def start_cmd_handler(message: types.Message):
    print("This is the Message ID : ", message.chat.id)
    user_list = db_func.search("user_id")
    user = types.User.get_current()
    if user['id'] in user_list:
        keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
        text_and_data = (
            ('My Profile', 'profile'),
            ('My Promo Code', 'promo'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text,
                    data in text_and_data)

        keyboard_markup.row(*row_btns)
        reply_text = "Hi! " + user['first_name']
        await message.answer(reply_text, reply_markup=keyboard_markup)
    else:
        keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
        text_and_data = (
            ('Register', 'register'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text,
                    data in text_and_data)

        keyboard_markup.row(*row_btns)
        reply_text = "Hi! " + user['first_name'] + " you are not registered with us."
        await message.answer(reply_text, reply_markup=keyboard_markup)


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel', text="Cancel")
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text="profile")
async def profile_msg_handler(query: types.CallbackQuery):
    print("Hello i am in the my profile loop")
    user = types.User.get_current()
    user_list = db_func.search("user_id")
    ind = user_list.index(user['id']) - 1 
    await query.answer('You answered With My Profile')
    await dp.bot.send_message(
                            query.message.chat.id,
                            md.text(
                                    md.text("Your Name ",
                                            md.bold(lists.name_list[ind])),
                                    md.text("Your Phone Number ",
                                            md.bold(lists.phone_list[ind])),
                                    md.text("Your Age ",
                                            md.bold(lists.age_list[ind])),
                                    md.text("Your City ",
                                            md.bold(lists.city_list[ind])),
                                    md.text("Your Region ",
                                            md.bold(lists.region_list[ind])),
                                    md.text("Your PromoCode is ",
                                            md.bold(lists.promo_list[ind])),
                                    sep='\n'),
                            parse_mode=ParseMode.MARKDOWN)

    reply_yes = "Done"
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                selective=True,
                                                one_time_keyboard=True)
    keyboard_markup.add('Menu')
    await query.message.answer(reply_yes, reply_markup=keyboard_markup)


@dp.callback_query_handler(text="promo")
async def promo_msg_handler(query: types.CallbackQuery):
    print("Hello i am in the my Promo Code")
    # to get the index of the user if present in the database
    user = types.User.get_current()
    user_list = db_func.search("user_id")
    ind = user_list.index(user['id']) - 1
    await query.answer('You answered With My Promo Code')
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                selective=True,
                                                one_time_keyboard=True)
    keyboard_markup.add('Menu')
    reply_text = f"Your Promo Code is `{str(lists.promo_list[ind])}`"
    await query.message.answer(reply_text,
                               parse_mode=ParseMode.MARKDOWN,
                               reply_markup=keyboard_markup)


@dp.message_handler(text="Menu")
async def menu_handler(message: types.Message):
    await start_cmd_handler(message)
