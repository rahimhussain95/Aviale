import datetime

from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/status")
def status():
    return render_template("status.html");

if __name__ == "__main__":
    app.run(debug=True)