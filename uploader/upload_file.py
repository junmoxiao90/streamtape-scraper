import os
import requests
import json
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
from uploader.get_ul_url import *

console = Console()

# 输入文件夹路径
folder_path = input("Enter Folder Path: ")

# 获取文件夹下所有的 flv 文件
flv_files = [f for f in os.listdir(folder_path) if f.endswith(".flv")]

if not flv_files:
    console.print("No FLV files found in the specified folder.", style="bold red")
else:
    console.print(f"Uploading {len(flv_files)} FLV files...", style="bold red")

    def upload_file(flv_file):
        file_path = os.path.join(folder_path, flv_file)
        console.print(f"Uploading {flv_file}...", style="bold yellow")

        files = {'file': (flv_file, open(file_path, 'rb'), 'multipart/form-data')}
        session = requests.Session()

        def ul_video(ul_url):
            headers = {"login": login_id, "key": key_id}
            try:
                response = session.post(ul_url, files=files, headers=headers)
                data = json.loads(response.text)
                url = data.get('result').get('url')
                console.print(f"Uploaded {flv_file} Successfully", style="bold green")
                console.print(f"Download link for {flv_file}: {url}")

                # 保存下载链接到文件
                save_path = '/home/junmoxiao/download_links.txt'
                with open(save_path, 'a') as save_file:
                    save_file.write(f"{flv_file}: {url}\n")

            except Exception as e:
                console.print(f"Error uploading {flv_file}: {str(e)}")

        ul_video(ul_url)

    # 使用 ThreadPoolExecutor 同时上传多个文件
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_file, flv_files)
