#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试免费的Stable Diffusion API
"""

import requests
import json

def test_free_stable_diffusion_api():
    """测试免费的Stable Diffusion API"""
    
    # API配置
    api_key = "rPpxeWVde2EUlnw4HBK5ZLwD5RFJxxA97CqG3Ry8W6voEQNq5xQhqsfWeOMi"
    url = "https://modelslab.com/api/v6/images/text2img"
    
    headers = {
        "key": api_key,
        "Content-Type": "application/json"
    }
    
    # 测试袜子图片生成 - 使用袜子相关的提示词
    sock_prompt = "R3alisticF, beautiful elegant sock, cream white color, soft terry fabric, delicate lace pattern, high quality product photo, e-commerce display, professional photography, clean white background, soft lighting, detailed texture, realistic, perfect composition"
    
    data = {
        "key": api_key,
        "prompt": sock_prompt,
        "model_id": "villainous-villanizer-turn-anything-into-a-villain-flux-v1-0",
        "lora_model": None,
        "width": "1024",
        "height": "1024",
        "negative_prompt": "(worst quality:2), (low quality:2), (normal quality:2), (jpeg artifacts), (blurry), (duplicate), (morbid), (mutilated), (out of frame), (extra limbs), (bad anatomy), (disfigured), (deformed), (cross-eye), (glitch), (oversaturated), (overexposed), (underexposed), (bad proportions), (bad hands), (bad feet), (cloned face), (long neck), (missing arms), (missing legs), (extra fingers), (fused fingers), (poorly drawn hands), (poorly drawn face), (mutation), (deformed eyes), watermark, text, logo, signature, grainy, tiling, censored, nsfw, ugly, blurry eyes, noisy image, bad lighting, unnatural skin, asymmetry",
        "num_inference_steps": "31",
        "scheduler": "DPMSolverMultistepScheduler",
        "guidance_scale": "7.5",
        "enhance_prompt": None
    }
    
    print("🧪 测试免费Stable Diffusion API生成袜子图片")
    print("=" * 70)
    print(f"📝 提示词: {sock_prompt}")
    print(f"🔗 API端点: {url}")
    print(f"🔑 API密钥: {api_key[:8]}...")
    print(f"🤖 模型: {data['model_id']}")
    
    try:
        print("\n🚀 发送请求...")
        response = requests.post(url, headers=headers, json=data, timeout=120)
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功!")
            print(f"📝 响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # 检查是否包含图片URL
            if 'output' in result and len(result['output']) > 0:
                image_url = result['output'][0]
                print(f"\n🎉 成功生成袜子图片!")
                print(f"🖼️ 图片URL: {image_url}")
                return image_url
            elif 'images' in result and len(result['images']) > 0:
                image_url = result['images'][0]
                print(f"\n🎉 成功生成袜子图片!")
                print(f"🖼️ 图片URL: {image_url}")
                return image_url
            elif 'url' in result:
                image_url = result['url']
                print(f"\n🎉 成功生成袜子图片!")
                print(f"🖼️ 图片URL: {image_url}")
                return image_url
            else:
                print("\n⚠️ 响应中没有找到图片URL")
                print("请检查API响应格式")
                return None
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"📝 错误信息: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ 请求超时")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return None
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return None

if __name__ == "__main__":
    image_url = test_free_stable_diffusion_api()
    
    if image_url:
        print(f"\n🎯 测试结果: 成功生成图片")
        print(f"🔗 图片链接: {image_url}")
        print(f"🌐 你可以在浏览器中打开这个链接查看生成的袜子图片!")
    else:
        print(f"\n❌ 测试结果: 图片生成失败")
