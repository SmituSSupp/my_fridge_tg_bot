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

import logging
from kitchen import Ingredient, Fridge
import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

FRIDGE_ACTION_SELECTION, FOOD_EXPORT_IMPORT = range(2)
COOKBOOK_ACTION_SELECTION, ADD_RECIPE, SHOW_ALL_RECIPES, SHOW_CAT_RECIPES, WHAT_CAN_I_DO = range(10, 16)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""

    update.message.reply_text("Hello there")

    return 1


def existing_fridge(update: Update, context: CallbackContext) -> int:
    """Starts the conversation about food export_import."""
    reply_keyboard = [['Add/take food', 'Close fridge']]

    update.message.reply_text(
        'Введите изменения в запасах еды',
        # reply_markup=ReplyKeyboardMarkup(
        #     reply_keyboard, one_time_keyboard=True, input_field_placeholder='Close fridge'
        # ),
    )

    return FOOD_EXPORT_IMPORT


def update_food(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    food_updatings = update.message.text
    food_updatings_lines = food_updatings.splitlines()

    food_update_pattern = '([+-]|добавить|убрать) (["a-zA-Zа-яА-Я0-9% ]+) ([0-9.]+) (кг|шт|л)'

    added = []
    removed = []

    for line in food_updatings_lines:
        food_match = re.search(food_update_pattern, line)

        if food_match:
            direcion, name, quantity, measure = food_match.groups()

            ingredient = Ingredient(name, float(quantity), measure)

            if direcion == "+" or "добавить":
                added.append(ingredient)
            elif direcion == "-" or "убрать":
                removed.append(ingredient)
            else:
                raise ValueError("unknown action")

    logger.info("food updating %s", update.message.text)

    fridge = Fridge()

    fridge.change_ingredients_on_shelfs(added, removed)

    update.message.reply_text(f"Обновления в составе холодильника!\n {fridge.show_shelfs()} \nВведите еще или "
                              f"закройте холодильник при помощи "
                              f"/close_fridge", reply_markup=ReplyKeyboardRemove())

    return FOOD_EXPORT_IMPORT


def close_fridge(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Закрываем холодос'
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    fridge_handler = ConversationHandler(
        entry_points=[CommandHandler('existing_fridge', existing_fridge)],
        states={
            FOOD_EXPORT_IMPORT: [MessageHandler(Filters.text & ~Filters.command, callback=update_food)],
        },
        fallbacks=[CommandHandler('close_fridge', close_fridge)],
    )

    start_handler = CommandHandler('start', start)

    dispatcher.add_handler(fridge_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
