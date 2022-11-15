import logging
import random

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow import get_answer_from_dialog_flow


def answer(session_id, project_id, event, vk_api):
    dialog_flow_response = get_answer_from_dialog_flow(session_id, project_id, event.text)

    if dialog_flow_response:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialog_flow_response,
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
    session_id = env.str('VK_DIALOG_FLOW_SESSION_ID')
    project_id = env.str('DIALOG_FLOW_PROJECT_ID')

    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(session_id, project_id, event, vk_api)
