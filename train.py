#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
袜子个性化设计系统 - 优化版本
核心理念：把每个人变成一只袜子！
"""

import os
import requests
import json
import base64
from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
from core.analysis import Analyzer, map_user_to_socks
from core.generator.base import HFGenerator

app = Flask(__name__)

def analyze_user_photo(photo):
    """分析用户照片，提取四个维度的特征"""
    try:
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
                            "text": """请仔细分析这张照片中的人物和画面，提取以下四个维度的特征，请用JSON格式回答：

1. gender: 性别 (male/female/unisex)
2. style: 风格偏好 (运动/商务/可爱/简约/复古/街头/文艺/甜酷)
3. vibe: 气质氛围 (活力四射/成熟稳重/温柔优雅/酷炫前卫/独立神秘/清新自然/时尚前卫/温暖亲和)
4. color_palette: 画面主要颜色 (请提取画面中面积最大的3-5种主要颜色，用英文描述，如: "coral red, cream white, warm beige, navy blue, soft pink")

请严格按照以下JSON格式回答，不要添加其他内容：
{
  "gender": "female",
  "style": "可爱",
  "vibe": "温柔优雅",
  "color_palette": "coral red, cream white, warm beige, navy blue, soft pink"
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
            "Authorization": f"Bearer {os.getenv("DOUBAO_API_TOKEN")}"
        }
        
        print("🔍 正在分析用户照片...")
        response = requests.post(DOUBAO_API_URL, headers=headers, json=data, timeout=120)
        
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
                return get_default_user_tags()
        else:
            print(f"❌ 豆包API调用失败: {response.status_code}")
            return get_default_user_tags()
            
    except Exception as e:
        print(f"❌ 分析用户照片时出错: {e}")
        return get_default_user_tags()

def get_default_user_tags():
    """获取默认用户标签"""
    return {
        "gender": "unisex",
        "style": "简约",
        "vibe": "清新自然",
        "color_palette": "classic black, elegant gray"
    }

def map_user_to_sock(user_tags):
    """将用户标签映射到袜子标签"""
    # 性别到形状的映射
    shape_mapping = {
        "male": "运动型",
        "female": "精致收口型",
        "unisex": "舒适通用型"
    }
    
    # 风格到材质的映射
    material_mapping = {
        "运动": "透气网眼面料",
        "商务": "优质精梳棉",
        "可爱": "柔软毛圈面料",
        "简约": "优质纯棉面料",
        "复古": "经典羊毛混纺",
        "街头": "耐磨尼龙混纺",
        "文艺": "天然亚麻混纺",
        "甜酷": "丝滑莱卡混纺"
    }
    
    # 气质到图案的映射
    pattern_mapping = {
        "活力四射": "动感条纹图案",
        "成熟稳重": "经典格纹图案",
        "温柔优雅": "精致蕾丝图案",
        "酷炫前卫": "几何抽象图案",
        "独立神秘": "暗色系图案",
        "清新自然": "简约纯色图案",
        "时尚前卫": "现代印花图案",
        "温暖亲和": "温馨花卉图案"
    }
    
    # 颜色映射
    color_mapping = {
        "red": "经典红色",
        "blue": "优雅蓝色",
        "green": "清新绿色",
        "yellow": "明亮黄色",
        "purple": "神秘紫色",
        "pink": "温柔粉色",
        "orange": "活力橙色",
        "brown": "温暖棕色",
        "black": "经典黑色",
        "white": "纯净白色",
        "gray": "优雅灰色",
        "navy": "深蓝海军色",
        "coral": "珊瑚红色",
        "cream": "奶油米色",
        "beige": "暖米色",
        "mint": "薄荷绿色",
        "lavender": "淡紫薰衣草色",
        "peach": "蜜桃色",
        "turquoise": "青绿色",
        "gold": "金色",
        "silver": "银色"
    }
    
    # 提取用户照片的主要颜色 - 使用所有提取的颜色
    user_colors = user_tags.get("color_palette", "").lower()
    sock_colors = []
    
    # 从用户颜色中提取袜子颜色
    for eng_color, chn_color in color_mapping.items():
        if eng_color in user_colors:
            sock_colors.append(chn_color)
    
    # 如果没有匹配到具体颜色，使用默认颜色
    if not sock_colors:
        sock_colors = ["经典黑色", "优雅灰色"]
    
    # 使用所有提取的颜色（最多5种）
    color_text = " + ".join(sock_colors[:5])
    
    # 构建袜子标签
    sock_tags = {
        "shape": shape_mapping.get(user_tags.get("gender", "unisex"), "舒适通用型"),
        "material": material_mapping.get(user_tags.get("style", "简约"), "优质纯棉面料"),
        "pattern": pattern_mapping.get(user_tags.get("vibe", "清新自然"), "简约纯色图案"),
        "color": color_text  # 使用所有提取的颜色
    }
    
    return sock_tags

