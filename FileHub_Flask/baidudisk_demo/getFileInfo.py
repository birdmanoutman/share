import json
from urllib.parse import quote

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Referer': 'https://pan.baidu.com/disk/home',
    # 可能需要添加更多头部信息
}

# 注意将access_token替换为您的实际访问令牌
access_token = "126.4932acbfe7bfad408c53ca046269160e.Yayu1Mr-z6nltVEpDq9rbCfLX9jDe90NrfFpn1p.Z6cljw"
# 将fsids替换为您想查询的文件的fsid列表，即使只查询一个文件，也需要使用列表格式
fsids = json.dumps([404988736663698])

url = f"http://pan.baidu.com/rest/2.0/xpan/multimedia?method=filemetas&access_token={access_token}&fsids={fsids}&thumb=1&dlink=1&extra=1&needmedia=1&detail=1"

# headers = {'User-Agent': 'pan.baidu.com'}

response = requests.get(url, headers=headers)

bduss_value = 'jhRSTFqUUVkeVgzOGxMflpneDk1cXh3SmVDOEd5QVpKbzY1RXRYN2k3SEUxRTFsSVFBQUFBJCQAAAAAAAAAAAEAAAAlHa8DYm01NDkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMRHJmXERyZlM'

cookies = {
    'BDUSS': bduss_value,
    # 添加其他必要的cookies
}
# 确保响应状态码为200，表示成功
if response.status_code == 200:
    response_data = response.json()  # 将响应内容解析为JSON格式（Python字典）

    # 从解析后的数据中提取dlink
    dlinks = [item['dlink'] for item in response_data.get('list', []) if 'dlink' in item]

    for dlink in dlinks:
        print(dlink)

    # 示例中只取第一个dlink用于下载
    if dlinks:
        dlink = dlinks[0]
        # 对dlink进行编码
        encoded_dlink = quote(dlink, safe=':/?&=%')

        # 文件将被保存在当前目录下，文件名由您指定
        save_path = "downloaded_file.pdf"

        # 发送GET请求下载文件
        download_response = requests.get(encoded_dlink, headers=headers, cookies=cookies, stream=True)

        if download_response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(download_response.content)
            print(f"文件已下载并保存到 {save_path}")
        else:
            print("下载失败，状态码：", download_response.status_code)

else:
    print("获取dlink失败，状态码：", response.status_code)
