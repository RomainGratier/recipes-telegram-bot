#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
# Import libraries
import argparse
import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)

from src.recommendation_engine.inference import predict_cuisine, get_similar_recipes
from src.recognition_engine.inference import classify_image

# Create the parser
my_parser = argparse.ArgumentParser(description='Give your personal token')

# Add the arguments
my_parser.add_argument('token', metavar='token', type=str, help='The token given by Fatherbot')


# Enable logging
logging.basicConfig(
    #filename= 'telgramBot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, GET_TEXT, GET_IMAGE = range(3)
# Callback data
CALLBACK1, CALLBACK2 = range(3,5)

reply_keyboard = [
    #['Add ingredient by photo', 'Add ingredient by text'],
    ['Show ingredients', 'Get recipes'],
    ['Remove item', 'Done'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info(f"{user.first_name}: Start")

    context.user_data['chat_id'] = update.message.chat_id

    update.message.reply_text(
        "Hi! I am you recipe bot. What ingredients do you currently have?"
        "You can send an image or add ingredients by typing it in one or two words",
        reply_markup=markup,
    )
    return CHOOSING

def received_image_information(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('infer_image.png')
    logger.info("Photo of %s: %s", user.first_name, 'infer_image.jpg')
    update.message.reply_text(
        'Thanks the photo is being processed'
    )

    user_data = context.user_data
    
    # Infer image prediction
    ingredient = classify_image('infer_image.png')
    
    keyboard = [
        [
            InlineKeyboardButton(ingredient[0], callback_data=ingredient[0]),
            InlineKeyboardButton(ingredient[1], callback_data=ingredient[1]),
            InlineKeyboardButton(ingredient[2], callback_data=ingredient[2])],
        [
            InlineKeyboardButton(ingredient[3], callback_data=ingredient[3]),
            InlineKeyboardButton(ingredient[4], callback_data=ingredient[4]),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Chose the ingredients you have on your image!", reply_markup=reply_markup)

    return CALLBACK1

def button1(update: Update, context: CallbackContext) -> int:
    logger.info(f": button1")

    query = update.callback_query
    query.answer()

    user_data = context.user_data    
    if 'ingredients_list' not in user_data:
        user_data['ingredients_list'] = [query.data]
    else:
        user_data['ingredients_list'].append(query.data)

    query.edit_message_text(text=f"Ok you selected: {query.data}")

    return CHOOSING

def recipes_query(update: Update, context: CallbackContext) -> int:
    """ Get recipes """
    user = update.message.from_user
    logger.info(f"{user.first_name}: recipes_query")

    user_data = context.user_data

    input_text = ' '.join(user_data['ingredients_list'])

    # Predict cuisine
    cuisine = predict_cuisine(input_text)

    keyboard = [
        [
            InlineKeyboardButton(cuisine[0], callback_data=cuisine[0]),
            InlineKeyboardButton(cuisine[1], callback_data=cuisine[1]),
            InlineKeyboardButton(cuisine[2], callback_data=cuisine[2])],
        [
            InlineKeyboardButton(cuisine[3], callback_data=cuisine[3]),
            InlineKeyboardButton(cuisine[4], callback_data=cuisine[4]),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Chose the type of cuisine you want!", reply_markup=reply_markup)

    return CALLBACK2

def button2(update: Update, context: CallbackContext) -> int:
    #user = update.message.from_user
    logger.info(f"button2")

    query = update.callback_query
    query.answer()

    # Get recipes
    recipes = get_similar_recipes(context.user_data['ingredients_list'], query.data)

    sep = '\n\n'
    for index, row in recipes.iterrows():

        title = 'Title: ' + row['title'] 
        ingredients=''
        list_ing = row['ingredients'].replace('ADVERTISEMENT', '').strip('][').split(', ')
        for ingredient in list_ing:
            ingredients+= ingredient.replace("'", "") + '\n'
        ingredients = 'Ingredients: ' + '\n' + ingredients
        instructions = 'Instruction: '+ '\n' + row['instructions']

        txt = title + sep + ingredients + sep + instructions

        context.bot.send_message(chat_id=context.user_data['chat_id'], text=txt)

    return CHOOSING

def show_basket(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info(f"{user.first_name}: show_basket")

    user_data = context.user_data
    update.message.reply_text(
        "Neat! Just so you know, this is what you already gived me:"
        f"{user_data['ingredients_list']}",
        reply_markup=markup,
    )
    return CHOOSING

def received_text_information(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info(f"{user.first_name}: received_text_information")

    user_data = context.user_data
    text = update.message.text
    
    if 'ingredients_list' not in user_data:
        user_data['ingredients_list'] = [text]
    else:
        user_data['ingredients_list'].append(text)

    update.message.reply_text(
        "Neat! Just so you know, this is what you already gived me:"
        f"{user_data['ingredients_list']}",
        reply_markup=markup,
    )
    return CHOOSING

def remove_item(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info(f"{user.first_name}: remove_item")

    user_data = context.user_data
    if 'ingredients_list' in user_data:
        del user_data['ingredients_list'][-1]

    return CHOOSING

def done(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info(f"{user.first_name}: done")

    user_data = context.user_data
    if 'ingredients_list' in user_data:
        del user_data['ingredients_list']

    update.message.reply_text(
        f"Bye bye until next time!"
    )

    user_data.clear()
    return ConversationHandler.END    

def main(bot_token) -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(Filters.photo & ~(Filters.command | Filters.regex('^(Done|Get recipes|Show ingredients|Remove item)$')), received_image_information),
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^(Done|Get recipes|Show ingredients|Remove item)$')), received_text_information),
                MessageHandler(Filters.regex('^Get recipes$'), recipes_query),
                MessageHandler(Filters.regex('^Show ingredients$'), show_basket),
                MessageHandler(Filters.regex('^Remove item$'), remove_item),
            ],
            CALLBACK1: [
                CallbackQueryHandler(button1)],
            CALLBACK2: [
                CallbackQueryHandler(button2)],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
        per_message=False,
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    # Execute the parse_args() method
    args = my_parser.parse_args()
    main(args.token)