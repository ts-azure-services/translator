import os
import requests
import uuid
from dotenv import load_dotenv
import random

class textTranslate:
    """
    Class to highlight the functionality of text translate
    """
    def __init__(self, sample_filename=None):
        if sample_filename == None:
            sample_filename = './data-files/text_translation/msft-values.txt'
        self.sample_filename = sample_filename
        self.sample_text = self.load_text(self.sample_filename)
        self.language_list_file = './data-files/text_translation/lang_list.txt'
        self.env_variables = './variables.env'
        self.auth_dict = self.load_variables()
        self.language_dictionary, self.sample_list = self.load_languages()
        self.cog_rg = self.auth_dict['cog_rg']
        self.cog_name = self.auth_dict['cog_name']
        self.cog_key = self.auth_dict['cog_key']
        self.cog_location = self.auth_dict['cog_location']
        self.source_url = self.auth_dict['source_url']
        self.target_url = self.auth_dict['target_url']
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.cog_key,
            'Ocp-Apim-Subscription-Region':self.cog_location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

    def load_variables(self):
        """Load up env variables of the API key & location"""
        load_dotenv(self.env_variables)
        auth_dict = {
                "cog_rg":os.environ['RESOURCE_GROUP'],
                "cog_name":os.environ['TRANSLATOR_NAME'],
                "cog_key":os.environ['TRANSLATOR_KEY'],
                "cog_location":os.environ['TRANSLATOR_LOCATION'],
                "source_url": os.environ['SOURCE_URL'],
                "target_url": os.environ['TARGET_URL']
                }
        return auth_dict

    def load_text(self, filepath):
        """Load sample text file to translate"""
        with open(filepath) as f:
            data = f.read().replace('\n', ' ')
        return data

    def load_single_line_text(self, filename):
        statements = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                statements.append(line)
        return statements

    def load_languages(self):
        """Create a random list of languages to test"""
        ld = {}
        with open(self.language_list_file) as f:
            for line in f:
                (val, key) = line.split(',')
                key = key.replace('\n','')
                ld[key] = val
        key_list = list(ld.keys())
        sample_list = random.choices(key_list,k=5)
        return ld, sample_list

    def translate_text(self, text=None, to_lang='fr', from_lang='en'):
        """Create a function that makes a REST request to the Text Translation service"""

        # To check char length, JSON array <=100, 10k chars max
        print(f"Number of text characters: {len(text)}")

        # Create the URL for the Text Translator service REST request
        path = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
        params = '&from={}&to={}'.format(from_lang, to_lang)
        constructed_url = path + params

        # Add the text to be translated to the body
        body = [{'text': text}]

        # Get the translation
        request = requests.post(constructed_url, headers=self.headers, json=body)
        response = request.json()
        return response[0]["translations"][0]["text"]

    def one_language(self, to_lang=None):
        """Test the API for one language"""
        translation = self.translate_text(self.sample_text, to_lang=to_lang, from_lang='en')
        print(f"********************")
        print(f"Text to translate (in English):\n {self.sample_text}")
        print(f"\033[92m Translated text (in {self.language_dictionary[to_lang]}):\n {translation} \033[00m")
        print(f"********************")
        print("")

    def multiple_in_single_call(self, to_lang=None):
        pass

    def transliterate(self, text = '猿も木から落ちる', source_lang='ja', fromScript='Jpan'):
        """Canned function to show transliteration."""

        # To check char length, JSON array <=100, 10k chars max
        if source_lang=='ja':
            print(f"Actual Japanese text: {text}.")
            print(f"Actual English translation: Monkeys also fall from trees.")
            print(f"Number of text characters: {len(text)}")

        # Create the URL for the Text Translator service REST request
        path = 'https://api.cognitive.microsofttranslator.com/transliterate?api-version=3.0'
        params = f'&language={source_lang}&fromScript={fromScript}&toScript=Latn'
        constructed_url = path + params

        # Add the text to be translated to the body
        body = [{'text': text}]

        # Get the translation
        request = requests.post(constructed_url, headers=self.headers, json=body)
        response = request.json()
        return response

    def five_random(self):
        """Test the API for five random languages"""
        for i,v in enumerate(self.sample_list):
            translation = self.translate_text(self.sample_text, to_lang=self.sample_list[i], from_lang='en')
            print(f"********************")
            print(f"Text to translate (in English):\n {self.sample_text}")
            print(f"\033[92m Translated text (in {self.language_dictionary[self.sample_list[i]]}):\n {translation} \033[00m")
            print(f"********************")
            print("")

