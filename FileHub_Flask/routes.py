import os

from flask import render_template, send_from_directory, request, redirect, url_for
from werkzeug.exceptions import InternalServerError

from preview_generator import get_pdf_preview, get_doc_preview, pptx_to_jpg
from utils import custom_secure_filename, shorten_filename


def setup_routes(app):
    @app.route('/')
    def index():
        directories = [d for d in os.listdir(app.config['ROOT']) if os.path.isdir(os.path.join(app.config['ROOT'], d))]
        return render_template('index.html', directories=directories)

    @app.route('/<folder_name>', methods=['GET', 'POST'])
    def upload_file(folder_name):
        folder_path = os.path.join(app.config['ROOT'], folder_name)
        previews = {}
        if request.method == 'POST':
            file = request.files.get('file')
            if file and file.filename:
                filename = custom_secure_filename(file.filename)
                file_save_path = os.path.join(folder_path, filename)
                file.save(file_save_path)

                try:
                    # 生成文件预览并存储路径
                    if filename.lower().endswith('.pdf'):
                        previews[filename] = get_pdf_preview(file_save_path)
                    elif filename.lower().endswith('.docx'):
                        previews[filename] = get_doc_preview(file_save_path)
                    elif filename.lower().endswith('.pptx'):
                        previews[filename] = pptx_to_jpg(file_save_path, folder_path)
                except Exception as e:
                    app.logger.error(f"Error generating preview for {filename}: {e}")
                    raise InternalServerError(f"Error generating preview for {filename}.")

                return redirect(url_for('upload_file', folder_name=folder_name))
        files = os.listdir(folder_path)
        # 将预览文件路径传递给前端模板
        return render_template('upload.html', folder_name=folder_name, files=files, previews=previews,
                               shorten_filename=shorten_filename)

    @app.route('/<folder_name>/<filename>')
    def download_file(folder_name, filename):
        folder_path = os.path.join(app.config['ROOT'], folder_name)
        return send_from_directory(folder_path, filename)
