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
        
        @custom_webhook.route('/train', methods=['GET'])
        async def get_training_data(request: Request) -> HTTPResponse:
            rasa_training_utils = RasaTrainingUtils()
            training_data_yml = rasa_training_utils.get_train_data()

            return HTTPResponse(body=training_data_yml, status=200, headers={
                'Content-Type': 'application/yaml'
            })

        return custom_webhook
