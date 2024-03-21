""""修改注册表后，利用这个脚本就能在浏览器中打开本地文件"""
import subprocess
import sys
import urllib.parse


def open_file(url):
    # 剔除URL协议头 (如果存在)
    if url.startswith("myapp://"):
        url = url[len("myapp://"):]  # 移除协议部分
    # 解码URL编码的路径
    file_path = urllib.parse.unquote(url)
    # Windows路径替换为正确的格式
    file_path = file_path.replace("/", "\\")
    # 使用默认程序打开文件
    subprocess.run(f'start "" "{file_path}"', shell=True, check=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        open_file(url)
    else:
        print("No URL provided.")
