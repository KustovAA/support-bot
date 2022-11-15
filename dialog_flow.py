from google.cloud import dialogflow


def get_answer_from_dialog_flow(session_id, project_id, text, language_code='ru-RU'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input},
    )

    return response.query_result.fulfillment_text, response.query_result.intent.is_fallback
