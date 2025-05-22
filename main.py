from flask import Flask, render_template, request, Response
import cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key_here'
camera = cv2.VideoCapture(0)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

ALLOWED_EXTENSIONS = {'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generateFrames():
    while True:
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    

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

@app.route("/video")
def video():
    return Response(generateFrames(), mimetype="multipart/x-mixed-replace; boundary=frame")
    


if __name__ == "__main__":
    app.run(debug=True)