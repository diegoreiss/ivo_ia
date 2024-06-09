# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Coroutine, Dict, List, Text

import requests
from rasa_sdk import Action, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

from services.gateway_service import GatewayService


ALLOWED_TIPO_DOCUMENTO = (
    'atestado de frequencia', 'atestado de matricula', 'historico escolar',
)


class CronogramaAction(Action):
    def name(self) -> Text:
        return 'action_enviar_cronograma'
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Coroutine[Any, Any, List[Dict[Text, Any]]]:
        user_uuid = tracker.sender_id.split('_')[1]

        gateway_service = GatewayService()
        res = gateway_service.get_turma_by_user(user_uuid)

        turma = res.json()
        print(turma)

        dispatcher.utter_message(response='utter_solicitar_informacao_cronograma', attachment={
            'type': 'file',
            'payload': {
                'title': turma['turma']['calendario'].split('/')[-1],
                'src': turma['turma']['calendario']
            }
        })


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


class ValidatePendenciaForm(FormValidationAction):
    def name(self) -> Text:
        return 'validate_pendencia_form'
    
    def validate_pendencia_aluno(self, slot_value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        """Validate slot pendencia_aluno"""

        pendencia_text = slot_value.strip()

        if len(pendencia_text) <= 0:
            return {'pendencia_aluno': None}

        return {'pendencia_aluno': pendencia_text}


class SubmitFormPendencia(Action):
    def name(self) -> Text:
        return 'action_submit_form_pendencia'
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Coroutine[Any, Any, List[Dict[Text, Any]]]:
        uuid = tracker.sender_id.split('_')[1]
        body = {
            'descricao': tracker.get_slot('pendencia_aluno')
        }

        print(f'user_uuid {uuid}')
        print(f'pendencia: {body}')
        
        dispatcher.utter_message(text='enviando form pendencia')

        return [SlotSet('pendencia_aluno', None)]
