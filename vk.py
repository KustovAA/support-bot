import logging
import random

from environs import Env
from google.cloud import dialogflow
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType


def send_message_to_dialog_flow(session_id, project_id, text, language_code = 'ru-RU'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input},
    )

    return response.query_result.fulfillment_text


def dialog(session_id, project_id, event, vk_api):
    dialog_flow_response = send_message_to_dialog_flow(session_id, project_id, event.text)

    if dialog_flow_response:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialog_flow_response,
            random_id=random.randint(1, 1000)
        )
    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message='Не совсем понимаю, о чем ты.',
            random_id=random.randint(1, 1000)
        )


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    env = Env()
    env.read_env()
    token = env.str('VK_ACCESS_TOKEN')
    session_id = env.str('SESSION_ID')
    project_id = env.str('PROJECT_ID')

    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            dialog(session_id, project_id, event, vk_api)
