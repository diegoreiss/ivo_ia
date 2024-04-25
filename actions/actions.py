# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Coroutine, Dict, List, Text
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from rasa_sdk.types import DomainDict


ALLOWED_TIPO_DOCUMENTO = (
    'atestado', 'matricula',
)

class ActionDarOi(Action):
    def name(self) -> Text:
        return 'action_dar_oi'
    
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Coroutine[Any, Any, List[Dict[Text, Any]]]:
        dispatcher.utter_message(response='utter_saudacao', nome='Diego')

        return []


class AskForTipoDocumenoAction(Action):
    def name(self) -> Text:
        return 'action_ask_tipo_documento'
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Coroutine[Any, Any, List[Dict[Text, Any]]]:
        dispatcher.utter_message(response='utter_ask_tipo_documento', buttons=[{'title': tipo, 'payload': tipo } for tipo in ALLOWED_TIPO_DOCUMENTO])

        return []


class SubmitFormTipoDocumento(Action):
    def name(self) -> Text:
        return 'action_submit_form_tipo_documento'
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Coroutine[Any, Any, List[Dict[Text, Any]]]:
        dispatcher.utter_message(text=f'form enviado {tracker.get_slot("tipo_documento")}')

        return []
