# This is a sample Python script.


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
