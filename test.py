import sys
import os
from pathlib import Path, PureWindowsPath
from pytube import YouTube
import moviepy.editor as mp

from flask import Flask, current_app, render_template, request, send_file, redirect, url_for
app = Flask(__name__)
def page_not_found_404(e): return render_template("error.html"), 404
def page_not_found_500(e): return render_template("error.html"), 500
app.register_error_handler(404, page_not_found_404)
app.register_error_handler(500, page_not_found_500)

@app.route("/", methods = ["GET"])
def g_index():
    return render_template("index.html", flag="hidden")

@app.route("/", methods = ["POST"])
def p_index():
    print(request.form)
    
    link = request.form["link"]
    video = YouTube(link)
    ext = "mp4" if "mp4" in request.form or len(request.form) == 1 else "mp3"
    title, length = video.title, video.length

    video.streams.filter(file_extension="mp4").first().download("/tmp", filename="download")  # os.getcwd()+"\\temp_downloads"

    if ext == "mp3":
        clip = mp.VideoFileClip("/tmp/download.mp4")
        clip.audio.write_audiofile("/tmp/download.mp3")

    print("success")
    
    return render_template("index.html", link=link,
                                         title=title,
                                         length=length,
                                         ext=ext,
                                         flag="")

@app.route("/get_download/<ext>")
def get_download(ext):
    return send_file("/tmp/download."+ext, as_attachment=True)
    '''path = Path(PureWindowsPath(os.getcwd()+"\\temp_downloads\\download."+ext))
    def generate():
        with open(path, encoding="utf-8", errors="ignore") as f:
            yield from f

        os.remove(path)

    res = current_app.response_class(generate(), mimetype="video/"+ext)
    res.headers.set("Content-Disposition", "attachment", filename="download."+ext)
    return res'''


if __name__ == "__main__":
    app.run()