def generate_sock_image(sock_tags):
    """生成袜子图片"""
    try:
        print("🎨 正在使用Stable Diffusion API生成袜子图片...")
        
        # 构建英文提示词，适合Stable Diffusion - 明确袜子形状，卡通风格，严格控制袜子数量
        prompt = f"a single beautiful {sock_tags['color']} sock, {sock_tags['shape']}, {sock_tags['material']}, {sock_tags['pattern']}, cartoon style, kawaii design, cute illustration, clean white background, high quality, only one sock, no multiple socks, single item focus, sock shape with toe area and heel area, foot covering design, textile footwear, sock silhouette, sock outline, sock form, sock structure, ONE SOCK ONLY, single sock design, isolated sock, solo sock"
        
        print(f"📝 提示词: {prompt}")
        
        # 尝试使用Stable Diffusion API
        try:
            image_url = generate_with_stable_diffusion(prompt)
            if image_url:
                print("✅ Stable Diffusion袜子图片生成成功!")
                return image_url
        except Exception as e:
            print(f"⚠️ Stable Diffusion生成失败: {e}")
        
        # 如果Stable Diffusion失败，使用占位符图片
        print("⚠️ 使用占位符图片")
        return generate_placeholder_image(sock_tags)
        
    except Exception as e:
        print(f"❌ 生成袜子图片时出错: {e}")
        return generate_placeholder_image(sock_tags)
