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
        res = gateway_service.get_aluno_document_url(user_uuid, 'cronograma')

        file = res.json()

        dispatcher.utter_message(response='utter_solicitar_informacao_cronograma', attachment={
            'type': 'file',
            'payload': {
                'src': file['url'],
                'title': file['title'],
                'content-type': file['content-type']
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
        user_uuid = tracker.sender_id.split('_')[1]
        tipo_documento = tracker.get_slot('tipo_documento')
        tipo_documento_for_query = str(tipo_documento).replace(' ', '_')

        gateway_service = GatewayService()
        res = gateway_service.get_aluno_document_url(user_uuid, tipo_documento_for_query)
        json = None

        match res.status_code:
            case 500 | 400 | 401 | 403:
                dispatcher.utter_message('Infelizmente não consegui gerar o seu documento :(. Tente novamente')
            case 200:
                json = res.json()
            case _:
                dispatcher.utter_message('Infelizmente houve um erro, tente novamente. :(')

        attatchment = {
            'type': 'file',
            'payload': {
                'src': json['url'],
                'title': json['title'],
                'content-type': json['content-type']
            }
        }

        dispatcher.utter_message(text=f'Segue o seu {tipo_documento}:', attachment=attatchment)
        
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
        body = {
            'descricao': tracker.get_slot('pendencia_aluno'),
            'custom_user': tracker.sender_id.split('_')[1]
        }

        gateway_service = GatewayService()
        res = gateway_service.criar_pendencia(body)

        match res.status_code:
            case 500 | 400 | 401 | 403:
                dispatcher.utter_message('Infelizmente não consegui gerar a sua pendência. :( Tente novamente')
            case 201:
                dispatcher.utter_message(text='Pendência criada com sucesso!')
                dispatcher.utter_message(text='Você pode ver as suas pendências na seção de pendências')
                dispatcher.utter_message(text='Com elas, o coordenador da sua instituição pode visualizar e lhe auxiliar melhor!')
            case _:
                dispatcher.utter_message('Infelizmente houve um erro, tente novamente. :(')

        return [SlotSet('pendencia_aluno', None)]
