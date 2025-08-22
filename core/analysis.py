import requests
from PIL import Image
import io
import json
import base64
import os

class Analyzer:

    @staticmethod
    def analyze_user_photo_thru_doubao(photo):
        try:
            # import env var
            doubao_api_token = os.getenv("DOUBAO_API_TOKEN")
            doubao_api_url = os.getenv("DOUBAO_API_URL")

            # 将照片转换为base64
            img = Image.open(photo)
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='JPEG')
            img_str = base64.b64encode(img_buffer.getvalue()).decode()
            
            # 构建请求数据
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

                                            下面是一个范例，请严格按照以下JSON格式回答，不要添加其他内容：
                                            {
                                                "gender": "female",
                                                "style": "可爱",
                                                "vibe": "温柔优雅",
                                                "color_palette": "red, yellow, silver, mint, lavender"
                                            }
                                            
                                            下面的范例都是不行的：
                                            {
                                                "gender": "男", # 不行，因为选项中只有male/female/unisex，而男不在gender选项中
                                                "style": "坚毅", # 不行，没有在选项中
                                                "vibe": "温柔优雅", # 可以，在选项中
                                                "color_palette": "red, yellow, silver, mint, cyan" #不行，cyan不在选项中
                                            } 
                                            """,
                                "type": "text"
                            }
                        ],
                        "role": "user"
                    }
                ]
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {doubao_api_token}"
            }
            
            print("🔍 正在分析用户照片...")
            response = requests.post(doubao_api_url, headers=headers, json=data, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # 尝试解析JSON
                try:
                    user_tags = json.loads(content)
                    print("✅ 用户照片分析成功!")
                    print(f"📝 分析结果: {content}")
                    return user_tags
                except json.JSONDecodeError:
                    print("⚠️ 返回的不是有效JSON，使用默认标签")
                    
            else:
                print(f"❌ 豆包API调用失败: {response.status_code}")
                
                
        except Exception as e:
            print(f"❌ 分析用户照片时出错: {e}")

def map_user_to_socks(user_tags):
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

    # Correspondings of color in user_tags
    users_colors = user_tags.get("color_palette", "").lower()
    color_list = []
    
    for usr_color in color_mapping:
        if usr_color in users_colors:
            color_list.append(color_mapping[usr_color])
    
    colors = ' + '.join(color_list)

    # Correspondings of gender in user_tags
    shape = shape_mapping[user_tags['gender']]
    material = material_mapping[user_tags['style']]
    pattern = pattern_mapping[user_tags['vibe']]

    sock_tags = {
        'shape':shape,
        'material': material,
        'pattern': pattern,
        'colors': colors
    }

    return sock_tags


