import os
import subprocess

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/open', methods=['GET'])
def open_file():
    file_path = request.args.get('path')
    if file_path and os.path.exists(file_path):
        # 简单的安全性检查，确保只打开特定类型的文件
        if file_path.endswith('.txt') or file_path.endswith('.pdf'):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(file_path)
                elif os.name == 'posix':  # macOS, Linux
                    subprocess.run(['open', file_path], check=True)
                return jsonify({"message": f"Opening {file_path}"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"error": "File type not allowed"}), 403
    else:
        return jsonify({"error": "File not found or path not provided"}), 404
