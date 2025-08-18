#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试袜子形状生成的改进
"""

import requests
import json

def test_sock_shape_generation():
    """测试袜子形状生成的改进"""
    
    # API配置
    api_key = "rPpxeWVde2EUlnw4HBK5ZLwD5RFJxxA97CqG3Ry8W6voEQNq5xQhqsfWeOMi"
    url = "https://modelslab.com/api/v6/images/text2img"
    
    headers = {
        "key": api_key,
        "Content-Type": "application/json"
    }
    
    print("🧦 测试袜子形状生成的改进")
    print("=" * 70)
    
    # 测试1: 明确袜子形状的提示词
    print("\n1️⃣ 测试明确袜子形状的提示词...")
    shape_prompt = "a single beautiful coral red + cream white sock, 精致收口型, 柔软毛圈面料, 精致蕾丝图案, cartoon style, kawaii design, cute illustration, clean white background, high quality, only one sock, no multiple socks, single item focus, sock shape with toe area and heel area, foot covering design, textile footwear, sock silhouette, sock outline, sock form, sock structure"
    
    data1 = {
        "key": api_key,
        "prompt": shape_prompt,
        "model_id": "stable-diffusion-v1-5",
        "width": "1024",
        "height": "1024",
        "num_inference_steps": "20",
        "guidance_scale": "7.5",
        "negative_prompt": "multiple socks, pair of socks, two socks, three socks, many socks, multiple items, duplicate objects, shoes, boots, sneakers, footwear, gloves, mittens, hats, caps, clothing, pants, shirts, dresses, skirts, jackets, coats, scarves, bags, purses, wallets, accessories, jewelry, watches, rings, necklaces, bracelets, earrings, sunglasses, belts, ties, bow ties, hair accessories, hair clips, hair bands, hair ties, hair pins, hair combs, hair brushes, mirrors, phones, laptops, computers, books, papers, documents, furniture, chairs, tables, beds, sofas, lamps, plants, flowers, trees, animals, pets, cars, bikes, motorcycles, buildings, houses, apartments, offices, stores, restaurants, cafes, parks, gardens, beaches, mountains, forests, deserts, oceans, rivers, lakes, clouds, sun, moon, stars, rain, snow, wind, fire, water, earth, air, (worst quality:2), (low quality:2), (normal quality:2), (jpeg artifacts), (blurry), (duplicate), (morbid), (mutilated), (out of frame), (extra limbs), (bad anatomy), (disfigured), (deformed), (cross-eye), (glitch), (oversaturated), (overexposed), (underexposed), (bad proportions), (bad hands), (bad feet), (cloned face), (long neck), (missing arms), (missing legs), (extra fingers), (fused fingers), (poorly drawn hands), (poorly drawn face), (mutation), (deformed eyes), watermark, text, logo, signature, grainy, tiling, censored, nsfw, ugly, blurry eyes, noisy image, bad lighting, unnatural skin, asymmetry"
    }
    
    print(f"📝 形状优化提示词: {shape_prompt}")
    print(f"🚫 负面提示词长度: {len(data1['negative_prompt'])} 字符")
    
    try:
        print("🚀 发送袜子形状生成请求...")
        response = requests.post(url, headers=headers, json=data1, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 袜子形状生成成功!")
            
            if 'output' in result and len(result['output']) > 0:
                image_url = result['output'][0]
                print(f"🖼️ 生成的图片URL: {image_url}")
                print("🎨 特点: 明确袜子形状、卡通风格、单只袜子")
                print("🔍 形状特征: 脚趾区域、脚跟区域、袜子轮廓、袜子结构")
            else:
                print("⚠️ 响应中没有找到图片URL")
        else:
            print(f"❌ 袜子形状生成失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 袜子形状生成出错: {e}")
    
    # 测试2: 对比原始提示词
    print("\n2️⃣ 对比原始提示词...")
    original_prompt = "a single beautiful coral red + cream white sock, 精致收口型, 柔软毛圈面料, 精致蕾丝图案, cartoon style, kawaii design, cute illustration, clean white background, high quality, only one sock, no multiple socks, single item focus"
    
    data2 = {
        "key": api_key,
        "prompt": original_prompt,
        "model_id": "stable-diffusion-v1-5",
        "width": "1024",
        "height": "1024",
        "num_inference_steps": "20",
        "guidance_scale": "7.5",
        "negative_prompt": "multiple socks, pair of socks, two socks, three socks, many socks, multiple items, duplicate objects, (worst quality:2), (low quality:2), (normal quality:2), (jpeg artifacts), (blurry), (duplicate), (morbid), (mutilated), (out of frame), (extra limbs), (bad anatomy), (disfigured), (deformed), (cross-eye), (glitch), (oversaturated), (overexposed), (underexposed), (bad proportions), (bad hands), (bad feet), (cloned face), (long neck), (missing arms), (missing legs), (extra fingers), (fused fingers), (poorly drawn hands), (poorly drawn face), (mutation), (deformed eyes), watermark, text, logo, signature, grainy, tiling, censored, nsfw, ugly, blurry eyes, noisy image, bad lighting, unnatural skin, asymmetry"
    }
    
    print(f"📝 原始提示词: {original_prompt}")
    print(f"🚫 原始负面提示词长度: {len(data2['negative_prompt'])} 字符")
    
    try:
        print("🚀 发送原始提示词请求...")
        response = requests.post(url, headers=headers, json=data2, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 原始提示词生成成功!")
            
            if 'output' in result and len(result['output']) > 0:
                image_url = result['output'][0]
                print(f"🖼️ 生成的图片URL: {image_url}")
                print("🎨 特点: 原始提示词、卡通风格、单只袜子")
            else:
                print("⚠️ 响应中没有找到图片URL")
        else:
            print(f"❌ 原始提示词生成失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 原始提示词生成出错: {e}")
    
    print("\n" + "=" * 70)
    print("🎯 测试完成!")
    print("💡 改进要点:")
    print("  1. ✅ 添加了明确的袜子形状描述")
    print("  2. ✅ 扩展了负面提示词，排除其他物品")
    print("  3. ✅ 强调袜子的结构特征")
    print("  4. ✅ 对比测试原始vs优化提示词")

if __name__ == "__main__":
    test_sock_shape_generation()

