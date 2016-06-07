#!/usr/bin/env python
#coding=utf-8

import os
import json
import base64
import urllib
import urllib2
import ConfigParser
import subprocess

from roboyun_afr.srv import *
import rospy

from facepp import API,File

'''
FacePlusPlus Service need to register in http://www.faceplusplus.com
create your application, after that you will have your apikey,secretkey
all the information write in the nlu.cfg file like this:

[faceplusplus]

API_KEY = your application key
API_SECRET = your secret key


'''


def get_config():
    config = ConfigParser.ConfigParser()
    file_path = os.path.join(os.path.dirname(__file__),'afr.cfg')
    config.read(file_path)
    return config.get('faceplusplus','SERVER'),config.get('faceplusplus','API_KEY'),config.get('faceplusplus','API_SECRET')



def afr_online(msg):
    file_path = os.path.join(os.path.dirname(__file__),'face.jpg')
    subprocess.call('raspistill -o %s -t 300 -w 480 -h 360 '%file_path,shell=True)
    result = api.recognition.recognize(img = File(file_path), group_name = 'ry_robot_001')
    #print 'result',result
    if result['face']:
        return result['face'][0]['candidate'][0]['person_name']
    else:
        return 'no person'

def handle_afr(req):

    return AFRResponse(afr_online(req.controller_json))

def afr_server():
    rospy.init_node('roboyun_afr')
    s = rospy.Service('afr_online',AFR,handle_afr)
    rospy.spin()

if __name__ == '__main__':
    _,API_KEY,API_SECRET = get_config()
    api = API(API_KEY,API_SECRET)
    afr_server()
