#!/usr/bin/env python
import os
import shutil
from flask import Flask, render_template, request, \
    Response, send_file, redirect, url_for
from camera import Camera
from face_verify import FaceCognitive

app = Flask(__name__)
camera = None
stamp = 'Time'
picFolder = os.path.join('static', 'captures')

def get_camera():
    global camera
    if not camera:
        camera = Camera()

    return camera

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_feed()
        if frame:
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            raise RuntimeError("No frame captured.")

@app.route('/video_feed/')
def video_feed():
    camera = get_camera()
    return Response(gen(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture/')
def capture():
    global stamp
    camera = get_camera()
    stamp = camera.capture()
    return redirect(url_for('show_capture', timestamp=stamp))

@app.route('/identify', methods = ['GET', 'POST'])
def identify():
    fullPath = os.path.join(picFolder, stamp)
    myString = FaceCognitive().faceCompare(fullPath+'.jpg', 'testImages/yo1.JPG')
    return render_template('identify.html', myPath=fullPath+'.jpg', finalThing=myString)

def stamp_file(timestamp):
    return 'captures/' + timestamp +".jpg"

@app.route('/capture/image/<timestamp>', methods=['POST', 'GET'])
def show_capture(timestamp):
    path = stamp_file(timestamp)

    return render_template('capture.html',
        stamp=timestamp, path=path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)