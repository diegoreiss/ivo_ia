from typing import Text, Any, Callable, Awaitable
import inspect
from sanic import Sanic, Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse

from rasa.core.channels.channel import (
    InputChannel,
    UserMessage,
)

from utils.rasa_training_utils import RasaTrainingUtils


class TrainingModel(InputChannel):
    def name(self) -> Text:
        """Name of your custom channel."""
        return 'training_model'
    
    def blueprint(self, on_new_message: Callable[[UserMessage], Awaitable[Any]]) -> Blueprint:
        custom_webhook = Blueprint(f'custom_webhook_{type(self).__name__}', inspect.getmodule(self).__name__)

        @custom_webhook.route('/', methods=['GET'])
        async def health(request: Request) -> HTTPResponse:
            return response.json({'status': 'ok', 'code': 200}, status=200)
        
        @custom_webhook.route('/story', methods=['POST'])
        async def create_story(request: Request) -> HTTPResponse:
            data = request.json

            rasa_training_utils = RasaTrainingUtils()
            rasa_training_utils.add_story(data)

            return response.json({}, status=418)

        @custom_webhook.route('/intent', methods=['GET'])
        async def get_all_intents(request: Request) -> HTTPResponse:
            args = request.get_args()
            page = int(args.get('page', 1))
            rasa_training_utils = RasaTrainingUtils()

            intents = rasa_training_utils.get_all_intents(page)
            
            return response.json({'data': intents}, status=200)
        
        @custom_webhook.route('/intent', methods=['POST'])
        async def create_intent(request: Request) -> HTTPResponse:
            intent = request.json

            if intent['examples'] != '':
                intent['examples'] = intent['examples'] + '\n'

            if not intent:
                return response.json({}, status=400)

            rasa_training_utils = RasaTrainingUtils()
            result = rasa_training_utils.add_intent(intent)

            if result:
                return response.json({}, status=201)
            
            return response.json({}, status=400)
        
        @custom_webhook.route('/intent/<intent>', methods=['GET'])
        async def get_intent_by_name(request: Request, intent: Text) -> HTTPResponse:
            rasa_training_utils = RasaTrainingUtils()
            intent = rasa_training_utils.get_intent(intent)

            return response.json(intent, status=200 if intent else 404)

        @custom_webhook.route('/intent/<intent>/change/examples', methods=['PATCH'])
        async def edit_intent_examples(request: Request, intent: Text) -> HTTPResponse:
            rasa_training_utils = RasaTrainingUtils()
            intent = rasa_training_utils.get_intent(intent)
            examples = request.json.get('examples')

            if not intent:
                return response.json({}, status=404)
            
            result = rasa_training_utils.edit_intent_examples(intent, examples)

            return response.json({}, status=200 if result else 400)
        
        @custom_webhook.route('/response', methods=['GET'])
        async def get_all_responses(request: Request) -> HTTPResponse:
            args = request.get_args()
            page = int(args.get('page', 1))
            rasa_training_utils = RasaTrainingUtils()

            responses = rasa_training_utils.get_all_responses(page)

            return response.json({'data': responses}, status=200)
        
        @custom_webhook.route('/train', methods=['GET'])
        async def get_training_data(request: Request) -> HTTPResponse:
            rasa_training_utils = RasaTrainingUtils()
            training_data_yml = rasa_training_utils.get_train_data()

            return HTTPResponse(body=training_data_yml, status=200, headers={
                'Content-Type': 'application/yaml'
            })

        return custom_webhook
