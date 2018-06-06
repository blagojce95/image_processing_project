from flask import Flask, render_template, request, redirect, jsonify
from nocache import nocache
from flask_bootstrap import Bootstrap
import os
import time

from app import compare

app = Flask(__name__)
Bootstrap(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
@nocache
def upload():
    target = os.path.join(APP_ROOT, 'static/')
    print(target)

    if request.method == "POST":
        timestamp = int(time.time())
        name_finger1 = str(timestamp) + "_finger1.jpg"
        name_finger2 = str(timestamp) + "_finger2.jpg"
        location_finger1 = os.path.join(target, name_finger1)
        location_finger2 = os.path.join(target, name_finger2)

        finger1 = request.files["fingerOneToUpload"]
        finger1.save(location_finger1)

        finger2 = request.files["fingerTwoToUpload"]
        finger2.save(location_finger2)

        score, result1, result2 = compare(location_finger1, location_finger2, target, timestamp)
        print score
        print result1
        print result2

        return render_template("upload.html", name_finger1=result1, name_finger2=result2, score=score)

    return render_template("error.html")


if __name__ == '__main__':
    app.run()
