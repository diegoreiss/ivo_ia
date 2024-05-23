# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Coroutine, Dict, List, Text
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet


ALLOWED_TIPO_DOCUMENTO = (
    'atestado de frequencia', 'atestado de matricula', 'historico escolar',
)

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
        tipo_documento = tracker.get_slot("tipo_documento")
        if tipo_documento == 'historico escolar':
            dispatcher.utter_message(response='utter_fornecer_historico_escolar')
        else:
            dispatcher.utter_message(text=f'form enviado {tipo_documento}')
        
        return [SlotSet('tipo_documento', None)]
    

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return 'action_default_fallback_name'

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="my_custom_fallback_template")

        return ['UserUtteranceReverted()']
