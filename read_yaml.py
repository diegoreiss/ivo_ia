import yaml
import pyaml
from pathlib import Path

from yaml.constructor import SafeConstructor

from utils.rasa_training_utils import RasaTrainingUtils

BASE_DIR = Path(__file__).parent
nlu_file = BASE_DIR / 'data/nlu_test.yml'
# nlu_file = BASE_DIR / 'domain_test.yml'

# def add_bool(self, node):
#     return self.construct_scalar(node)
# SafeConstructor.add_constructor(u'tag:yaml.org,2002:bool', add_bool)

# new_intent = {
#     'intent': 'ferias',
#     'examples': '\n'.join([
#         '- minhas ferias',
#         '- quero saber das minhas ferias',
#     ]) + '\n'
# }

# responses = {
#     'responses': {
#         "utter_saudacao": [
#             {
#                 "text": "Oi, eu sou o IVO, um assistente virtual\nEm que posso ajudar?\n"
#             },
#             {
#                 "text": "Olá!!! mem chamo IVO, sou um assistente virtual feito para te ajudar com algumas informações!"
#             }
#         ],
#         "utter_agradecimento": [
#             {
#                 "text": "De nada, é sempre um prazer ajudar!"
#             },
#             {
#                 "text": "Qual o próximo assunto que te interessa?"
#             }
#         ],
#         "utter_despedida": [
#             {
#                 "text": "Foi um prazer te ajudar! Sempre que tiver alguma dúvida, volte aqui! Até logo!"
#             },
#             {
#                 "text": "Foi um prazer te ajudar! Sempre que precisar, volte aqui! Até a próxima!"
#             },
#             {
#                 "text": "Foi um prazer te ajudar! Quando surgir alguma dúvida, volte aqui! Até mais!"
#             }
#         ]
# }}




body = {
    'data': {
        'nlu': [
            {
                'intent': 'ferias',
                'examples': '- minhas férias\n- quando é as minhas férias\n'
            }
        ],
        'responses': {
            'utter_ferias': [
                {
                    'text': 'suas férias será em dezembro'
                },
            ],
        },
        'stories': [
            {
                'story': 'dialogo_sobre_ferias',
                'steps': [
                    {
                        'intent': 'ferias',
                    },
                    {
                        'action': 'utter_ferias'
                    }
                ]
            }
        ]
    }
}

# rtu = RasaTrainingUtils()
# rtu.get_train_data()

from utils.pagination_utils import PaginationUtils


pagu = PaginationUtils()

current = 'diego'
new = 'coisas'

with open(nlu_file, 'r', encoding='utf-8') as nlu:
    data = yaml.safe_load(nlu)


# data['intents'][data['intents'].index(current)] = new

# print(data['intents'])

# a, = filter(lambda intent: intent['intent'] == s, data['nlu'])
# a['intent'] = 'coisas'
# print(data['nlu'])

# py = pyaml.dump(data, sort_dicts=pyaml.PYAMLSort.none)
# print(py)

# data_nlu = data['nlu']
# print(data_nlu, '\n\n')

# f = [intent for intent in data_nlu if intent['intent'] == 'asdfsdf']
# print(f)

# paginated = pagu.paginate(data_nlu, 10, 2)
# print(paginated)

# print(pyaml.dump(paginated, sort_dicts=pyaml.PYAMLSort.none))
# print(data['nlu'])

# with open(nlu_file, 'r', encoding='utf-8') as domain:
#     data = yaml.safe_load(domain)

# print(pyaml.dump(data, sort_keys=False, width=500))
