import eventlet
# eventlet.monkey_patch()
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, send_from_directory,Response
from flask_socketio import SocketIO,emit,send
from datetime import date
<<<<<<< HEAD
from passlib.hash import pbkdf2_sha256
#import pyrebase
=======
>>>>>>> 4a27070795eea0b32cde1a8b5273ae0c67fe2a6b
import re
import natsort
from operator import itemgetter
from pyfcm import FCMNotification
from configGUI import *
from datetime import date
from datetime import datetime
<<<<<<< HEAD
# from firebase_admin import firebase_admin.messaging
#from firebaseconfig import db
from markPointsVid import  captureFrame,get_mouse_points
# from lineCrossFinal_resnet_roi_copy1 import lineCross
# from lineCrossFinal_resnet_roi_test import lineCross
# from deepstream_test_3 import run_crowdcount
=======
from markPointsVid import  captureFrame
from flask_sqlalchemy import SQLAlchemy
from VideoCamera import VideoCamera
from mypusher import pusher_client
basedir = os.path.abspath(os.path.dirname(__file__))
>>>>>>> 4a27070795eea0b32cde1a8b5273ae0c67fe2a6b

async_mode = 'eventlet'
app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'camDB.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app,async_mode=async_mode)

class Camera(db.Model):
    __tablename__='cameras'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(64),unique=True)
    ip_address = db.Column(db.String(64),unique=True)
    channel = db.Column(db.String(64))
    uid = db.Column(db.String(64))
    activity_monitor = db.Column(db.String,default='Both')

    def get_cam_name(self):
        return self.name
    @property
    def get_cam_id(self):
        return self.id
    def get_cam_ip(self):
        return self.ip_address
    def get_cam_channel(self):
        return self.channel
    def get_cam_uid(self):
        return self.uid
    def get_cam_activity(self):
        return self.activity_monitor
    

class CameraConfig(db.Model):
    __tablename__ = 'cameras_config'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    camera_id = db.Column(db.Integer,unique=True)
    cam_name = db.Column(db.String(64))
    ip = db.Column(db.String(64),unique=True)
    roi = db.Column(db.Text)

class Notifications(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(255))
    msg = db.Column(db.Text)
    image_url = db.Column(db.Text)

# done by sukanya
@app.route('/singlecamview')
def singlecam():
    c = Camera.query.all()
    return render_template('dashboard/single_cam.html',cams = c)

@app.route('/fourcamview')
def fourcam():
    return render_template('dashboard/four_cam.html')

@app.route('/eightcamview')
def eightcam():
    return render_template('dashboard/eight_cam.html',)

@app.route('/twentycamview')
def twentycam():
    return render_template('dashboard/twenty_cam.html')
# end code by sukanya

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

# for frames to be shown
def gen(camera):
    while True:
        frame = camera.getframe()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ frame +b'\r\n')

@app.route('/video/<ip>',methods=['GET'])
def video(ip):
    if ip == '0' or ip=='127.0.0.1':
        ip = 0
    return Response(gen(VideoCamera(ip)),content_type='multipart/x-mixed-replace;boundary=frame')

# for live cam page
@app.route('/player')
def player():
    c = Camera.query.all();
    if len(c)==0:
        error = 'Not camera found'
        return render_template('dashboard/cam/live.html',err = error)
    return render_template('dashboard/cam/live.html',cams = c)

# route for adding the camera
@app.route('/addcamera')
def add_cam_page():
    return render_template('dashboard/cam/create.html')

# route to cam management page
@app.route('/cameramanage')
def cam_manage():
    cams = Camera.query.all()
    if len(cams)==0:
        cams = 'No records found...'
        return render_template('dashboard/cam/index.html',cams=cams)

    return render_template('dashboard/cam/index.html',cams=cams)

@app.route('/remove-cam', methods=['POST'])
def remove_cam():
    c = Camera.query.get(request.form['camid'])
    cc = CameraConfig.query.filter_by(camera_id=c.id).first()
    if cc != None:
        db.session.delete(cc)
    else:
        pass
    db.session.delete(c)
    db.session.commit()
    c = Camera.query.all()
    return redirect('/cameramanage')

@app.route('/configure-cam', methods=['POST'])
def config_cam():
    c = Camera.query.get(request.form['camid'])
    ip = c.ip_address
    name = c.name
    name,ip,roi = captureFrame(ip,name)
    cam_conf = CameraConfig(camera_id=c.id,cam_name=name,ip=ip,roi=roi)
    db.session.add(cam_conf)
    db.session.commit()
    return redirect('/cameramanage')

@app.route('/add-camera', methods=['POST'])
def add_camera():
    pwd = request.form['password']
    cam_name = request.form['cam_name']
    if request.form['activity'] is None:
        activity = 'both'
    else:
        activity = request.form['activity']
    ipaddress = request.form['ipaddress']
    channel = request.form['channel']
    userid = request.form['uid']
    c = Camera(name=cam_name,ip_address=ipaddress,channel=channel,uid=userid,activity_monitor='Both')
    db.session.add(c)
    db.session.commit()
    test_connect([cam_name,channel,ipaddress]) # for notification showing
    return redirect('/cameramanage')


# this is for the notifications
# @socketio.on('noti',namespace='/notify')
def test_connect(data):
    print('--'*100)
    print('insdie test connect functions')
    print('--'*25)
    title = data[0]
    messages = data[1]
    image_url = data[2]
    notification = Notifications(title=title,msg=messages,image_url=image_url)
    db.session.add(notification)
    db.session.commit()
    pusher_client.trigger('my-channel', 'my-event', {'title':title,'message':messages,'img_url':image_url })

@app.route('/notifications')
def notifications():
    n = Notifications.query.all();

    if len(n)==0:
        n = 'No records found...'
        return render_template('dashboard/notifications/index.html',notify=n)
    return render_template('dashboard/notifications/index.html',notify=n) 

@app.route('/analytics')
def analytics():
    return render_template('dashboard/analytics.html')

@app.route('/index.html')
def index():
    return render_template('dashboard/admin.html', home=True)

@app.route('/')
def hello_world(): 
    return render_template('dashboard/admin.html', home=True)

@socketio.on('connect',namespace='/conn')    
def ws_con():
    socketio.emit('msg',{'message':'connected'},namespace='/conn')

# @socketio.on('disconnect',namespace='/notify')
# def ws_disconn():
#     socketio.emit('msg',{'message':'disconnected'},namespace='/notify')
# if __name__ == '__main__':
#     socketio.run(Threading=True,debug=True, host='127.0.0.1')
