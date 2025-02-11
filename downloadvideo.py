from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from yt_dlp import YoutubeDL
import os
import threading

# 打包方法：cd 进入你的文件路径，然后执行：pyinstaller --onefile downloadvideo.py

app = Flask(__name__)
CORS(app)  # 允许跨域请求

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

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
            "format": "bestvideo+bestaudio",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, f"{videoId}.%(ext)s"),
            "progress_hooks": [progress_hook],
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }],
        }) as ydl:
            ydl.download([url])

    thread = threading.Thread(target=run_download)
    thread.start()

    return jsonify({"error": 0, "msg": "处理开始", "videoId": videoId})


@app.route("/api/tasks/getprogress/<string:videoId>", methods=["GET"])
def getprogress(videoId):
    """ 获取下载进度 """
    return jsonify(progress_data.get(videoId, {"status": "not started"}))


@app.route("/api/tasks/checkfile/<string:videoId>", methods=["GET"])
def checkfile(videoId):
    """ 检查文件是否存在 """
    filepath = os.path.join(DOWNLOAD_FOLDER, f"{videoId}.mp4")  # ✅ 确保检查的是最终 mp4 文件
    if os.path.exists(filepath):
        return jsonify({"error": 0, "msg": "文件已存在", "videoId": videoId})
    return jsonify({"error": 1, "msg": "文件未找到"}), 404


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