'''
def generate_with_stable_diffusion(prompt):
    """使用Stable Diffusion API生成图片"""
    try:
        print("🔄 调用免费Stable Diffusion API...")
        print(f"🔗 API端点: {STABLE_DIFFUSION_URL}")
        print(f"📝 提示词: {prompt}")
        
        headers = {
            "key": STABLE_DIFFUSION_API_KEY,
            "Content-Type": "application/json"
        }
        
        # 构建请求数据 - 使用免费API格式，严格控制袜子数量
        data = {
            "key": STABLE_DIFFUSION_API_KEY,
            "prompt": prompt,
            "model_id": "stable-diffusion-v1-5",  # 使用可用的免费模型
            "width": "1024",
            "height": "1024",
            "num_inference_steps": "20",  # 减少步数以加快生成速度
            "guidance_scale": "7.5",
            "watermark": "no",  # 关闭水印
            "negative_prompt": "multiple socks, pair of socks, two socks, three socks, many socks, multiple items, duplicate objects, shoes, boots, sneakers, footwear, gloves, mittens, hats, caps, clothing, pants, shirts, dresses, skirts, jackets, coats, scarves, bags, purses, wallets, accessories, jewelry, watches, rings, necklaces, bracelets, earrings, sunglasses, belts, ties, bow ties, hair accessories, hair clips, hair bands, hair ties, hair pins, hair combs, hair brushes, mirrors, phones, laptops, computers, books, papers, documents, furniture, chairs, tables, beds, sofas, lamps, plants, flowers, trees, animals, pets, cars, bikes, motorcycles, buildings, houses, apartments, offices, stores, restaurants, cafes, parks, gardens, beaches, mountains, forests, deserts, oceans, rivers, lakes, clouds, sun, moon, stars, rain, snow, wind, fire, water, earth, air, (worst quality:2), (low quality:2), (normal quality:2), (jpeg artifacts), (blurry), (duplicate), (morbid), (mutilated), (out of frame), (extra limbs), (bad anatomy), (disfigured), (deformed), (cross-eye), (glitch), (oversaturated), (overexposed), (underexposed), (bad proportions), (bad hands), (bad feet), (cloned face), (long neck), (missing arms), (missing legs), (extra fingers), (fused fingers), (poorly drawn hands), (poorly drawn face), (mutation), (deformed eyes), watermark, text, logo, signature, grainy, tiling, censored, nsfw, ugly, blurry eyes, noisy image, bad lighting, unnatural skin, asymmetry, (multiple:1.5), (duplicate:1.5), (repetition:1.5), (clones:1.5), (copies:1.5), (similar items:1.5), (identical objects:1.5), (repeated elements:1.5), (multiple instances:1.5), (several items:1.5), (group of objects:1.5), (collection of items:1.5), (set of objects:1.5), (bunch of items:1.5), (cluster of objects:1.5), (array of items:1.5), (series of objects:1.5), (sequence of items:1.5), (line of objects:1.5), (row of items:1.5), (column of objects:1.5), (grid of items:1.5), (pattern of objects:1.5), (arrangement of items:1.5), (layout of objects:1.5), (composition of items:1.5), (assembly of objects:1.5), (formation of items:1.5), (structure of objects:1.5), (system of items:1.5), (network of objects:1.5), (web of items:1.5), (mesh of objects:1.5), (matrix of items:1.5), (array of objects:1.5), (field of items:1.5), (area of objects:1.5), (zone of items:1.5), (region of objects:1.5), (section of items:1.5), (part of objects:1.5), (portion of items:1.5), (fraction of objects:1.5), (segment of items:1.5), (division of objects:1.5), (subdivision of items:1.5), (subsection of objects:1.5), (subpart of items:1.5), (subportion of objects:1.5), (subfraction of items:1.5), (subsegment of objects:1.5), (subdivision of items:1.5), (subsubsection of objects:1.5), (subsubpart of items:1.5), (subsubportion of objects:1.5), (subsubfraction of items:1.5), (subsubsegment of objects:1.5), (subsubsubdivision of items:1.5), (subsubsubsubsection of objects:1.5), (subsubsubsubpart of items:1.5), (subsubsubsubportion of objects:1.5), (subsubsubsubfraction of items:1.5), (subsubsubsubsegment of objects:1.5), (subsubsubsubsubdivision of items:1.5), (subsubsubsubsubsubsection of objects:1.5), (subsubsubsubsubsubpart of items:1.5), (subsubsubsubsubsubportion of objects:1.5), (subsubsubsubsubsubfraction of items:1.5), (subsubsubsubsubsubsegment of objects:1.5), (subsubsubsubsubsubsubdivision of items:1.5), (subsubsubsubsubsubsubsubsubsection of objects:1.5), (subsubsubsubsubsubsubsubsubpart of items:1.5), (subsubsubsubsubsubsubsubsubsubportion of objects:1.5), (subsubsubsubsubsubsubsubsubsubfraction of items:1.5), (subsubsubsubsubsubsubsubsubsubsegment of objects:1.5), (subsubsubsubsubsubsubsubsubsubsubdivision of items:1.5), (subsubsubsubsubsubsubsubsubsubsubsubsubsection of objects:1.5), (subsubsubsubsubsubsubsubsubsubsubsubpart of items:1.5), (subsubsubsubsubsubsubsubsubsubsubsubportion of objects:1.5), (subsubsubsubsubsubsubsubsubsubsubsubsubfraction of items:1.5), (subsubsubsubsubsubsubsubsubsubsubsubsubsegment of objects:1.5), (subsubsubsubsubsubsubsubsubsubsubsubsubsubdivision of items:1.5), (subsubsubsubsubsubsubsubsubsubsubsubsubsubsubsection of objects:1.5), (subsubsubsubsubsubsubsubsubsubsubsubsubsubpart of items:1.5), (subsubsubsubsubsubsubsubsubsubsubsubsubsubsubportion of objects:1.5), (subsubsubsubsubsubsubsubsubsubsubsubsubsubsubfraction of items:1.5), (subsubsubsubsubsubsubsubsubsubsubsubsubsubsubsegment of objects:1.5), (subsubsubsubsubsubsubsubsubsubsubsubsubsubsubsubdivision of items:1.5), (subsubsubsubsubsubsubsubsubsubsubsubsubsubsubsubsubsection of items:1.5)"
        }
        
        response = requests.post(STABLE_DIFFUSION_URL, headers=headers, json=data, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Stable Diffusion API调用成功!")
            print(f"📊 响应: {result}")
            
            if 'output' in result and len(result['output']) > 0:
                image_url = result['output'][0]
                print(f"🖼️ 生成的图片URL: {image_url}")
                return image_url
            else:
                print("⚠️ 响应中没有找到图片URL")
                return None
        else:
            print(f"❌ Stable Diffusion API调用失败: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Stable Diffusion生成出错: {e}")
        return None

def generate_placeholder_image(sock_tags):
    """生成占位符图片"""
    try:
        print("🎨 生成占位符图片...")
        
        # 使用via.placeholder.com生成占位符图片
        color = "666666"  # 默认颜色
        text = f"{sock_tags['color']} {sock_tags['shape']} {sock_tags['material']} {sock_tags['pattern']}"
        
        # 清理文本，移除特殊字符
        text = text.replace(" ", "%20").replace("+", "%2B")
        
        placeholder_url = f"https://via.placeholder.com/800x600/{color}/FFFFFF?text={text}"
        print(f"🖼️ 占位符图片URL: {placeholder_url}")
        
        return placeholder_url
        
    except Exception as e:
        print(f"❌ 生成占位符图片时出错: {e}")
        return "https://via.placeholder.com/800x600/666666/FFFFFF?text=袜子生成失败"
'''

