import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters


def send_message_to_dialog_flow(session_id, project_id, text, language_code='ru-RU'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input},
    )

    return response.query_result.fulfillment_text


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def get_dialog(session_id, project_id):
    def dialog(update: Update, context: CallbackContext):
        dialog_flow_response = send_message_to_dialog_flow(session_id, project_id, update.message.text)

        if dialog_flow_response:
            update.message.reply_text(dialog_flow_response)
        else:
            update.message.reply_text('Не совсем понимаю, о чем ты.')

    return dialog


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    env = Env()
    env.read_env()
    token = env.str('TG_BOT_TOKEN')
    chat_id = env.str('TG_USER_CHAT_ID')
    session_id = env.str('SESSION_ID')
    project_id = env.str('PROJECT_ID')

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    dialog_handler = MessageHandler(Filters.text & ~Filters.command, get_dialog(session_id, project_id))
    dispatcher.add_handler(dialog_handler)

    updater.start_polling()
    updater.idle()
