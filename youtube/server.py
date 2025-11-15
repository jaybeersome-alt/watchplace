from flask import Flask, request, redirect, render_template, send_from_directory, url_for
import os
import random
import string

app = Flask(__name__)
UPLOAD_FOLDER = "videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_random_string(length=11):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/")
def index():
    video_ids = [name for name in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))]
    
    # Read the title of each video
    videos = []
    for vid in video_ids:
        title_file = os.path.join(UPLOAD_FOLDER, vid, "title.txt")
        if os.path.exists(title_file):
            with open(title_file, "r", encoding="utf-8") as f:
                title = f.read()
        else:
            title = "Untitled"
        videos.append({"id": vid, "title": title})

    return render_template("index.html", videos=videos)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        video = request.files['video']
        thumbnail = request.files['thumbnail']
        title = request.form['title']

        video_id = generate_random_string()
        video_folder = os.path.join(UPLOAD_FOLDER, video_id)
        os.makedirs(video_folder)

        video.save(os.path.join(video_folder, "video.mp4"))
        thumbnail.save(os.path.join(video_folder, "thumbnail.jpg"))

        with open(os.path.join(video_folder, "title.txt"), "w", encoding="utf-8") as f:
            f.write(title)

        return redirect("/")
    return render_template("upload.html")

@app.route("/videos/<video_id>/<filename>")
def serve_video(video_id, filename):
    return send_from_directory(os.path.join(UPLOAD_FOLDER, video_id), filename)

@app.route("/watch/<video_id>")
def watch(video_id):
    video_folder = os.path.join(UPLOAD_FOLDER, video_id)
    if not os.path.exists(video_folder):
        return "Video not found", 404
    with open(os.path.join(video_folder, "title.txt"), "r", encoding="utf-8") as f:
        title = f.read()
    return render_template("video.html", video_id=video_id, title=title)

if __name__ == "__main__":
    app.run(debug=True)