@app.route('/')
def home():
    """主页"""
    if request.method == 'POST':
        try:
            # 获取上传的照片
            if 'photo' not in request.files:
                return jsonify({"error": "没有上传照片"})
            
            photo = request.files['photo']
            if photo.filename == '':
                return jsonify({"error": "没有选择照片"})
            
            # 分析用户照片
            user_tags = Analyzer.analyze_user_photo_thru_doubao(photo)
            print(f"🎯 用户标签: {user_tags}")
            
            # 映射到袜子标签
            sock_tags = map_user_to_sock(user_tags)
            print(f"🧦 袜子标签: {sock_tags}")
            
            hf_api_url = os.getenv('HF_API_URL')
            hf_api_token = os.getenv('HF_API_TOKEN')

            # 生成袜子图片
            #TO-DO: FIX THIS
            hf_generator = HFGenerator(hf_api_token, hf_api_url)
            image = hf_generator.generate()
            
            # 返回结果
            return render_template('result.html', 
                                user_tags=user_tags, 
                                sock_tags=sock_tags, 
                                image_url=image)
            
        except Exception as e:
            print(f"❌ 处理请求时出错: {e}")
            return jsonify({"error": f"处理请求时出错: {e}"})
    
    return render_template('upload.html')

if __name__ == '__main__':
    if DOUBAO_API_TOKEN:
        print("✅ 豆包API Token已配置，将使用豆包AI模型")
    else:
        print("❌ 错误: 未设置DOUBAO_API_TOKEN")
        exit(1)
    
    print("🚀 启动袜子个性化设计系统...")
    print("🎯 核心理念：把每个人变成一只袜子！")
    
    app.run(debug=True, port=5001)
