import os
import re
from io import BytesIO

import comtypes.client
import docx
import fitz  # PyMuPDF
from PIL import Image
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)
ROOT_FOLDER = './'
app.config['UPLOAD_FOLDER'] = ROOT_FOLDER


def get_pdf_preview(pdf_path):
    # 打开PDF文件，提取第一页作为图像
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)  # 第一页
    pix = page.get_pixmap()
    img = Image.open(BytesIO(pix.tobytes()))
    preview_path = pdf_path + "_preview.png"
    img.save(preview_path)
    return preview_path


def get_doc_preview(doc_path):
    # 打开DOC文件，提取前50个字
    doc = docx.Document(doc_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
        if len(' '.join(text)) > 50:
            break
    return ' '.join(text)[:50]


def pptx_to_jpg(pptx_path, output_folder):
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    deck = powerpoint.Presentations.Open(pptx_path)
    deck.Slides[0].Export(os.path.join(output_folder, "slide1.jpg"), "JPG")
    deck.Close()
    powerpoint.Quit()


@app.route('/')
def index():
    directories = [d for d in os.listdir(ROOT_FOLDER) if os.path.isdir(os.path.join(ROOT_FOLDER, d))]
    return render_template_string('''
        <html>
            <head><title>文件共享服务</title></head>
            <body>
                <h1>选择上传目录</h1>
                {% for folder in directories %}
                    <li><a href="{{ url_for('upload_file', folder_name=folder) }}">{{ folder }}</a></li>
                {% endfor %}
            </body>
        </html>
    ''', directories=directories)


def custom_secure_filename(filename):
    # 移除非法字符，但允许中文和其他非ASCII字符
    filename = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5_.-]', '', filename)
    return filename


def shorten_filename(filename, max_length=16):
    """如果文件名大于max_length个字符，只显示前max_length个字符"""
    if len(filename) > max_length:
        return f"{filename[:max_length]}..."
    return filename


@app.route('/upload/<folder_name>', methods=['GET', 'POST'])
def upload_file(folder_name):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_save_path = os.path.join(folder_path, filename)
            file.save(file_save_path)

            # 根据文件类型生成预览
            if filename.lower().endswith('.pdf'):
                get_pdf_preview(file_save_path)
            elif filename.lower().endswith('.docx'):
                get_doc_preview(file_save_path)
            elif filename.lower().endswith('.pptx'):
                pptx_to_jpg(file_save_path, folder_path)

            return redirect(url_for('upload_file', folder_name=folder_name))
    files = os.listdir(folder_path)
    return render_template_string('''
        <!doctype html>
        <title>文件上传</title>
        <head>
            <style>
                .gallery {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    align-items: center;
                    justify-content: center;
                }
                .gallery div {
                    width: 100px; /* 匹配图片和文件名宽度 */
                }
                .gallery img {
                    width: 100%; /* 图片宽度自适应 */
                    height: 100px; /* 固定图片高度 */
                    object-fit: cover;
                }
                .file-name {
                    text-align: center;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }
            </style>
        </head>
        <body>
            <h1>上传文件到 "{{ folder_name }}"</h1>
            <form method=post enctype=multipart/form-data>
              选择文件: <input type=file name=file>
              <input type=submit value=上传>
            </form>
            <div class="gallery">
                {% for file in files %}
                    <div>
                        <a href="{{ url_for('download_file', folder_name=folder_name, filename=file) }}">
                            {% if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) %}
                                <img src="{{ url_for('download_file', folder_name=folder_name, filename=file) }}" alt="{{ file }}">
                            {% endif %}
                            <div class="file-name">{{ shorten_filename(file) }}</div>
                        </a>
                    </div>
                {% endfor %}
            </div>
            <a href="{{ url_for('index') }}">返回</a>
        </body>
    ''', folder_name=folder_name, files=files, shorten_filename=shorten_filename)


@app.route('/files/<folder_name>/<filename>')
def download_file(folder_name, filename):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    return send_from_directory(folder_path, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7861)
