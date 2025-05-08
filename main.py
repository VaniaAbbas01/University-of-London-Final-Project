from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/name")
def hello_name():
    return "<p>Hello, Name!</p>"

if __name__ == "__main__":
    app.run(debug=True)