class documentTranslate(textTranslate):
    """
    Class to highlight document translation
    """

    def translate_docs(self, source_lang='en', target_lang='es'):
        """Create a function that makes a REST request for a Document Translate"""

        self.headers = {
            'Ocp-Apim-Subscription-Key': self.cog_key,
            'Content-type': 'application/json',
        }
        # Create the URL for the Text Translator service REST request
        path = f'https://{self.cog_name}.cognitiveservices.azure.com/translator/text/batch/v1.0/batches/'

        # Add the text to be translated to the body
        body = {
                "inputs":[
                    {
                        "source":{
                            "sourceUrl":self.source_url,
                            "storageSource": "AzureBlob",
                            "language": source_lang
                            },
                        "targets":[
                            {
                                "targetUrl":self.target_url,
                                "storageSource":"AzureBlob",
                                "category":"general",
                                "language": target_lang
                                }
                            ]
                        }
                    ]
                }

        # Trigger the document translation request, validate response
        response = requests.post(path, headers=self.headers, json=body)
        status, reason, resp_headers = response.status_code, response.reason, response.headers
        print(f"response status code: {status}")
        print(f"response status: {reason}")
        print(f"response headers: {resp_headers}")

        # Get request id
        json_response = dict(resp_headers)
        operation_location = json_response['Operation-Location'].split('/')
        request_id = operation_location[-1:][0]
        print(f"Request ID: {request_id}")

        ## Get status of request once
        ## Could iterate if requests take longer (depends on demo samples)
        #print(f"Checking on response status of request...")
        #time.sleep(5)
        #self.check_request(request_id)


    #def check_request(self, request_id):
    #    """Function to check status of response sent"""
    #    host = f'{self.cog_name}.cognitiveservices.azure.com'
    #    parameters = '//translator/text/batch/v1.0/batches/{request_id}'
    #    key =  self.cog_key
    #    conn = http.client.HTTPSConnection(host)
    #    payload = ''
    #    headers = {'Ocp-Apim-Subscription-Key': key}
    #    conn.request("GET", parameters , payload, headers)
    #    res = conn.getresponse()
    #    data = res.read()
    #    print(data)
    #    print(res.status)
    #    print(data.decode("utf-8"))

class customTranslate(textTranslate):
    def custom_translate(self, text=None, category_id=None, to_lang='fr', from_lang='en'):
        """Create a function that makes a REST request to the Custom Translation model"""

        # To check char length, JSON array <=100, 10k chars max
        print(f"Number of text characters: {len(text)}")

        # Create the URL for the Text Translator service REST request
        path = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
        params = '&from={}&to={}'.format(from_lang, to_lang)
        category = f'&category={category_id}'
        constructed_url = path + params + category

        # Add the text to be translated to the body
        body = [{'text': text}]

        # Get the translation
        request = requests.post(constructed_url, headers=self.headers, json=body)
        response = request.json()
        return response
        #return response[0]["translations"][0]["text"]

    def one_language(self, category_id=None, to_lang=None, from_lang='en'):
        """Test the API for one language"""
        # Feed in the custom translation text based upon the demo artifacts
        translation = self.custom_translate(
                text=self.sample_text, 
                category_id=None, 
                to_lang=to_lang, from_lang=from_lang)
        print(f"********************")
        print(f"Text to translate (in English):\n {self.sample_text}")
        print(f"\033[92m Translated text (in {self.language_dictionary[to_lang]}):\n {translation} \033[00m")
        print(f"********************")
        print("")

