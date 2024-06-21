import requests
import json
import time
import cv2
import numpy as np
import base64
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='log.log', encoding='utf-8',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(
            self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt,  model, width, height, negative_prompt='', images=1):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "negativePromptUnclip": negative_prompt,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(
            self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=20, delay=10):
        while attempts > 0:
            response = requests.get(
                self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


def get_generated_image(prompt, negative_prompt, width=1024, height=1024):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/',
                        '2FF286FA8F9A4E2027023510F6D31E38', '0F9B0DF9044B67F54EAAEB6CE8ABDAC9')
    model_id = api.get_model()
    uuid = api.generate(prompt=prompt, negative_prompt=negative_prompt, width=width,
                        height=height, model=model_id)
    images = api.check_generation(uuid)
    decoded = base64.b64decode(images[0])
    nparr = np.frombuffer(decoded, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    logger.info('File sent ot an interface')
    return img
