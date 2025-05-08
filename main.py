from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key_here'

class uploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Submit")

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    form = uploadFileForm()
    return render_template("index.html", form=form)

@app.route("/name")
def hello_name():

    return "<p>Hello, Name!</p>"

if __name__ == "__main__":
    app.run(debug=True)