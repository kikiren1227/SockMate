#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试更新后的Stable Diffusion API
"""

import requests
import json

def test_final_stable_diffusion_api():
    """测试更新后的Stable Diffusion API"""
    
    # API配置
    api_key = "rPpxeWVde2EUlnw4HBK5ZLwD5RFJxxA97CqG3Ry8W6voEQNq5xQhqsfWeOMi"
    url = "https://modelslab.com/api/v6/images/text2img"
    
    headers = {
        "key": api_key,
        "Content-Type": "application/json"
    }
    
    # 测试袜子图片生成 - 使用袜子相关的提示词
    sock_prompt = "a beautiful cream white sock, elegant cuff design, soft terry fabric, delicate lace pattern, high quality product photo, e-commerce display, professional photography, clean white background, soft lighting, detailed texture, realistic, perfect composition"
    
    data = {
        "key": api_key,
        "prompt": sock_prompt,
        "model_id": "stable-diffusion-v1-5",  # 使用可用的免费模型
        "width": "1024",
        "height": "1024",
        "num_inference_steps": "20",  # 减少步数以加快生成速度
        "guidance_scale": "7.5"
    }
    
    print("🧪 最终测试更新后的Stable Diffusion API")
    print("=" * 70)
    print(f"📝 提示词: {sock_prompt}")
    print(f"🔗 API端点: {url}")
    print(f"🔑 API密钥: {api_key[:8]}...")
    print(f"🤖 模型: {data['model_id']}")
    print(f"📏 尺寸: {data['width']}x{data['height']}")
    print(f"🔄 推理步数: {data['num_inference_steps']}")
    
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
    image_url = test_final_stable_diffusion_api()
    
    if image_url:
        print(f"\n🎯 测试结果: 成功生成图片")
        print(f"🔗 图片链接: {image_url}")
        print(f"🌐 你可以在浏览器中打开这个链接查看生成的袜子图片!")
        print(f"🎉 现在你的袜子个性化设计系统应该可以生成真正的袜子图片了!")
    else:
        print(f"\n❌ 测试结果: 图片生成失败")
        print(f"💡 请检查API配置和网络连接")
