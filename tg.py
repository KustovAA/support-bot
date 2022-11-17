import logging
from functools import partial

from environs import Env
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from dialog_flow import get_answer_from_dialog_flow


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def answer(project_id, update: Update, context: CallbackContext):
    dialog_flow_answer, is_fallback = get_answer_from_dialog_flow(update.effective_chat.id, project_id, update.message.text)

    update.message.reply_text(dialog_flow_answer)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    env = Env()
    env.read_env()
    token = env.str('TG_BOT_TOKEN')
    project_id = env.str('DIALOG_FLOW_PROJECT_ID')

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    dialog_handler = MessageHandler(Filters.text & ~Filters.command, partial(
        answer,
        project_id
    ))
    dispatcher.add_handler(dialog_handler)

    updater.start_polling()
    updater.idle()
