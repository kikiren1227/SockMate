#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试豆包API的图像生成功能
"""

import requests
import json

def test_image_generation():
    """测试豆包API的图像生成功能"""
    
    # API配置
    api_token = "cacfd50c-e415-4e69-941b-e22b32705c27"
    base_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    # 请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    # 测试不同的图像生成提示词
    test_prompts = [
        "一双红色袜子，精致收口型，柔软毛圈面料，精致蕾丝图案，高质量产品图",
        "sock, red color, elegant design, high quality product photo",
        "袜子 红色 精致 高质量 产品图"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🧪 测试 {i}: {prompt}")
        print("=" * 60)
        
        payload = {
            "model": "doubao-seed-1-6-250615",
            "messages": [
                {
                    "content": [
                        {
                            "text": prompt,
                            "type": "text"
                        }
                    ],
                    "role": "user"
                }
            ]
        }
        
        try:
            print("🚀 发送请求...")
            response = requests.post(
                base_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            
            print(f"📊 响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 请求成功!")
                
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    print(f"📝 返回内容类型: {type(content)}")
                    print(f"📝 返回内容: {content[:200]}...")
                    
                    # 检查是否包含图像数据
                    if isinstance(content, dict):
                        print("🔍 返回的是字典格式")
                        if 'image_url' in content:
                            print("✅ 找到image_url字段")
                        if 'image' in content:
                            print("✅ 找到image字段")
                    elif isinstance(content, str):
                        print("🔍 返回的是字符串格式")
                        if content.startswith('data:image'):
                            print("✅ 找到base64图像数据")
                        else:
                            print("⚠️ 返回的是文本描述")
                else:
                    print("❌ 响应中没有choices")
            else:
                print(f"❌ 请求失败: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ 测试出错: {e}")
        
        print("-" * 60)

if __name__ == "__main__":
    test_image_generation()

