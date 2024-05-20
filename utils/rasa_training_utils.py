import json
from pathlib import Path

import pyaml
import yaml

from utils.pagination_utils import PaginationUtils

BASE_DIR = Path(__file__).parent.parent
DATA_FOLDER = BASE_DIR / 'data'
IGNORE_FOLDER = BASE_DIR / 'ignore'

FILE_PATHS = {
    'config': BASE_DIR / 'config.yml',
    'domain': BASE_DIR / 'domain.yml',
    'domain_ignore': IGNORE_FOLDER / 'domain_ignore.yml',
    'nlu': BASE_DIR / DATA_FOLDER / 'nlu.yml',
    'nlu_ignore': IGNORE_FOLDER / 'nlu_ignore.yml',
    'rules': BASE_DIR / DATA_FOLDER / 'rules.yml',
    'stories': BASE_DIR / DATA_FOLDER / 'stories.yml',
    'stories_ignore': IGNORE_FOLDER / 'stories_ignore.yml',
}

NLU_FILE = BASE_DIR / DATA_FOLDER / 'nlu.yml'
RULES_FILE = BASE_DIR / DATA_FOLDER / 'rules.yml'
STORIES_FILE = BASE_DIR / DATA_FOLDER / 'stories.yml'
DOMAIN_FILE = BASE_DIR / 'domain.yml'
CONFIG_FILE = BASE_DIR / 'config.yml'
DEFAULT_ENCODING = 'utf-8'
DEFAULT_BOOLEAN_REPRESENTER = u'tag:yaml.org,2002:bool'
DEFAULT_NULL_REPRESENTER = u'tag:yaml.org,2002:null'
DEFAULT_PAGINATION_SIZE = 10
DEFAULT_PAGINATION_NUMBER = 1


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
    
    def add_intent(self, intent):
        result = False

        with open(FILE_PATHS['nlu'], 'r', encoding=DEFAULT_ENCODING) as nlu:
            data = yaml.safe_load(nlu)
        
        data['nlu'].append(intent)

        if data:
            with open(FILE_PATHS['nlu'], 'w', encoding=DEFAULT_ENCODING) as nlu:
                pyaml.dump(data, nlu, sort_dicts=pyaml.PYAMLSort.none, width=500)
            
            result = True
        
        with open(FILE_PATHS['domain'], 'r', encoding=DEFAULT_ENCODING) as domain:
            data = yaml.safe_load(domain)
        
        data['intents'].append(intent['intent'])

        if data:
            with open(FILE_PATHS['domain'], 'w', encoding=DEFAULT_ENCODING) as domain:
                pyaml.dump(data, domain, sort_dicts=pyaml.PYAMLSort.none, width=500)
            
            result = True
        
        return result
    
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
    
    def get_all_intents(self, page=DEFAULT_PAGINATION_NUMBER):
        with open(FILE_PATHS['nlu'], 'r', encoding=DEFAULT_ENCODING) as nlu:
            data = yaml.safe_load(nlu)
        
        pagination_utils = PaginationUtils()
        data = pagination_utils.paginate(data['nlu'], DEFAULT_PAGINATION_SIZE, page)

        data = {
            'total_pages': data['total_pages'],
            'nlu': {
                'intents': data['page_data']
            }
        }

        return data
    
    def get_all_available_intents_names(self):
        with open(FILE_PATHS['nlu_ignore'], 'r', encoding=DEFAULT_ENCODING) as nlu_ignore:
            data = yaml.safe_load(nlu_ignore)
        
        intents_for_ignore = tuple(map(lambda i: i['intent'], data['nlu']))

        with open(FILE_PATHS['nlu'], 'r', encoding=DEFAULT_ENCODING) as nlu:
            data = yaml.safe_load(nlu)

        intents = filter(lambda i: i not in intents_for_ignore, map(lambda i: i['intent'], data['nlu']))

        with open(FILE_PATHS['domain_ignore'], 'r', encoding=DEFAULT_ENCODING) as domain_ignore:
            data = yaml.safe_load(domain_ignore)
        
        responses_for_ignore = data['responses']

        with open(FILE_PATHS['domain'], 'r', encoding=DEFAULT_ENCODING) as domain:
            data = yaml.safe_load(domain)
        
        responses = tuple(response.split('utter_')[1] for response in filter(lambda r: r not in responses_for_ignore, data['responses']))

        available_intents = tuple(filter(lambda i: i not in responses, intents))

        return available_intents

    def get_all_intents_names(self):
        with open(FILE_PATHS['nlu'], 'r', encoding=DEFAULT_ENCODING) as nlu:
            data = yaml.safe_load(nlu)
        
        intents_names = tuple(map(lambda i: i['intent'], data['nlu']))

        return intents_names
    
    def get_intent(self, name):
        with open(FILE_PATHS['nlu'], 'r', encoding=DEFAULT_ENCODING) as nlu:
            data = yaml.safe_load(nlu)
        
        intent = next((intent for intent in data['nlu'] if intent['intent'] == name), None)

        return intent
    
    def edit_intent_examples(self, intent, examples):
        result = False

        with open(FILE_PATHS['nlu'], 'r', encoding=DEFAULT_ENCODING) as nlu:
            data = yaml.safe_load(nlu)
        
        data['nlu'][data['nlu'].index(intent)]['examples'] = examples

        with open(FILE_PATHS['nlu'], 'w', encoding=DEFAULT_ENCODING) as nlu:
            pyaml.dump(data, nlu, sort_dicts=pyaml.PYAMLSort.none, width=500)
        
        result = True

        return result
    
    def add_response(self, response):
        result = False

        with open(FILE_PATHS['domain'], 'r', encoding=DEFAULT_ENCODING) as domain:
            data = yaml.safe_load(domain)
        
        if data:
            data['responses'].update(response)

            with open(FILE_PATHS['domain'], 'w', encoding=DEFAULT_ENCODING) as domain:
                pyaml.dump(data, domain, sort_dicts=pyaml.PYAMLSort.none, width=500)
            
            return not result
        
        return result
    
    def edit_response_texts(self, response, texts):
        result = False

        with open(FILE_PATHS['domain'], 'r', encoding=DEFAULT_ENCODING) as domain:
            data = yaml.safe_load(domain)

        if data:
            if not data['responses'].get(response):
                return result

            data['responses'][response] = texts

            with open(FILE_PATHS['domain'], 'w', encoding=DEFAULT_ENCODING) as domain:
                pyaml.dump(data, domain, sort_dicts=pyaml.PYAMLSort.none, width=500)
            
            return not result
        
        return result

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
    
    def get_all_responses(self, page=DEFAULT_PAGINATION_NUMBER):
        pagination_utils = PaginationUtils()

        with open(FILE_PATHS['domain'], 'r', encoding=DEFAULT_ENCODING) as domain:
            data = yaml.safe_load(domain)
        
        data = pagination_utils.paginate_dict(data['responses'], DEFAULT_PAGINATION_SIZE, page)
        data = {
            'total_pages': data['total_pages'],
            'responses': data['page_data']
        }

        return data
    
    def get_all_responses_names(self):
        with open(FILE_PATHS['domain'], 'r', encoding=DEFAULT_ENCODING) as domain:
            data = yaml.safe_load(domain)
        
        return tuple(data['responses'].keys())
    
    def get_response(self):
        ...
    
    def get_all_stories(self):
        with open(FILE_PATHS['stories_ignore'], 'r', encoding=DEFAULT_ENCODING) as stories_ignore:
            data = yaml.safe_load(stories_ignore)
        
        stories_for_ignore = data['stories']
        
        with open(FILE_PATHS['stories'], 'r', encoding=DEFAULT_ENCODING) as stories:
            data = yaml.safe_load(stories)
        
        return tuple(filter(lambda s: s['story'] not in stories_for_ignore , data['stories']))
    
    def create_story(self, story):
        result = False

        with open(FILE_PATHS['stories'], 'r', encoding=DEFAULT_ENCODING) as stories:
            data = yaml.safe_load(stories)
        
        data['stories'].append(story)

        with open(FILE_PATHS['stories'], 'w', encoding=DEFAULT_ENCODING) as stories:
            pyaml.dump(data, stories, sort_dicts=pyaml.PYAMLSort.none, width=500)
        
        return not result
    
    def edit_story_steps(self, story, steps):
        result = False

        with open(FILE_PATHS['stories'], 'r', encoding=DEFAULT_ENCODING) as stories:
            data = yaml.safe_load(stories)
        
        story_filtered = next(filter(lambda s: s['story'] == story, data['stories']), None)

        if not story_filtered:
            return result
        
        story_filtered['steps'] = steps

        with open(FILE_PATHS['stories'], 'w', encoding=DEFAULT_ENCODING) as stories:
            pyaml.dump(data, stories, sort_dicts=pyaml.PYAMLSort.none, width=500)
        
        return not result
    
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
