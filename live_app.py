from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, send_from_directory
from datetime import date
from passlib.hash import pbkdf2_sha256
import pyrebase
import re
import natsort
from operator import itemgetter
import firebase_admin
from firebase_admin import credentials
from pyfcm import FCMNotification
from configGUI import *
from datetime import date
from datetime import datetime
# from firebase_admin import firebase_admin.messaging
from firebaseconfig import db
from markPointsVid import  captureFrame,get_mouse_points
# from lineCrossFinal_resnet_roi_copy1 import lineCross
# from lineCrossFinal_resnet_roi_test import lineCross
# from deepstream_test_3 import run_crowdcount

app = Flask(__name__, static_url_path='/static')


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

@app.route('/player')
def player():
    return render_template('display4.html', peoplecounting=True)

@app.route('/firebase-messaging-sw.js')
def sw():
    response=make_response(
                     send_from_directory('static',filename='firebase-messaging-sw.js'))
    #change the content header file
    response.headers['Content-Type']='application/javascript'
    return response

@app.route('/beep-02.mp3')
def beep_sound():
    response=make_response(
                     send_from_directory('static',filename='audio/beep-02.mp3'))
    #change the content header file
    response.headers['Content-Type']="audio/mpeg"
    return response

@app.route('/linecrossing')
def line_crossing():
    data = db.child('line Crossing').get().val().values()
    dict_sorted = natsort.natsorted(data, key=itemgetter(*['camera_name']))
    # klist = db.child("line Crossing").get().val().keys()
    # klist.sort(key=natural_keys)
    return render_template('linecrossing.html', data=dict_sorted, cam_type="linecrossing")

# FIXME: HIMADRI CONFIGURE THIS
@app.route('/pplCount')
def people_count():
    # data = db.child('Crowd Counting').get().val().values()
    # dict_sorted = natsort.natsorted(data, key=itemgetter(*['camera_name']))
    # klist = db.child("line Crossing").get().val().keys()
    # klist.sort(key=natural_keys)
    # return render_template('pplecount.html', data=dict_sorted, cam_type="crowdcount")
    return render_template('pplecount.html')

@app.route('/crowdcount')
def crowd_count():
    try:
        data = db.child('Crowd Count').get().val().values()
    except:
        return render_template('index.html')
    return render_template('crowdcount.html', data=data, cam_type="crowdcount")

@app.route('/linecrossing/<cam_id>')
def cam1(cam_id):
    data = {'id' : cam_id}
    camdata = db.child("cameras").child(cam_id).get().val()
    print(camdata)
    return render_template('cam1.html', data=data, camdata=camdata)

# route for adding the camera
@app.route('/addcamera')
def add_cam_page():
    return render_template('dashboard/cam/create.html')

# route to cam management page
@app.route('/cameramanage')
def cam_manage():
    return render_template('dashboard/cam/index.html')

@app.route('/cam-info', methods=['POST', 'GET'])
def cam_info():
    camdata = db.child('line Crossing').get().val().values()
    dict_sorted = natsort.natsorted(camdata, key=itemgetter(*['camera_name']))
    return jsonify(dict_sorted)

@app.route('/remove-cam', methods=['POST'])
def remove_cam():
    data = request.get_json()['id']
    try:
        db.child('line Crossing').child(data).remove()
    except:
        return jsonify({ "success": False })
    return jsonify({ "success": True })

@app.route('/configure-cam/<camid>', methods=['POST'])
def config_cam(camid):
    try:
        camdata = db.child('line Crossing').child(camid).get().val()
    except:
        return jsonify({"success": False})
    try: 
        info = configure(camdata)
    except:
        return jsonify({"success": False})
    
    [line1, line2, regionPts, case, slope] = info
    line1 = str(line1)
    line2 = str(line2)
    regionPts = str(regionPts)
    line1 = [(line1.strip('()').split('), (')[0]), (line1.strip('()').split('), (')[1])]
    # line2 = camDetails['Line2'].values[i]
    line2 = [((line2.strip('()').split('), (')[0])), ((line2.strip('()').split('), (')[1]))]
    regionPts = [((regionPts.strip('[]').split('], [')[0])), ((regionPts.strip('[]').split('], [')[1])),((regionPts.strip('[]').split('], [')[2])), ((regionPts.strip('[]').split('], [')[3])) ]
    print(info)
    print(regionPts)
    try:
        db.child('line Crossing').child(camid).child('configuration').set({"line1": line1, "line2":line2, "regionPts":regionPts, "case": case, "slope":slope})
        return jsonify({ "success": True })
    except:
        return jsonify({ "success": False })

@app.route('/add-camera', methods=['POST'])
def add_camera():
    pwd = request.form['password']
    cam_name = request.form['cam_name']
    activity = request.form['activity']
    ipaddress = request.form['ipaddress']
    channel = request.form['channel']
    userid = request.form['uid']
    db.child(activity).child(cam_name).set({ 'password': pwd, 'camera_name': cam_name, 'activity': activity, 'ipaddress': ipaddress, 'channel': channel, 'userid': userid })
    return render_template('camManage.html')

@app.route('/run-lc-configuration', methods=['POST'])
def run_lc_config():
    try:
        lineCross()
        return jsonify({ "success": True })
    except:
        return jsonify({ "success": False })

    return render_template('index.html', home=True)

@app.route('/run-cc-configuration', methods=['POST'])
def run_cc_config():
    try:
        run_crowdcount()
        return jsonify({ "success": True })
    except:
        return jsonify({ "success": False })

    # return render_template('index.html', home=True)

@app.route('/camsd4', methods=['POST'])
def display_four():
    formdata = request.form
    data = db.child('line Crossing').get().val().values()
    dict_sorted = natsort.natsorted(data, key=itemgetter(*['camera_name']))
    today = str(date.today())
    return render_template('display4.html', formdata=formdata, today=today, data=dict_sorted)

@app.route('/camsd8', methods=['POST'])
def display_eight():
    data = request.form
    today = str(date.today())
    return render_template('display8.html', data=data, today=today)

@app.route('/index.html')
def index():
    return render_template('dashboard/admin.html', home=True)

@app.route('/')
def hello_world():    
    return render_template('dashboard/admin.html', home=True)
    
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
