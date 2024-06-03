import os

import requests
from dotenv import load_dotenv


load_dotenv(override=True)


GATEWAY_SERVICE_URL = os.environ['GATEWAY_SERVICE_URL']
GATEWAY_SERVICE_API_KEY = os.environ['GATEWAY_SERVICE_API_KEY']


class GatewayService:
    def get_turma_by_user(self, uuid):
        res = requests.get(f'{GATEWAY_SERVICE_URL}/user/{uuid}/turma/', headers={
            'Accept': 'application/json',
            'Authorization': f'Api-Key {GATEWAY_SERVICE_API_KEY}'
        })

        return res
