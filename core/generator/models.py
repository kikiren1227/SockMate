from base import ImageGenerator, PlatformParams, BaseParams
import requests

class HFGenerator(ImageGenerator):

    def __init__(self, platform_params: PlatformParams):
        self._api_token = platform_params['api_token']
        self._url = platform_params['api_url']
        self.model = platform_params['model']

    def generate(self, params: BaseParams):
        header = {
            "Authorization": f"Bearer {self._api_token}"
        }

        payload = {
            "inputs": params["prompt"],
            "parameters": {
                "width": params['width'], 
                "height": params['height']
            }
        }

        try:
            response = requests.post(self._url, headers=header, json=payload)
            return response.content

        except requests.HTTPError:
            print("Http Error")

class FalGenerator(ImageGenerator):

    def __init__(self, platform_params: PlatformParams):
        self._api_token = platform_params["api_token"]
        self._api_url = platform_params["api_url"]
        self.model = platform_params["model"]

    def generate(self, params: BaseParams):
        header = {
            "Authorization": f"Key {self._api_token}",
            "Content-Type": "application/json"
        }

        payload = {
            'prompt': params['prompt'],
            'guidance_scale': params["guidance_scale"],
        }

        try:
            response = requests.post(self._api_url, headers=header, json=payload)
            return response.content
        except requests.HTTPError:
            print("Http Error")
        