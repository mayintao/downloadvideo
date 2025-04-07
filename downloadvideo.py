import tempfile

from flask import Flask, jsonify, Response
from flask_cors import CORS
from yt_dlp import YoutubeDL
import os
import threading

# 打包方法：python控制台执行：pyinstaller --onefile downloadvideo.py
# 将 cookies 从 cookies.txt 文件转换为字典
cookies = [
    {'domain': '.youtube.com', 'name': 'PREF', 'value': 'f4=4000000&tz=Asia.Kuching&f7=100', 'path': '/',
     'secure': True},
    {'domain': '.youtube.com', 'name': 'LOGIN_INFO',
     'value': 'AFmmF2swRgIhAPe3vlaX_xLpdhRBWqbsCSIuABBH7ZpZ5ioNnhVD1HLbAiEAtFTz-ZbJtEgWtWYi61jYp_N1RwW3Fz-r_Vffrt4Ev9w:QUQ3MjNmeG15dldIbFVJSmxVYW5VVlNLY2tXTDB4dVEtVm1VSVpoUmtVM2xnb2xYamdiMm9zYk5DbTdHYTV6RmpqN0ZXOWJ2SVNDa0FPLUpxMTRCelRFRmlqT21RU0IxejFjVzgzOWZvSDZTRUJ3LUNoUUJhc3lfaGhHVVFGbVFiRUQ4VU9uZUZQbWl6OWVuX3pOM3BBSW11c0w1anJaMWhR',
     'path': '/', 'secure': True},
    {'domain': '.youtube.com', 'name': 'HSID', 'value': 'A2UHsB2VvTBKuydkC', 'path': '/', 'secure': True},
    {'domain': '.youtube.com', 'name': 'SSID', 'value': 'AYO2XywiGjw0NCCCa', 'path': '/', 'secure': True},
    {'domain': '.youtube.com', 'name': 'APISID', 'value': 'R53cYDewGpvp9DER/A7zCawVZhpLVRrLQJ', 'path': '/',
     'secure': True},
    {'domain': '.youtube.com', 'name': 'SAPISID', 'value': 'ewahBVrU0SobzUxU/ArECdcd693pAWRDO6', 'path': '/',
     'secure': True},
    {'domain': '.youtube.com', 'name': '__Secure-1PAPISID', 'value': 'ewahBVrU0SobzUxU/ArECdcd693pAWRDO6', 'path': '/',
     'secure': True},
    {'domain': '.youtube.com', 'name': '__Secure-3PAPISID', 'value': 'ewahBVrU0SobzUxU/ArECdcd693pAWRDO6', 'path': '/',
     'secure': True},
    {'domain': '.youtube.com', 'name': 'SID',
     'value': 'g.a000vQhaIfpdKR9JP3scvueHOe7N-ydyNfPkeqJ-aIJti6soFu0Oo7aq5_QDfZqsips0mLAhHgACgYKAUsSAQASFQHGX2Mi-S5Pz2C1CcNGetp6gI5XqhoVAUF8yKr5CZnaFp4ghh81SsFTrR2T0076',
     'path': '/', 'secure': False},
    {'domain': '.youtube.com', 'name': '__Secure-1PSID',
     'value': 'g.a000vQhaIfpdKR9JP3scvueHOe7N-ydyNfPkeqJ-aIJti6soFu0OltdO77mYoAcLAeHuGV-pvwACgYKAccSAQASFQHGX2MiQ4KApxvAVxpejulQoRAx2BoVAUF8yKo_i1VXuiLtBoKNRrJQFhY90076',
     'path': '/', 'secure': True},
    {'domain': '.youtube.com', 'name': '__Secure-3PSID',
     'value': 'g.a000vQhaIfpdKR9JP3scvueHOe7N-ydyNfPkeqJ-aIJti6soFu0OtgpKWGgpDu6E_Rp7L_sKbgACgYKAagSAQASFQHGX2MidvbaOvgmBk9Gd7idnoS3TRoVAUF8yKq8jEQDxA0MX4tkSjv80Ooo0076',
     'path': '/', 'secure': True},
    {'domain': '.youtube.com', 'name': '__Secure-1PSIDTS',
     'value': 'sidts-CjEB7pHptXy00S70BSIXqUaewWv6tVpUvrnosixpL8mEeIYlfG-3ezDVPLt8tWIHqhFNEAA', 'path': '/',
     'secure': True},
    {'domain': '.youtube.com', 'name': '__Secure-3PSIDTS',
     'value': 'sidts-CjEB7pHptXy00S70BSIXqUaewWv6tVpUvrnosixpL8mEeIYlfG-3ezDVPLt8tWIHqhFNEAA', 'path': '/',
     'secure': True},
    {'domain': '.youtube.com', 'name': 'SIDCC',
     'value': 'AKEyXzU6bKKIcc2L3oWm_EfopipAmh-ChHF5jM0fwdb3BDSpqoOjlZMw4PmE4g6mOcRJo6MB30g', 'path': '/',
     'secure': False},
    {'domain': '.youtube.com', 'name': '__Secure-1PSIDCC',
     'value': 'AKEyXzW9gh3H2Mf4chRNGLHSsMgiGER4PEH44lSdZaFVDSkOLq0xA3QFRhAVvGvY8Ci9CjSMUnQ', 'path': '/',
     'secure': True},
    {'domain': '.youtube.com', 'name': '__Secure-3PSIDCC',
     'value': 'AKEyXzWqfi9dgt7e3P0qPvbfE_zaAYBdS7oFpEX-OYxHV_TPd4f8s_Bw35Afcsui8pDMaxaQjQg', 'path': '/',
     'secure': True},
]

