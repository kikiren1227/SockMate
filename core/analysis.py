import requests
from typing import TypedDict, Any
from abc import ABC, abstractmethod
from PIL import Image
import io
import json
import base64
import os

class AnalyzerParams(TypedDict):
    image: Any
    api_token: str
    api_url: str

class AnalysisResult(TypedDict):
    gender: str
    style: str
    vibe: str
    color_palette: str

class SockDesign(TypedDict):
    shape: str
    material: str
    pattern: str
    colors: str

class Analyzer(ABC):
    """Abstract base class for image analysis"""
    
    @abstractmethod
    def analyze(self, params: AnalyzerParams) -> AnalysisResult:
        """Analyze image and return user characteristics"""
        pass

class DoubaoAnalyzer(Analyzer):
    """Uses Doubao API for image analysis"""
    
    def __init__(self, api_token: str, api_url: str):
        self._api_token = api_token
        self._api_url = api_url
    
    def analyze(self, params: AnalyzerParams) -> AnalysisResult:
        # Convert image to base64
        img = Image.open(params["image"])
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Build request data
        data = {
            "model": "doubao-seed-1-6-250615",
            "messages": [
                {
                    "content": [
                        {
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_str}"
                            },
                            "type": "image_url"
                        },
                        {
                            "text": """请仔细分析这张照片中的人物和画面，提取以下四个维度的特征。其中，gender，style和vibe只能括号中从下面提供的选项中选择。请用JSON格式回答：

1. gender: 性别 (male/female/unisex)
2. style: 风格偏好 (运动/商务/可爱/简约/复古/街头/文艺/甜酷)
3. vibe: 气质氛围 (活力四射/成熟稳重/温柔优雅/酷炫前卫/独立神秘/清新自然/时尚前卫/温暖亲和)
4. color_palette: 画面主要颜色，请从可用的选项中提取3种至5种颜色 (red/blue/green/yellow/purple/pink/orange/brown/black/white/gray/navy/coral/cream/beige/mint/lavender/peach/turquoise/gold/silver)

请严格按照以下JSON格式回答，不要添加其他内容：
{
    "gender": "female",
    "style": "可爱",
    "vibe": "温柔优雅",
    "color_palette": "red, yellow, silver, mint, lavender"
}""",
                            "type": "text"
                        }
                    ],
                    "role": "user"
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_token}"
        }
        
        response = requests.post(self._api_url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        print("Getting result")
        content = result['choices'][0]['message']['content']
        
        user_tags = json.loads(content)
        return user_tags

class SockMapper:
    """Maps user characteristics to sock design"""
    
    @staticmethod
    def map_user_to_socks(user_tags: AnalysisResult) -> SockDesign:
        shape_mapping = {
            "male": "Athletic Style",
            "female": "Refined Cuff Style",
            "unisex": "Comfortable Universal Style"
        }

        material_mapping = {
            "运动": "Breathable Mesh Fabric",
            "商务": "Premium Combed Cotton",
            "可爱": "Soft Terry Fabric",
            "简约": "Premium Pure Cotton Fabric",
            "复古": "Classic Wool Blend",
            "街头": "Durable Nylon Blend",
            "文艺": "Natural Linen Blend",
            "甜酷": "Smooth Lycra Blend"
        }

        pattern_mapping = {
            "活力四射": "Dynamic Stripe Pattern",
            "成熟稳重": "Classic Plaid Pattern",
            "温柔优雅": "Delicate Lace Pattern",
            "酷炫前卫": "Geometric Abstract Pattern",
            "独立神秘": "Dark Color Pattern",
            "清新自然": "Simple Solid Pattern",
            "时尚前卫": "Modern Print Pattern",
            "温暖亲和": "Warm Floral Pattern"
        }

        color_mapping = {
            "red": "Classic Red",
            "blue": "Elegant Blue",
            "green": "Fresh Green",
            "yellow": "Bright Yellow",
            "purple": "Mysterious Purple",
            "pink": "Gentle Pink",
            "orange": "Vibrant Orange",
            "brown": "Warm Brown",
            "black": "Classic Black",
            "white": "Pure White",
            "gray": "Elegant Gray",
            "navy": "Deep Navy Blue",
            "coral": "Coral Red",
            "cream": "Cream Beige",
            "beige": "Warm Beige",
            "mint": "Mint Green",
            "lavender": "Light Lavender Purple",
            "peach": "Peach Color",
            "turquoise": "Turquoise Green",
            "gold": "Gold",
            "silver": "Silver"
        }

        # Extract colors from user tags
        users_colors = user_tags.get("color_palette", "").lower()
        color_list = []
        
        for usr_color in color_mapping:
            if usr_color in users_colors:
                color_list.append(color_mapping[usr_color])
        
        colors = ' + '.join(color_list)

        # Map characteristics
        shape = shape_mapping[user_tags['gender']]
        material = material_mapping[user_tags['style']]
        pattern = pattern_mapping[user_tags['vibe']]

        return {
            'shape': shape,
            'material': material,
            'pattern': pattern,
            'colors': colors
        }

# Convenience function for backward compatibility
def analyze_user_photo_thru_doubao(photo) -> AnalysisResult:
    """Legacy function for backward compatibility"""
    analyzer = DoubaoAnalyzer(
        api_token=os.getenv("DOUBAO_API_TOKEN"),
        api_url=os.getenv("DOUBAO_API_URL")
    )
    params = AnalyzerParams(
        image=photo,
        api_token=os.getenv("DOUBAO_API_TOKEN"),
        api_url=os.getenv("DOUBAO_API_URL")
    )
    return analyzer.analyze(params)

def map_user_to_socks(user_tags: AnalysisResult) -> SockDesign:
    """Legacy function for backward compatibility"""
    return SockMapper.map_user_to_socks(user_tags)


