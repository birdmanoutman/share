import time

import requests


# 第一步：获取设备码和用户码
def get_device_code(client_id):
    url = "https://openapi.baidu.com/oauth/2.0/device/code"
    params = {
        'response_type': 'device_code',
        'client_id': client_id,
        'scope': 'basic,netdisk'
    }
    headers = {
        'User-Agent': 'pan.baidu.com'
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()  # 返回响应的JSON数据


# 第二步：用户使用设备码完成授权
def instruct_user_to_authorize(verification_url, user_code):
    print(f"请访问 {verification_url} 并输入用户码: {user_code} 进行授权。")
    print("授权完成后，请按回车继续...")
    input()  # 等待用户按回车确认


# 第三步：轮询获取访问令牌
def poll_for_access_token(client_id, client_secret, device_code):
    url = "https://openapi.baidu.com/oauth/2.0/token"
    params = {
        'grant_type': 'device_token',
        'code': device_code,
        'client_id': client_id,
        'client_secret': client_secret
    }
    poll_interval = 5  # 轮询间隔通常由服务提供商在响应中指定
    timeout = time.time() + 10 * 60  # 设定一个超时时间，例如10分钟

    while time.time() < timeout:
        response = requests.post(url, data=params)
        json_data = response.json()
        if response.status_code == 200 and 'access_token' in json_data:
            return json_data['access_token']  # 返回访问令牌
        elif json_data.get('error') == 'authorization_pending':
            print("等待用户授权...")
            time.sleep(poll_interval)
        else:
            print("错误:", json_data)
            break
    return None


# 主程序
def main():
    client_id = ''
    client_secret = ''

    # 获取设备码和用户码
    device_code_data = get_device_code(client_id)
    device_code = device_code_data.get('device_code')
    user_code = device_code_data.get('user_code')
    verification_url = device_code_data.get('verification_url', 'https://openapi.baidu.com/device')

    # 指导用户授权
    instruct_user_to_authorize(verification_url, user_code)

    # 轮询获取访问令牌
    access_token = poll_for_access_token(client_id, client_secret, device_code)
    if access_token:
        print("访问令牌获取成功:", access_token)
    else:
        print("获取访问令牌失败。")


if __name__ == "__main__":
    main()
