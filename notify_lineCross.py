import os
import time
import datetime
from os.path import expanduser
import glob
import logging
import gi
from datetime import datetime
from datetime import date
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Notify', '0.7')
from gi.repository import Notify

global camera_name

def get_latest_log_folder(camera_name):
    """ Get latest log folder """
    today = str(date.today())
    dir_logs = "LineCrossing/{}/{}".format(today,camera_name)
    print(dir_logs)
    latest_file = sorted(glob.glob(dir_logs+"//Tresspass_alert_*"),key=os.path.getctime)[-2] # * means all if need specific format then *.csv
    #latest_file = (list_of_files, key=os.path.getctime)[-2]

    return latest_file

class ImageNotification:
    def __init__(self, camera_name):
        self.camera_name = camera_name
        Notify.init("Crowd Gathering")
        self.dir_log = get_latest_log_folder(camera_name)
        notification = Notify.Notification.new("Line Crossing at Camera %s" % (camera_name))
        os.system('echo%s ' % ("& xdg-open %s" % (self.dir_log)))
        #notification.show()
        

'''if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    camera_name = 'RingRoad5'
    obj = ImageNotification(camera_name)'''
