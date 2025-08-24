from typing import Any, TypedDict
from abc import ABC, abstractmethod

class BaseParams(TypedDict):
    prompt: str
    guidance_scale: int | float | None
    width: int
    height: int
    negative_prompt: str | None
    seed: int | None

    @classmethod
    def create(cls, 
            prompt: str, 
            width: int = 512, 
            height: int = 512, 
            negative_prompt: str = None, 
            guidance_scale: int | float | None = None, 
            seed: int | None = None) -> 'BaseParams':
        return {
            "prompt": prompt,
            "guidance_scale": guidance_scale,
            "width": width,
            "height": height,
            "negative_prompt": negative_prompt,
            "seed": seed
        }

class ImageReferenceParams(BaseParams):
    reference_image: Any
    control_type: str

class PlatformParams(TypedDict):
    api_url: str
    api_token: str
    model: str | None
    
    @classmethod
    def create(cls, api_url: str, api_token: str, model: str | None): # model value will be None if we are using a router
        return { 
            'api_url': api_url,
            'api_token': api_token,
            'model': model
        }

class ImageGenerator(ABC):

    @abstractmethod
    def generate(self, param: BaseParams | ImageReferenceParams) -> Any:
        pass


