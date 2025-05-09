from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key_here'

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

ALLOWED_EXTENSIONS = {'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload():
    if 'video' not in request.files:
        return "No file part", 400
    video = request.files['video']
    if video.filename == '':
        return "No selected file", 400
    if video and allowed_file(video.filename):
        video.save('static/uploads/' + video.filename)
    return "invalid file type", 400
    


if __name__ == "__main__":
    app.run(debug=True)