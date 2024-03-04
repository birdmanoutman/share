# routes.py
import os
import shutil

from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory, abort, flash
from werkzeug.utils import secure_filename

from preview_generator import generate_preview
from utils import allowed_file, custom_secure_filename, shorten_filename

bp = Blueprint('filehub', __name__)


def setup_routes(app):
    @bp.route('/')
    def index():
        directories = [d for d in os.listdir(current_app.config['ROOT']) if
                       os.path.isdir(os.path.join(current_app.config['ROOT'], d))]
        return render_template('index.html', directories=directories)

    @bp.route('/<folder_name>', methods=['GET', 'POST'])
    def upload_file(folder_name):
        folder_path = os.path.join(current_app.config['ROOT'], folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if request.method == 'POST':
            # Check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = custom_secure_filename(file.filename)
                file_path = os.path.join(folder_path, filename)
                file.save(file_path)
                generate_preview(file_path)  # Replace this with your preview generation logic

        files = os.listdir(folder_path)
        files_data = [{
            'name': f,
            'path': os.path.join(folder_name, f),
            'preview': generate_preview(os.path.join(folder_path, f)),
            # Assuming generate_preview returns a path to the preview image or None
        } for f in files if os.path.isfile(os.path.join(folder_path, f))]

        return render_template('upload.html', folder_name=folder_name, files_data=files_data,
                               shorten_filename=shorten_filename)

    @bp.route('/<folder_name>/<filename>')
    def download_file(folder_name, filename):
        # Security check - ensure filename is safe
        filename = secure_filename(filename)
        folder_path = os.path.join(current_app.config['ROOT'], folder_name)
        file_path = os.path.join(folder_path, filename)
        if not os.path.exists(file_path):
            abort(404)
        return send_from_directory(folder_path, filename)

    @bp.route('/<folder_name>/<filename>/delete', methods=['POST'])
    def delete_file(folder_name, filename):
        filename = secure_filename(filename)
        file_path = os.path.join(current_app.config['ROOT'], folder_name, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return redirect(url_for('filehub.upload_file', folder_name=folder_name))
        else:
            abort(404)

    @bp.route('/<folder_name>/<filename>/move', methods=['POST'])
    def move_file(folder_name, filename):
        # Get the destination folder from the form
        destination_folder = request.form.get('destination')
        if not destination_folder:
            abort(400, description="Destination folder not provided.")

        source = os.path.join(current_app.config['ROOT'], folder_name, secure_filename(filename))
        destination = os.path.join(current_app.config['ROOT'], destination_folder, secure_filename(filename))

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        shutil.move(source, destination)
        return redirect(url_for('filehub.upload_file', folder_name=destination_folder))

    @bp.route('/<folder_name>/<filename>/copy', methods=['POST'])
    def copy_file(folder_name, filename):
        # Get the destination folder from the form
        destination_folder = request.form.get('destination')
        if not destination_folder:
            abort(400, description="Destination folder not provided.")

        source = os.path.join(current_app.config['ROOT'], folder_name, secure_filename(filename))
        destination = os.path.join(current_app.config['ROOT'], destination_folder, secure_filename(filename))

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        shutil.copy(source, destination)
        return redirect(url_for('filehub.upload_file', folder_name=destination_folder))