# 创建临时文件来存储 cookies
with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_cookie_file:
    temp_cookie_file.write("# Netscape HTTP Cookie File\n")
    temp_cookie_file.write("# This is a generated file! Do not edit.\n")
    for cookie in cookies:
        # 格式化为 Netscape cookie 格式
        temp_cookie_file.write(
            f"{cookie['domain']}\tTRUE\t{cookie['path']}\tTRUE\t{cookie['name']}\t{cookie['value']}\n")
    temp_cookie_file_path = temp_cookie_file.name

app = Flask(__name__)
CORS(app)  # 允许跨域请求

DOWNLOAD_FOLDER = "~/Downloads"

progress_data = {}


def progress_hook(d):
    """ 监听下载进度 """
    video_id = d.get("info_dict", {}).get("id", "unknown")

    if d['status'] == 'downloading':
        progress_data[video_id] = {
            "status": "downloading",
            "downloaded": d.get("downloaded_bytes", 0),
            "total": d.get("total_bytes", 1)
        }

    elif d['status'] == 'finished':
        # ✅ 改成最终的 mp4 文件路径
        correct_filepath = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.mp4")
        progress_data[video_id] = {
            "status": "completed",
            "filepath": correct_filepath  # 这里强制改成最终的文件名
        }


# http://127.0.0.1:5000/api/tasks/checkfile/Iz9Gr1ATrDo
@app.route("/api/tasks/checkfile/<string:videoId>", methods=["GET"])
def checkfile(videoId):
    """ 检查文件是否存在 """
    filepath = os.path.join(DOWNLOAD_FOLDER, f"{videoId}.mp4")  # ✅ 确保检查的是最终 mp4 文件
    if os.path.exists(filepath):
        return jsonify({"error": 0, "msg": "文件已存在", "videoId": videoId})
    return jsonify({"error": 1, "msg": "文件未找到"}), 404


# http://127.0.0.1:5000/api/tasks/downloadvideobyytnew/Iz9Gr1ATrDo
@app.route("/api/tasks/downloadvideobyytnew/<string:videoId>", methods=["GET"])
def downloadvideobyytnew(videoId):
    """ 启动后台线程下载视频 """
    url = f"https://youtube.com/watch?v={videoId}"
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{videoId}.mp4")

    # ✅ 下载前清除进度缓存，防止前端获取旧数据
    if videoId in progress_data:
        del progress_data[videoId]

    if os.path.exists(output_path):
        return jsonify({"error": 0, "msg": "文件已存在，直接提供下载链接", "videoId": videoId})

    def run_download():

        with YoutubeDL({
            "cookiefile": temp_cookie_file_path,  # 使用临时 cookie 文件=
            "format": "bestvideo+bestaudio",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, f"{videoId}.%(ext)s"),
            "progress_hooks": [progress_hook],
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }],
            "extractor-args": "youtube:player_client=android"
        }) as ydl:
            ydl.download([url])

    thread = threading.Thread(target=run_download)
    thread.start()

    return jsonify({"error": 0, "msg": "处理开始", "videoId": videoId})


@app.route("/api/tasks/getprogress/<string:videoId>", methods=["GET"])
def getprogress(videoId):
    """ 获取下载进度 """
    return jsonify(progress_data.get(videoId, {"status": "not started"}))


@app.route("/api/tasks/downloadfile/<string:videoId>", methods=["GET"])
def downloadfile(videoId):
    """ 提供文件下载并在成功后删除 """
    print(videoId)
    filepath = os.path.join(DOWNLOAD_FOLDER, f"{videoId}.mp4")
    print(filepath)

    if not os.path.exists(filepath):
        return jsonify({"error": 1, "msg": "文件未找到"}), 404

    def generate():
        with open(filepath, "rb") as f:
            yield from f

    response = Response(generate(), mimetype="video/mp4", headers={
        "Content-Disposition": f"attachment; filename={videoId}.mp4"
    })

    @response.call_on_close
    def cleanup():
        """ 当下载连接关闭后删除文件，并清除进度数据 """
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"✅ 文件 {filepath} 已删除")

        # ✅ 下载完成后清理 progress_data，防止前端查询到旧的已完成状态
        if videoId in progress_data:
            del progress_data[videoId]

    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 从环境变量读取端口，默认为 5000
    app.run(host="0.0.0.0", port=port, debug=True)
