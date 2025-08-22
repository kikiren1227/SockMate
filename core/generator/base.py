import requests
from typing import TypedDict
from abc import ABC, abstractmethod

class BaseParams(TypedDict):
    prompt: str
    width: int
    height: int

class ImageGenerator(ABC):

    @abstractmethod
    def generate(self, param: BaseParams):
        pass

class HFGenerator(ImageGenerator):

    def __init__(self, api_token: str, url: str):
        self._api_token = api_token
        self._url = url

    def generate(self, params: BaseParams):
        header = {
            "Authorization": f"Bearer {self._api_token}"
        }

        payload = {
            "inputs": params["prompt"],
            "parameters": {
                "width": f"{params['width']}", 
                "height": f"{params['height']}"
            }
        }

        try:
            response = requests.post(self._url, headers=header, json=payload)
            return response.content

        except requests.HTTPError:
            print("Http Error")
