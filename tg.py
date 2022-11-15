import logging
from functools import partial

from environs import Env
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from dialog_flow import get_answer_from_dialog_flow


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def answer(session_id, project_id, update: Update, context: CallbackContext):
    dialog_flow_response = get_answer_from_dialog_flow(session_id, project_id, update.message.text)

    if dialog_flow_response:
        update.message.reply_text(dialog_flow_response)
    else:
        update.message.reply_text('Не совсем понимаю, о чем ты.')


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    env = Env()
    env.read_env()
    token = env.str('TG_BOT_TOKEN')
    session_id = env.str('TG_DIALOG_FLOW_SESSION_ID')
    project_id = env.str('DIALOG_FLOW_PROJECT_ID')

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    dialog_handler = MessageHandler(Filters.text & ~Filters.command, partial(
        answer,
        session_id,
        project_id
    ))
    dispatcher.add_handler(dialog_handler)

    updater.start_polling()
    updater.idle()
