import requests
import json

# 定义请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Referer': 'https://pan.baidu.com/disk/home',
}

# 设置访问令牌和文件fsid列表
access_token = "您的实际访问令牌"
fsids = json.dumps([您的文件fsid])

# 构造API URL
url = f"http://pan.baidu.com/rest/2.0/xpan/multimedia?method=filemetas&access_token={access_token}&fsids={fsids}&thumb=1&dlink=1&extra=1&needmedia=1&detail=1"

# 发起GET请求
response = requests.get(url, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    response_data = response.json()  # 解析响应内容为字典

    # 提取dlink
    dlinks = [item['dlink'] for item in response_data.get('list', []) if 'dlink' in item]

    # 遍历所有dlink（这里只处理第一个）
    if dlinks:
        dlink = dlinks[0]

        # 设置文件保存路径
        save_path = "downloaded_file.pdf"

        # 使用Cookies（如果需要）
        cookies = {'BDUSS': '您的BDUSS值'}

        # 发起下载请求
        download_response = requests.get(dlink, headers=headers, cookies=cookies, stream=True)

        # 保存文件
        if download_response.status_code == 200:
            with open(save_path, "wb") as file:
                for chunk in download_response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print(f"文件已下载并保存到 {save_path}")
        else:
            print("下载失败，状态码：", download_response.status_code)
else:
    print("获取dlink失败，状态码：", response.status_code)
