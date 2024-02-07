# utils.py
import os
import re
import shutil


def custom_secure_filename(filename):
    # 移除非法字符，但允许中文和其他非ASCII字符
    filename = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5_.-]', '', filename)
    return filename


def shorten_filename(filename, max_length=16):
    """如果文件名大于max_length个字符，只显示前max_length个字符"""
    if len(filename) > max_length:
        return f"{filename[:max_length]}..."
    return filename


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def file_operation(operation, file_path, destination_path=None):
    """
    Perform a file operation like move or delete.

    :param operation: The operation to perform ('move' or 'delete').
    :param file_path: The path to the file to operate on.
    :param destination_path: The new path for the file if the operation is 'move'.
    """
    try:
        if operation == 'delete':
            # Ensure the file exists before attempting to delete
            if os.path.isfile(file_path):
                os.remove(file_path)
                return {'status': 'success', 'message': f'File {file_path} deleted successfully.'}
            else:
                return {'status': 'error', 'message': f'File {file_path} not found.'}

        elif operation == 'move':
            # Ensure the file exists and the destination is valid before attempting to move
            if os.path.isfile(file_path) and destination_path is not None:
                # Create the destination directory if it doesn't exist
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.move(file_path, destination_path)
                return {'status': 'success', 'message': f'File moved to {destination_path} successfully.'}
            else:
                return {'status': 'error', 'message': 'Invalid file or destination.'}

    except OSError as e:
        return {'status': 'error', 'message': str(e)}
