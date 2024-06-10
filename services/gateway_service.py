import os

import requests
from dotenv import load_dotenv


load_dotenv(override=True)


GATEWAY_SERVICE_URL = os.environ['GATEWAY_SERVICE_URL']
GATEWAY_SERVICE_API_KEY = os.environ['GATEWAY_SERVICE_API_KEY']


class GatewayService:
    def get_aluno_document_url(self, uuid, file):
        res = requests.get(f'{GATEWAY_SERVICE_URL}/document/aluno/{uuid}/?file={file}', headers={
            'Accept': 'application/json',
            'Authorization': f'Api-Key {GATEWAY_SERVICE_API_KEY}'
        })

        return res
    
    def criar_pendencia(self, body):
        res = requests.post(f'{GATEWAY_SERVICE_URL}/pendencia/', headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Api-Key {GATEWAY_SERVICE_API_KEY}'
        }, json=body)

        return res
