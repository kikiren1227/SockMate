#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
袜子个性化设计系统
"""

import os
from flask import Flask, redirect, render_template, request, jsonify, url_for
from PIL import Image
import io
from core.analysis import DoubaoAnalyzer, SockMapper, AnalyzerParams, AnalysisResult, SockDesign
from core.generator.base import HFGenerator, BaseParams

app = Flask(__name__)

def analyze_user_photo(photo) -> AnalysisResult:
    """分析用户照片，提取四个维度的特征"""
    api_url = os.getenv("DOUBAO_API_URL")
    api_token = os.getenv("DOUBAO_API_TOKEN")
    
    analyzer = DoubaoAnalyzer(
        api_token=api_token,
        api_url=api_url
    )
    params = AnalyzerParams(
        image=photo,
        api_token=api_token,
        api_url=api_url
    )
    return analyzer.analyze(params)

@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        return upload_file()
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    photo = request.files['photo']
    if photo.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # 分析用户照片
        user_tags = analyze_user_photo(photo)
        if not user_tags:
            return jsonify({'error': 'Failed to analyze photo'}), 500
        
        # 映射到袜子设计
        sock_design = SockMapper.map_user_to_socks(user_tags)
        
        # 生成袜子图片
        generator = HFGenerator(
            api_token=os.getenv("HF_API_TOKEN"),
            url=os.getenv("HF_API_URL")
        )
        
        # 构建提示词
        prompt = f"a single beautiful {sock_design['colors']} sock, {sock_design['shape']}, {sock_design['material']}, {sock_design['pattern']}, cartoon style, kawaii design, cute illustration, clean white background, high quality, only one sock, no multiple socks, single item focus"
        
        params = BaseParams.create(
            prompt=prompt,
            width=512,
            height=512
        )
        
        image_data = generator.generate(params)
        if not image_data:
            return jsonify({'error': 'Failed to generate image'}), 500
        
        # 保存图片
        image_path = f"static/generated/sock_{hash(str(sock_design)) % 10000}.jpg"
        with open(image_path, 'wb') as f:
            f.write(image_data)
        
        return redirect(url_for('result_page',
                                image_path=image_path,
                                design=str(sock_design),
                                user_tags=str(user_tags)))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/result')
def result_page():
    image_path = request.args.get('image_path')
    design = request.args.get('design')
    user_tags = request.args.get('user_tags')
    
    return render_template('result.html', 
                         image_path=image_path, 
                         design=design, 
                         user_tags=user_tags)

if __name__ == '__main__':
    app.run(debug=True)
