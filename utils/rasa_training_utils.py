from pathlib import Path

import pyaml
import yaml

BASE_DIR = Path(__file__).parent.parent
DATA_FOLDER = BASE_DIR / 'data'

FILE_PATHS = {
    'config': BASE_DIR / 'config.yml',
    'domain': BASE_DIR / 'domain.yml',
    'nlu': BASE_DIR / DATA_FOLDER / 'nlu.yml',
    'rules': BASE_DIR / DATA_FOLDER / 'rules.yml',
    'stories': BASE_DIR / DATA_FOLDER / 'stories.yml'
}
NLU_FILE = BASE_DIR / DATA_FOLDER / 'nlu.yml'
RULES_FILE = BASE_DIR / DATA_FOLDER / 'rules.yml'
STORIES_FILE = BASE_DIR / DATA_FOLDER / 'stories.yml'
DOMAIN_FILE = BASE_DIR / 'domain.yml'
CONFIG_FILE = BASE_DIR / 'config.yml'
DEFAULT_ENCODING = 'utf-8'
DEFAULT_BOOLEAN_REPRESENTER = u'tag:yaml.org,2002:bool'
DEFAULT_NULL_REPRESENTER = u'tag:yaml.org,2002:null'


pyaml.add_representer(bool, lambda dumper, data: dumper.represent_scalar(DEFAULT_BOOLEAN_REPRESENTER, str(data).lower()))
pyaml.add_representer(type(None), lambda dumper, data: dumper.represent_scalar(DEFAULT_NULL_REPRESENTER, 'null'))


class RasaTrainingUtils:
    def add_story(self, data):
        """
        data request
        {
            "nlu": [
                {
                    "intent": "",
                    "examples": ""
                }
            ],
            "responses": {
                "utter_<name_of_intent>": [
                    {
                        "text": ""
                    }
                ]
            },
            "stories": [
                {
                    "story": "",
                    "steps": [
                        {
                            "intent": "",
                        }
                        {
                            "action": ""
                        }
                    ]
                }
            ]
        }
        """

        self.__add_intents(data['data']['nlu'])
        self.__add_responses(data['data']['responses'])

        with open(FILE_PATHS['stories'], 'r', encoding=DEFAULT_ENCODING) as stories_yml:
            file = yaml.safe_load(stories_yml)

            for stories in data['data']['stories']:
                file['stories'].append(stories)
        
        if file:
            with open(FILE_PATHS['stories'], 'w', encoding=DEFAULT_ENCODING) as stories_yml:
                pyaml.dump(file, stories_yml, sort_dicts=pyaml.PYAMLSort.none, width=500)
    
    def get_story(self):
        ...
    
    def __add_intents(self, intents):
        """
        intent request
        [
            {
                "intent": "",
                "examples": ""
            }
        ]
        """

        with open(FILE_PATHS['nlu'], 'r', encoding=DEFAULT_ENCODING) as nlu:
            data = yaml.safe_load(nlu)

            for intent in intents:
                data['nlu'].append(intent)
        
        if data:
            with open(FILE_PATHS['nlu'], 'w', encoding=DEFAULT_ENCODING) as nlu:
                pyaml.dump(data, nlu, sort_dicts=pyaml.PYAMLSort.none)
        
        with open(FILE_PATHS['domain'], 'r', encoding=DEFAULT_ENCODING) as domain:
            data = yaml.safe_load(domain)

            for intent in intents:
                data['intents'].append(intent['intent'])
        
        if data:
            with open(FILE_PATHS['domain'], 'w', encoding=DEFAULT_ENCODING) as domain:
                pyaml.dump(data, domain, sort_dicts=pyaml.PYAMLSort.none, width=500)
    
    def get_intent(self):
        ...
    
    def __add_responses(self, responses):
        """
        response request
        [
            {
                "utter_<name_of_intent>": [
                    {
                        "text": ""
                    }
                ]
            }
        ]
        """
        with open(FILE_PATHS['domain'], 'r', encoding=DEFAULT_ENCODING) as domain:
            data = yaml.safe_load(domain)

            for response_name, values in responses.items():
                data['responses'][response_name] = values
            
        if data:
            with open(FILE_PATHS['domain'], 'w', encoding=DEFAULT_ENCODING) as domain:
                pyaml.dump(data, domain, sort_dicts=pyaml.PYAMLSort.none, width=500)
    
    def get_response(self):
        ...
    
    def get_train_data(self):
        def extract_data(file_path, keys):
            with open(file_path, 'r', encoding=DEFAULT_ENCODING) as yml_file:
                data = yaml.safe_load(yml_file)
            
            return {key: data[key] for key in keys}

        KEYS = {
            'config': ('pipeline', 'policies'),
            'domain': ('intents', 'entities', 'slots', 'actions', 'forms', 'responses', 'session_config'),
            'nlu': ('nlu',),
            'rules': ('rules',),
            'stories': ('stories',)
        }
        train_data = dict()
        
        for key, file_path in FILE_PATHS.items():
            train_data.update(extract_data(file_path, KEYS[key]))

        train_data = pyaml.dump(train_data, sort_dicts=pyaml.PYAMLSort.none, width=500)

        return train_data
