import re


def custom_secure_filename(filename):
    # 移除非法字符，但允许中文和其他非ASCII字符
    filename = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5_.-]', '', filename)
    return filename


def shorten_filename(filename, max_length=16):
    """如果文件名大于max_length个字符，只显示前max_length个字符"""
    if len(filename) > max_length:
        return f"{filename[:max_length]}..."
    return filename
