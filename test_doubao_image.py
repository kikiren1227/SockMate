#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试豆包API的图像生成功能
"""

import requests
import json

def test_doubao_image_generation():
    """测试豆包API的图像生成功能"""
    
    # API配置
    api_token = "cacfd50c-e415-4e69-941b-e22b32705c27"
    base_url = "https://ark.cn-beijing.volces.com/api/v3"
    
    # 测试图像生成API
    print("🧪 测试豆包API图像生成功能")
    print("=" * 60)
    
    # 1. 测试图像生成端点
    print("\n1️⃣ 测试图像生成API端点...")
    image_url = f"{base_url}/images/generations"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    payload = {
        "prompt": "a beautiful red sock, elegant design, high quality product photo",
        "n": 1,
        "size": "1024x1024",
        "response_format": "url"
    }
    
    try:
        print(f"🔗 请求URL: {image_url}")
        print(f"📝 请求内容: {payload}")
        
        response = requests.post(
            image_url,
            headers=headers,
            json=payload,
            timeout=120
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📋 响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 图像生成API成功!")
            print(f"📝 响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if 'data' in result and len(result['data']) > 0:
                image_url = result['data'][0]['url']
                print(f"🖼️ 生成的图片URL: {image_url}")
            else:
                print("⚠️ 响应中没有图片数据")
        else:
            print(f"❌ 图像生成API失败")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 图像生成API调用出错: {e}")
    
    # 2. 测试聊天API的图像生成功能
    print("\n2️⃣ 测试聊天API的图像生成功能...")
    chat_url = f"{base_url}/chat/completions"
    
    chat_payload = {
        "model": "doubao-seed-1-6-250615",
        "messages": [
            {
                "content": [
                    {
                        "text": "请生成一张图片：一双红色袜子，精致设计，高质量产品图",
                        "type": "text"
                    }
                ],
                "role": "user"
            }
        ],
        "stream": False
    }
    
    try:
        print(f"🔗 请求URL: {chat_url}")
        print(f"📝 请求内容: {chat_payload}")
        
        response = requests.post(
            chat_url,
            headers=headers,
            json=chat_payload,
            timeout=120
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天API成功!")
            print(f"📝 响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"📝 返回内容类型: {type(content)}")
                print(f"📝 返回内容: {content[:500]}...")
                
                # 检查是否包含图像数据
                if isinstance(content, dict):
                    print("🔍 返回的是字典格式")
                    for key in content.keys():
                        print(f"  - {key}: {content[key]}")
                elif isinstance(content, str):
                    print("🔍 返回的是字符串格式")
                    if "图片" in content or "image" in content.lower():
                        print("✅ 可能包含图片相关信息")
                    else:
                        print("⚠️ 返回的是普通文本描述")
            else:
                print("❌ 响应中没有choices")
        else:
            print(f"❌ 聊天API失败")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 聊天API调用出错: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 测试完成!")

if __name__ == "__main__":
    test_doubao_image_generation()

