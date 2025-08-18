#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Stable Diffusion API集成
"""

import requests
import json

def test_stable_diffusion_api():
    """测试Stable Diffusion API"""
    
    # API配置
    api_key = "rPpxeWVde2EUlnw4HBK5ZLwD5RFJxxA97CqG3Ry8W6voEQNq5xQhqsfWeOMi"
    url = "https://modelslab.com/api/v7/images/text-to-image"
    
    headers = {
        "key": api_key,
        "Content-Type": "application/json"
    }
    
    # 测试袜子图片生成
    sock_prompt = "a beautiful cream white sock, elegant cuff design, soft terry fabric, delicate lace pattern, high quality product photo, e-commerce display, professional photography, clean white background, soft lighting, detailed texture, realistic"
    
    data = {
        "key": api_key,
        "prompt": sock_prompt,
        "model_id": "imagen-4",
        "aspect_ratio": "1:1"
    }
    
    print("🧪 测试Stable Diffusion API生成袜子图片")
    print("=" * 60)
    print(f"📝 提示词: {sock_prompt}")
    print(f"🔗 API端点: {url}")
    print(f"🔑 API密钥: {api_key[:8]}...")
    
    try:
        print("\n🚀 发送请求...")
        response = requests.post(url, headers=headers, json=data, timeout=120)
        
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📋 响应头: {dict(response.headers)}")
        
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
    image_url = test_stable_diffusion_api()
    
    if image_url:
        print(f"\n🎯 测试结果: 成功生成图片")
        print(f"🔗 图片链接: {image_url}")
    else:
        print(f"\n❌ 测试结果: 图片生成失败")
