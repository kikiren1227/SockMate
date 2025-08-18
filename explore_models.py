#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
探索可用的免费模型
"""

import requests
import json

def explore_available_models():
    """探索可用的免费模型"""
    
    # API配置
    api_key = "rPpxeWVde2EUlnw4HBK5ZLwD5RFJxxA97CqG3Ry8W6voEQNq5xQhqsfWeOMi"
    url = "https://modelslab.com/api/v6/images/text2img"
    
    headers = {
        "key": api_key,
        "Content-Type": "application/json"
    }
    
    print("🔍 探索可用的免费模型")
    print("=" * 50)
    
    # 测试一些常见的模型ID
    models_to_test = [
        "stable-diffusion-v1-5",
        "stable-diffusion-v2-1",
        "stable-diffusion-xl",
        "realistic-vision-v5",
        "dream-shaper-v8",
        "deliberate-v3",
        "openjourney-v4",
        "anything-v5",
        "counterfeit-v3",
        "realistic-vision-v4",
        "dreamlike-photoreal-v2",
        "vintedois-diffusion-v0-4",
        "realistic-vision-v3",
        "dreamlike-diffusion-v1",
        "stable-diffusion-v1-4"
    ]
    
    working_models = []
    
    for model in models_to_test:
        print(f"\n🧪 测试模型: {model}")
        
        data = {
            "key": api_key,
            "prompt": "a simple red sock, high quality",
            "model_id": model,
            "width": "512",
            "height": "512",
            "num_inference_steps": "20",
            "guidance_scale": "7.5"
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'status' in result and result['status'] == 'error':
                    if 'Model not found' in str(result):
                        print(f"  ❌ 模型不存在: {model}")
                    else:
                        print(f"  ⚠️ 模型存在但其他错误: {result.get('message', 'Unknown error')}")
                else:
                    print(f"  ✅ 模型可用: {model}")
                    working_models.append(model)
            else:
                print(f"  ❌ HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ 测试出错: {e}")
    
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    
    if working_models:
        print(f"✅ 可用的模型 ({len(working_models)}个):")
        for model in working_models:
            print(f"  - {model}")
    else:
        print("❌ 没有找到可用的免费模型")
        print("💡 建议:")
        print("  1. 检查API密钥是否有效")
        print("  2. 查看API文档获取正确的模型列表")
        print("  3. 考虑使用其他免费的图像生成服务")
    
    return working_models

if __name__ == "__main__":
    working_models = explore_available_models()
