import asyncio
import logging

import aiohttp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


async def sync_file_to_notion(session, api_key, database_id, file_info):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
    }
    data = {
        # 根据Notion API要求构造数据
    }
    async with session.post(url, json=data, headers=headers) as response:
        if response.status == 200:
            logging.info(f"Successfully synced {file_info['name']} to Notion.")
        else:
            logging.error(f"Failed to sync {file_info['name']}. Status: {response.status}")


async def main(api_key, database_id, directory):
    files_info = scan_local_directory(directory)  # 假设这是扫描目录的函数
    async with aiohttp.ClientSession() as session:
        tasks = [sync_file_to_notion(session, api_key, database_id, file_info) for file_info in files_info]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    # 这里可以解析命令行参数或读取配置文件
    api_key = "your_api_key"
    database_id = "your_database_id"
    directory = "/path/to/your/directory"
    asyncio.run(main(api_key, database_id, directory))
