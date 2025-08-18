#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深入研究豆包API的图像生成能力
"""

import requests
import json

def research_doubao_image_generation():
    """深入研究豆包API的图像生成能力"""
    
    # API配置
    api_token = "cacfd50c-e415-4e69-941b-e22b32705c27"
    base_url = "https://ark.cn-beijing.volces.com/api/v3"
    
    print("🔬 深入研究豆包API图像生成能力")
    print("=" * 70)
    
    # 1. 测试不同的模型
    print("\n1️⃣ 测试不同的模型...")
    models_to_test = [
        "doubao-seed-1-6-250615",  # 当前使用的模型
        "doubao-seed",              # 基础模型
        "doubao",                   # 通用模型
        "doubao-vision",            # 视觉模型
        "doubao-multimodal"         # 多模态模型
    ]
    
    for model in models_to_test:
        print(f"\n🧪 测试模型: {model}")
        test_model_image_generation(base_url, api_token, model)
    
    # 2. 测试不同的API端点
    print("\n2️⃣ 测试不同的API端点...")
    endpoints_to_test = [
        "/images/generations",
        "/images/create", 
        "/images/generate",
        "/v1/images/generations",
        "/chat/completions"  # 已知工作的端点
    ]
    
    for endpoint in endpoints_to_test:
        print(f"\n🔗 测试端点: {endpoint}")
        test_endpoint(base_url, api_token, endpoint)
    
    # 3. 测试不同的请求格式
    print("\n3️⃣ 测试不同的请求格式...")
    test_request_formats(base_url, api_token)
    
    print("\n" + "=" * 70)
    print("🎯 研究完成!")

def test_model_image_generation(base_url, api_token, model):
    """测试特定模型的图像生成能力"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    # 测试聊天API
    chat_payload = {
        "model": model,
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
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=chat_payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ 模型 {model} 聊天API成功")
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                # 检查是否包含图像相关关键词
                image_keywords = ["图片", "image", "生成", "create", "generate", "photo", "photograph"]
                has_image_content = any(keyword in content.lower() for keyword in image_keywords)
                
                if has_image_content:
                    print(f"  🖼️ 模型 {model} 可能支持图像生成")
                    print(f"  📝 内容预览: {content[:100]}...")
                else:
                    print(f"  ⚠️ 模型 {model} 返回普通文本")
        else:
            print(f"  ❌ 模型 {model} 聊天API失败: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ 模型 {model} 测试出错: {e}")

def test_endpoint(base_url, api_token, endpoint):
    """测试特定的API端点"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    # 测试图像生成端点
    if "images" in endpoint:
        payload = {
            "prompt": "a beautiful red sock, elegant design, high quality product photo",
            "n": 1,
            "size": "1024x1024"
        }
        
        try:
            response = requests.post(
                f"{base_url}{endpoint}",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            print(f"  📊 状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ 端点 {endpoint} 成功!")
                print(f"  📝 响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            elif response.status_code == 404:
                print(f"  ❌ 端点 {endpoint} 不存在")
            elif response.status_code == 400:
                print(f"  ⚠️ 端点 {endpoint} 存在但参数错误")
                print(f"  📝 错误信息: {response.text}")
            else:
                print(f"  ⚠️ 端点 {endpoint} 其他错误: {response.status_code}")
                print(f"  📝 错误信息: {response.text}")
                
        except Exception as e:
            print(f"  ❌ 端点 {endpoint} 测试出错: {e}")

def test_request_formats(base_url, api_token, model="doubao-seed-1-6-250615"):
    """测试不同的请求格式"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    print(f"\n🧪 测试不同的请求格式 (模型: {model})...")
    
    # 格式1: 直接请求图像
    format1 = {
        "model": model,
        "messages": [
            {
                "content": "请生成一张图片：一双红色袜子",
                "role": "user"
            }
        ]
    }
    
    # 格式2: 多模态请求
    format2 = {
        "model": model,
        "messages": [
            {
                "content": [
                    {
                        "text": "请生成一张图片",
                        "type": "text"
                    }
                ],
                "role": "user"
            }
        ]
    }
    
    # 格式3: 图像生成请求
    format3 = {
        "model": model,
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
        "response_format": "image"  # 尝试指定响应格式
    }
    
    formats = [
        ("格式1: 直接请求", format1),
        ("格式2: 多模态请求", format2), 
        ("格式3: 指定图像格式", format3)
    ]
    
    for name, payload in formats:
        print(f"\n  🧪 {name}...")
        try:
            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"    ✅ 成功")
                
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    
                    # 检查响应内容
                    if isinstance(content, dict):
                        print(f"    🔍 返回字典格式，键: {list(content.keys())}")
                    elif isinstance(content, str):
                        if "图片" in content or "image" in content.lower():
                            print(f"    🖼️ 可能包含图像信息")
                        else:
                            print(f"    📝 返回文本描述")
                else:
                    print(f"    ⚠️ 响应格式异常")
            else:
                print(f"    ❌ 失败: {response.status_code}")
                
        except Exception as e:
            print(f"    ❌ 出错: {e}")

if __name__ == "__main__":
    research_doubao_image_generation()

