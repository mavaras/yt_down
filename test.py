import sys
import os
from pathlib import Path, PureWindowsPath
from pytube import YouTube

from flask import Flask, current_app, render_template, request, send_file, redirect, url_for
app = Flask(__name__)


@app.route("/", methods = ["GET"])
def g_index():
    return render_template("index.html", flag="hidden")

@app.route("/", methods = ["POST"])
def p_index():
    try:
        link = request.form["link"]
        video = YouTube(link)
        ext = "mp4" if "mp4" in request.form or len(request.form) == 1 else "mp3"
        title, length = video.title, video.length
    
        video.streams.filter(file_extension=ext).first().download("\\tmp", filename="download")
        
        print("success")
    except:
        pass
    
    return render_template("index.html", link=link,
                                         title=title,
                                         length=length,
                                         ext=ext,
                                         flag="")

@app.route("/get_download/<ext>")
def get_download(ext):
    path = "\\tmp\\download."+ext
    def generate():
        with open(path, encoding="utf-8", errors="ignore") as f:
            yield from f

        os.remove(path)

    res = current_app.response_class(generate(), mimetype="video/"+ext)
    res.headers.set("Content-Disposition", "attachment", filename="download."+ext)
    return res

@app.route("/download", methods = ["GET", "POST"])
def download():
    if request.method == "POST":
        print(request.form["algo"])
        return render_template("download.html", algo = request.form["algo"])


if __name__ == "__main__":
    app.run()

