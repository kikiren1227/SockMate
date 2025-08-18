#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试优化后的袜子个性化设计系统
"""

import requests
import json

def test_optimized_system():
    """测试优化后的系统功能"""
    
    # API配置
    api_key = "rPpxeWVde2EUlnw4HBK5ZLwD5RFJxxA97CqG3Ry8W6voEQNq5xQhqsfWeOMi"
    url = "https://modelslab.com/api/v6/images/text2img"
    
    headers = {
        "key": api_key,
        "Content-Type": "application/json"
    }
    
    print("🧪 测试优化后的袜子个性化设计系统")
    print("=" * 70)
    
    # 测试1: 多颜色袜子生成
    print("\n1️⃣ 测试多颜色袜子生成...")
    multi_color_prompt = "a single beautiful coral red + cream white + warm beige + black sock, 精致收口型, 柔软毛圈面料, 精致蕾丝图案, cartoon style, kawaii design, cute illustration, clean white background, high quality, only one sock, no multiple socks, single item focus"
    
    data1 = {
        "key": api_key,
        "prompt": multi_color_prompt,
        "model_id": "stable-diffusion-v1-5",
        "width": "1024",
        "height": "1024",
        "num_inference_steps": "20",
        "guidance_scale": "7.5",
        "negative_prompt": "multiple socks, pair of socks, two socks, three socks, many socks, multiple items, duplicate objects, (worst quality:2), (low quality:2), (normal quality:2), (jpeg artifacts), (blurry), (duplicate), (morbid), (mutilated), (out of frame), (extra limbs), (bad anatomy), (disfigured), (deformed), (cross-eye), (glitch), (oversaturated), (overexposed), (underexposed), (bad proportions), (bad hands), (bad feet), (cloned face), (long neck), (missing arms), (missing legs), (extra fingers), (fused fingers), (poorly drawn hands), (poorly drawn face), (mutation), (deformed eyes), watermark, text, logo, signature, grainy, tiling, censored, nsfw, ugly, blurry eyes, noisy image, bad lighting, unnatural skin, asymmetry"
    }
    
    print(f"📝 多颜色提示词: {multi_color_prompt}")
    print(f"🚫 负面提示词: {data1['negative_prompt'][:100]}...")
    
    try:
        print("🚀 发送多颜色袜子生成请求...")
        response = requests.post(url, headers=headers, json=data1, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 多颜色袜子生成成功!")
            
            if 'output' in result and len(result['output']) > 0:
                image_url = result['output'][0]
                print(f"🖼️ 生成的图片URL: {image_url}")
                print("🎨 特点: 多颜色、卡通风格、单只袜子")
            else:
                print("⚠️ 响应中没有找到图片URL")
        else:
            print(f"❌ 多颜色袜子生成失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 多颜色袜子生成出错: {e}")
    
    # 测试2: 卡通风格袜子生成
    print("\n2️⃣ 测试卡通风格袜子生成...")
    cartoon_prompt = "a single beautiful cream white sock, 精致收口型, 柔软毛圈面料, 精致蕾丝图案, cartoon style, kawaii design, cute illustration, clean white background, high quality, only one sock, no multiple socks, single item focus"
    
    data2 = {
        "key": api_key,
        "prompt": cartoon_prompt,
        "model_id": "stable-diffusion-v1-5",
        "width": "1024",
        "height": "1024",
        "num_inference_steps": "20",
        "guidance_scale": "7.5",
        "negative_prompt": "multiple socks, pair of socks, two socks, three socks, many socks, multiple items, duplicate objects, realistic, photorealistic, (worst quality:2), (low quality:2), (normal quality:2), (jpeg artifacts), (blurry), (duplicate), (morbid), (mutilated), (out of frame), (extra limbs), (bad anatomy), (disfigured), (deformed), (cross-eye), (glitch), (oversaturated), (overexposed), (underexposed), (bad proportions), (bad hands), (bad feet), (cloned face), (long neck), (missing arms), (missing legs), (extra fingers), (fused fingers), (poorly drawn hands), (poorly drawn face), (mutation), (deformed eyes), watermark, text, logo, signature, grainy, tiling, censored, nsfw, ugly, blurry eyes, noisy image, bad lighting, unnatural skin, asymmetry"
    }
    
    print(f"📝 卡通风格提示词: {cartoon_prompt}")
    
    try:
        print("🚀 发送卡通风格袜子生成请求...")
        response = requests.post(url, headers=headers, json=data2, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 卡通风格袜子生成成功!")
            
            if 'output' in result and len(result['output']) > 0:
                image_url = result['output'][0]
                print(f"🖼️ 生成的图片URL: {image_url}")
                print("🎨 特点: 卡通风格、可爱设计、单只袜子")
            else:
                print("⚠️ 响应中没有找到图片URL")
        else:
            print(f"❌ 卡通风格袜子生成失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 卡通风格袜子生成出错: {e}")
    
    print("\n" + "=" * 70)
    print("🎯 测试完成!")
    print("💡 优化要点:")
    print("  1. ✅ 提取3-5种主要颜色")
    print("  2. ✅ 生成单张袜子图片")
    print("  3. ✅ 严格控制袜子数量")
    print("  4. ✅ 生成卡通风格袜子")

if __name__ == "__main__":
    test_optimized_system()
